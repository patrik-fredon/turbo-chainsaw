"""
Secure command execution system for Fredon Menu
"""

import os
import shlex
import subprocess
import logging
import time
from typing import List, Optional, Dict, Any
from enum import Enum

from .models import CommandType

logger = logging.getLogger(__name__)


class ExecutionResult:
    """Result of command execution."""

    def __init__(self, success: bool, exit_code: int = None, stdout: str = "",
                 stderr: str = "", execution_time_ms: float = 0,
                 error: Optional[str] = None):
        self.success = success
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.execution_time_ms = execution_time_ms
        self.error = error


class SecurityValidator:
    """Validates command security before execution."""

    # Blocked characters and patterns
    BLOCKED_CHARACTERS = [';', '&', '|', '`', '$', '(', ')', '<', '>', '"', "'"]
    BLOCKED_PATTERNS = [
        r'rm\s+-rf',
        r'sudo\s+',
        r'su\s+',
        r'passwd',
        r'chmod\s+\d',
        r'chown\s+',
        r'mkfs',
        r'dd\s+if=',
        r'fdisk',
        r'mount',
        r'umount',
    ]

    # Allowed command prefixes
    ALLOWED_PREFIXES = [
        '/usr/bin/',
        '/usr/local/bin/',
        '/bin/',
        '/snap/bin/',
        'npm ',
        'python',
        'python3',
        'node',
        'flatpak ',
        'xdg-open',
    ]

    # Blocked command names
    BLOCKED_COMMANDS = [
        'rm', 'sudo', 'su', 'passwd', 'chmod', 'chown',
        'dd', 'mkfs', 'fdisk', 'mount', 'umount'
    ]

    @classmethod
    def validate_command(cls, command: str, command_type: CommandType) -> tuple[bool, Optional[str]]:
        """
        Validate command is safe to execute.

        Args:
            command: Command string to validate
            command_type: Type of command execution

        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not command or not command.strip():
            return False, "Empty command not allowed"

        command = command.strip()

        # Check for blocked characters
        for char in cls.BLOCKED_CHARACTERS:
            if char in command:
                return False, f"Blocked character '{char}' found in command"

        # Check for blocked patterns
        import re
        for pattern in cls.BLOCKED_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Blocked pattern '{pattern}' found in command"

        # Check for blocked commands
        command_parts = command.split()
        if command_parts:
            base_command = command_parts[0]
            if base_command in cls.BLOCKED_COMMANDS:
                return False, f"Blocked command '{base_command}' not allowed"

        # Validate based on command type
        if command_type == CommandType.SHELL:
            return cls._validate_shell_command(command)
        elif command_type == CommandType.NPM:
            return cls._validate_npm_command(command)
        elif command_type == CommandType.PYTHON:
            return cls._validate_python_command(command)
        elif command_type == CommandType.APP:
            return cls._validate_app_command(command)

        return False, f"Unknown command type: {command_type}"

    @classmethod
    def _validate_shell_command(cls, command: str) -> tuple[bool, Optional[str]]:
        """Validate shell command."""
        # Check if command starts with allowed prefix
        for prefix in cls.ALLOWED_PREFIXES:
            if command.startswith(prefix):
                return True, None

        # Check if command is a simple executable name
        command_parts = command.split()
        if command_parts:
            base_command = command_parts[0]
            # Allow simple commands without path
            if '/' not in base_command and len(base_command) > 0:
                return True, None

        return False, "Shell command does not start with allowed prefix"

    @classmethod
    def _validate_npm_command(cls, command: str) -> tuple[bool, Optional[str]]:
        """Validate NPM command."""
        if not command.strip():
            return False, "Empty NPM script name"

        # NPM scripts should be simple names
        if ' ' in command.strip():
            return False, "NPM script names should not contain spaces"

        return True, None

    @classmethod
    def _validate_python_command(cls, command: str) -> tuple[bool, Optional[str]]:
        """Validate Python command."""
        if not os.path.exists(command):
            return False, f"Python script not found: {command}"

        if not command.endswith('.py'):
            return False, "Python scripts must end with .py"

        return True, None

    @classmethod
    def _validate_app_command(cls, command: str) -> tuple[bool, Optional[str]]:
        """Validate desktop application command."""
        # Check if it's a .desktop file
        if command.endswith('.desktop'):
            if not os.path.exists(command):
                return False, f"Desktop file not found: {command}"
            return True, None

        # Check if command exists in PATH
        command_parts = command.split()
        if command_parts:
            base_command = command_parts[0]
            if '/' in base_command:
                # Full path - check if executable exists
                if not os.path.exists(base_command):
                    return False, f"Application not found: {base_command}"
                if not os.access(base_command, os.X_OK):
                    return False, f"Application not executable: {base_command}"
            else:
                # Command name - check if it exists in PATH
                import shutil
                if not shutil.which(base_command):
                    return False, f"Command not found in PATH: {base_command}"

        return True, None


class CommandLauncher:
    """Handles secure command execution."""

    def __init__(self):
        self.max_execution_time = 30  # seconds

    def execute_command(self, command: str, command_type: CommandType,
                        working_dir: Optional[str] = None,
                        env: Optional[Dict[str, str]] = None) -> ExecutionResult:
        """
        Execute command securely.

        Args:
            command: Command to execute
            command_type: Type of command execution
            working_dir: Working directory for execution
            env: Environment variables

        Returns:
            ExecutionResult with execution details
        """
        start_time = time.time()

        # Validate command security
        is_valid, error_message = SecurityValidator.validate_command(command, command_type)
        if not is_valid:
            return ExecutionResult(
                success=False,
                error=error_message,
                execution_time_ms=(time.time() - start_time) * 1000
            )

        try:
            if command_type == CommandType.SHELL:
                result = self._execute_shell_command(command, working_dir, env, start_time)
            elif command_type == CommandType.NPM:
                result = self._execute_npm_command(command, working_dir, env, start_time)
            elif command_type == CommandType.PYTHON:
                result = self._execute_python_command(command, working_dir, env, start_time)
            elif command_type == CommandType.APP:
                result = self._execute_app_command(command, working_dir, env, start_time)
            else:
                result = ExecutionResult(
                    success=False,
                    error=f"Unknown command type: {command_type}",
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            logger.info(f"Command executed: {command_type.value} - {command[:50]}... "
                       f"Success: {result.success}")
            return result

        except Exception as e:
            logger.error(f"Unexpected error executing command '{command}': {e}")
            return ExecutionResult(
                success=False,
                error=f"Unexpected error: {str(e)}",
                execution_time_ms=(time.time() - start_time) * 1000
            )

    def _execute_shell_command(self, command: str, working_dir: Optional[str],
                               env: Optional[Dict[str, str]], start_time: float) -> ExecutionResult:
        """Execute shell command."""
        # Parse command safely
        try:
            # Use shlex.split to properly handle arguments
            args = shlex.split(command)
        except ValueError as e:
            return ExecutionResult(
                success=False,
                error=f"Invalid command syntax: {e}",
                execution_time_ms=(time.time() - start_time) * 1000
            )

        try:
            # Execute command without shell
            process = subprocess.run(
                args,
                cwd=working_dir,
                env=env,
                timeout=self.max_execution_time,
                capture_output=True,
                text=True,
                start_new_session=True  # Run in new process group
            )

            return ExecutionResult(
                success=process.returncode == 0,
                exit_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
                execution_time_ms=(time.time() - start_time) * 1000
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                error=f"Command timed out after {self.max_execution_time} seconds",
                execution_time_ms=(time.time() - start_time) * 1000
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Execution failed: {e}",
                execution_time_ms=(time.time() - start_time) * 1000
            )

    def _execute_npm_command(self, script_name: str, working_dir: Optional[str],
                            env: Optional[Dict[str, str]], start_time: float) -> ExecutionResult:
        """Execute NPM script."""
        # Find package.json directory
        if working_dir is None:
            working_dir = os.getcwd()

        package_json_path = os.path.join(working_dir, 'package.json')
        if not os.path.exists(package_json_path):
            return ExecutionResult(
                success=False,
                error=f"package.json not found in {working_dir}",
                execution_time_ms=(time.time() - start_time) * 1000
            )

        # Validate script exists in package.json
        import json
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)

            scripts = package_data.get('scripts', {})
            if script_name not in scripts:
                return ExecutionResult(
                    success=False,
                    error=f"NPM script '{script_name}' not found in package.json",
                    execution_time_ms=(time.time() - start_time) * 1000
                )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Error reading package.json: {e}",
                execution_time_ms=(time.time() - start_time) * 1000
            )

        # Execute npm run command
        npm_command = f"npm run {script_name}"
        return self._execute_shell_command(npm_command, working_dir, env, start_time)

    def _execute_python_command(self, script_path: str, working_dir: Optional[str],
                               env: Optional[Dict[str, str]], start_time: float) -> ExecutionResult:
        """Execute Python script."""
        python_command = f"python3 {script_path}"
        return self._execute_shell_command(python_command, working_dir, env, start_time)

    def _execute_app_command(self, command: str, working_dir: Optional[str],
                           env: Optional[Dict[str, str]], start_time: float) -> ExecutionResult:
        """Execute desktop application."""
        try:
            if command.endswith('.desktop'):
                # Execute desktop file
                desktop_command = f"gtk-launch {os.path.basename(command)}"
                # Launch application in background without waiting
                args = shlex.split(desktop_command)
                subprocess.Popen(
                    args,
                    cwd=working_dir,
                    env=env,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Execute application directly in background
                args = shlex.split(command)
                subprocess.Popen(
                    args,
                    cwd=working_dir,
                    env=env,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            # For apps, we don't wait for completion
            return ExecutionResult(
                success=True,
                exit_code=0,
                execution_time_ms=(time.time() - start_time) * 1000
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Failed to launch application: {e}",
                execution_time_ms=(time.time() - start_time) * 1000
            )