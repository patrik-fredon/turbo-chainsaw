# Launcher API Contract

**Version**: 1.0
**Date**: 2025-10-25
**Purpose**: Define application launching interface and command execution patterns

## Command Execution Interface

### Execution Types

```python
class CommandType(Enum):
    """Supported command execution types."""

    SHELL = "shell"           # Execute via system shell
    NPM = "npm"               # Run npm script
    PYTHON = "python"         # Execute Python script
    APP = "app"               # Launch desktop application
```

### Execution API

```python
def execute_command(button: Button) -> ExecutionResult:
    """
    Execute command associated with button securely.

    Args:
        button: Button configuration with command details

    Returns:
        ExecutionResult containing:
        - success: boolean
        - exit_code: int (if command executed)
        - stdout: str (captured output)
        - stderr: str (error output)
        - execution_time_ms: float
        - error: ExecutionError (if failed)

    Security features:
    - Command validation against whitelist
    - Argument sanitization and escaping
    - User permission isolation
    - Resource limits enforcement
    - Timeout protection
    """
```

### Command Validation

```python
class CommandValidator:
    """Validates command safety before execution."""

    def validate_command(command: str, command_type: CommandType) -> ValidationResult:
        """
        Validate command is safe to execute.

        Validation rules:
        1. Check against blocked commands list
        2. Scan for dangerous characters
        3. Validate command path is within allowed directories
        4. Check file permissions and existence
        5. Verify command type compatibility

        Returns:
        - valid: boolean
        - sanitized_command: str (if valid)
        - warnings: List[str]
        - errors: List[SecurityError]
        """
```

## Execution Patterns

### Shell Commands

```python
def execute_shell_command(command: str) -> ExecutionResult:
    """
    Execute shell command with security constraints.

    Pattern:
    - Validate command against whitelist
    - Use subprocess.run() with shell=False
    - Sanitize arguments properly
    - Set resource limits
    - Capture output for error reporting

    Example:
    Input: "firefox -new-window https://example.com"
    Output: subprocess.run(["firefox", "-new-window", "https://example.com"])
    """
```

### NPM Scripts

```python
def execute_npm_script(script_name: str, project_path: str = None) -> ExecutionResult:
    """
    Execute NPM script from package.json.

    Pattern:
    - Locate package.json file
    - Validate script exists in scripts section
    - Run "npm run script_name" in project directory
    - Handle npm-specific error codes

    Example:
    Input: script_name="dev", project_path="/home/user/myapp"
    Output: subprocess.run(["npm", "run", "dev"], cwd="/home/user/myapp")
    """
```

### Python Scripts

```python
def execute_python_script(script_path: str, args: List[str] = None) -> ExecutionResult:
    """
    Execute Python script with proper environment.

    Pattern:
    - Validate script file exists and is .py
    - Use system Python or configured interpreter
    - Pass arguments safely
    - Set PYTHONPATH if needed

    Example:
    Input: script_path="/home/user/scripts/backup.py", args=["--full"]
    Output: subprocess.run(["python3", "/home/user/scripts/backup.py", "--full"])
    """
```

### Desktop Applications

```python
def execute_desktop_application(app_command: str) -> ExecutionResult:
    """
    Launch desktop application.

    Pattern:
    - Parse .desktop file if app name provided
    - Validate executable exists
    - Launch with proper environment
    - Handle Wayland-specific considerations

    Example:
    Input: "org.mozilla.firefox"
    Output: Parse /usr/share/applications/firefox.desktop and execute Exec= line
    """
```

## Security Contract

### Command Whitelist

```yaml
allowed_commands:
  system:
    - /usr/bin/firefox
    - /usr/bin/chromium
    - /usr/bin/code
    - /usr/bin/gimp
    - /usr/bin/libreoffice
  development:
    - npm
    - yarn
    - python
    - python3
    - node
  utilities:
    - xdg-open
    - gnome-terminal
    - alacritty
    - nautilus
    - thunar
```

### Blocked Patterns

```python
BLOCKED_PATTERNS = [
    r'[;&|`$()]',           # Shell metacharacters
    r'rm\s+-rf',           # Dangerous file operations
    r'sudo\s+',             # Privilege escalation
    r'passwd',              # Password modification
    r'chmod\s+[0-9]',       # Permission changes
    r'chown\s+',            # Ownership changes
    r'mkfs',                # Filesystem operations
    r'dd\s+if=',            # Disk operations
]
```

### Resource Limits

```python
class ResourceLimits:
    """Resource constraints for command execution."""

    max_execution_time_s: int = 30      # Maximum execution time
    max_memory_mb: int = 512            # Maximum memory usage
    max_cpu_percent: float = 50.0       # Maximum CPU usage
    max_processes: int = 10              # Maximum child processes
