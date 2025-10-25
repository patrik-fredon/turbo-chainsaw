# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a **Spec-ify** template repository that uses a structured specification-driven development workflow. The repository is organized around the following key directories:

- `.specify/` - Contains templates, scripts, and memory for the Spec-ify workflow
- `.claude/commands/` - Custom slash commands for feature development
- `specs/` - Feature specifications and implementation plans (created during development)

## Core Development Workflow

This repository follows a **specification-first** development approach using custom slash commands:

### 1. Feature Specification
- `/speckit.specify` - Create or update feature specifications from natural language descriptions
- `/speckit.clarify` - Identify underspecified areas and ask targeted clarification questions

### 2. Implementation Planning
- `/speckit.plan` - Generate technical implementation plans and design artifacts
- `/speckit.tasks` - Create actionable, dependency-ordered task breakdowns

### 3. Development Execution
- `/speckit.implement` - Execute implementation plans by processing all tasks
- `/speckit.analyze` - Perform cross-artifact consistency and quality analysis

### 4. Quality Assurance
- `/speckit.checklist` - Generate custom checklists based on feature requirements

## Development Commands

### Prerequisites Check
```bash
# Check if development environment is ready
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

### Feature Branch Management
The repository uses numbered feature branches (e.g., `001-feature-name`, `002-add-auth`). Use the common functions in `.specify/scripts/bash/common.sh` for branch and path resolution.

### Constitution-Driven Development
The project is governed by a constitution defined in `.specify/memory/constitution.md`. All development must comply with constitutional principles, which typically include:
- Library-first architecture
- CLI interface requirements
- Test-first development (TDD)
- Integration testing focus
- Observability and versioning standards

## File Organization

### Template System
- `.specify/templates/` - Markdown templates for all specification artifacts
- `spec-template.md` - Feature specification template
- `plan-template.md` - Implementation plan template
- `tasks-template.md` - Task breakdown template
- `checklist-template.md` - Quality checklist template

### Script Utilities
- `.specify/scripts/bash/` - Bash utilities for workflow automation
- `common.sh` - Shared functions for repository navigation and branch management
- `check-prerequisites.sh` - Environment and dependency validation
- `setup-plan.sh` - Plan generation workflow
- `create-new-feature.sh` - Feature creation automation

## Important Notes

- **No Traditional Source Code**: This is a template repository - actual source code will be created during feature implementation
- **Specification-First**: All development starts with user requirements and proceeds through structured planning
- **Branch Naming**: Use numbered prefixes (001-, 002-, etc.) for feature branches to enable proper spec mapping
- **Task Dependencies**: Implementation follows strict dependency ordering - foundational phases block user story work
- **Independent Testing**: Each user story should be independently testable and deliverable as an MVP increment

## Getting Started

1. Create a feature specification: `/speckit.specify "your feature description"`
2. Generate implementation plan: `/speckit.plan`
3. Create task breakdown: `/speckit.tasks`
4. Execute implementation: `/speckit.implement`

The workflow ensures all development is traceable from user requirements through to working code.

## Active Technologies
- Python 3.11+ + GTK3, gtk-layer-shell, python-gobject, gdk-pixbuf2, python-pillow (001-fredon-menu)
- JSON configuration file at ~/.config/fredon-menu/config.json, optional icon cache (001-fredon-menu)

## Recent Changes
- 001-fredon-menu: Added Python 3.11+ + GTK3, gtk-layer-shell, python-gobject, gdk-pixbuf2, python-pillow