```

## Error Handling

### Execution Errors

```yaml
# Command execution error response
error:
  type: "execution_error"
  message: "Failed to execute command"
  details:
    command: "firefox -new-window"
    exit_code: 127
    error_type: "COMMAND_NOT_FOUND"
    stderr: "bash: firefox: command not found"
    execution_time_ms: 45
    suggestions:
      - "Install Firefox: sudo pacman -S firefox"
      - "Check if command is in PATH"
      - "Verify executable permissions"
```

### Security Errors

```yaml
# Security violation error response
error:
  type: "security_error"
  message: "Command blocked for security reasons"
  details:
    command: "rm -rf /home/user"
    violation_type: "DANGEROUS_COMMAND_PATTERN"
    blocked_pattern: "rm -rf"
    rule: "DESTRUCTIVE_OPERATION_BLOCKED"
    security_level: "HIGH"
```

### Timeout Errors

```yaml
# Execution timeout error response
error:
  type: "timeout_error"
  message: "Command execution timed out"
  details:
    command: "sleep 60"
    timeout_seconds: 30
    actual_runtime_seconds: 30
    action_taken: "PROCESS_TERMINATED"
    suggestion: "Increase timeout limit or optimize command"
```

## Integration API

### Environment Setup

```python
def setup_execution_environment() -> EnvironmentResult:
    """
    Setup secure execution environment.

    Returns:
    - wayland_display: str (WAYLAND_DISPLAY)
    - xdg_runtime_dir: str (XDG_RUNTIME_DIR)
    - home_directory: str (HOME)
    - path_entries: List[str] (secure PATH)
    - environment_vars: Dict[str, str] (additional env vars)
    """
```

### Process Management

```python
class ProcessManager:
    """Manage launched processes."""

    def launch_process(command: List[str], env: Dict[str, str]) -> ProcessResult:
        """
        Launch process with proper environment.

        Features:
        - Detach from parent process
        - Set proper user permissions
        - Handle Wayland display
        - Monitor for zombie processes
        """

    def cleanup_processes() -> CleanupResult:
        """
        Cleanup terminated processes.

        Features:
        - Reap zombie processes
        - Close file descriptors
        - Free resources
        - Update process statistics
        """
```

## Performance Monitoring

### Execution Metrics

```python
class ExecutionMetrics:
    """Command execution performance metrics."""

    total_executions: int              # Total commands executed
    successful_executions: int         # Successful executions
    failed_executions: int             # Failed executions
    average_execution_time_ms: float   # Average execution time
    max_execution_time_ms: float       # Maximum execution time
    security_violations: int           # Blocked commands
    timeout_occurrences: int           # Timeout events
```

### Performance Targets

```yaml
targets:
  command_launch_ms: <= 100           # Time to start execution
  average_execution_ms: <= 2000       # Average command runtime
  security_validation_ms: <= 10       # Security check time
  process_cleanup_ms: <= 50           # Process cleanup time
  memory_overhead_mb: <= 10           # Additional memory usage
```

## Testing Contract

### Unit Tests

```python
class LauncherTests:
    """Test suite for launcher functionality."""

    def test_command_validation():
        """Test command security validation."""

    def test_shell_execution():
        """Test shell command execution."""

    def test_npm_script_execution():
        """Test NPM script execution."""

    def test_python_script_execution():
        """Test Python script execution."""

    def test_security_blocking():
        """Test dangerous command blocking."""

    def test_timeout_handling():
        """Test execution timeout handling."""
```

### Integration Tests

```python
class LauncherIntegrationTests:
    """Integration tests for launcher with real applications."""

    def test_firefox_launch():
        """Test launching Firefox browser."""

    def test_terminal_launch():
        """Test launching terminal emulator."""

    def test_code_editor_launch():
        """Test launching code editor."""

    def test_file_manager_launch():
        """Test launching file manager."""
```

This contract defines the complete application launching interface with comprehensive security measures, error handling, performance requirements, and testing standards for the Fredon Menu application.