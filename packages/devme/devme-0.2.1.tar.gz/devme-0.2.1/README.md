# DevMe

A lightweight developer dashboard that provides instant visibility into your project's health, configuration status, and development environment.

## What is DevMe?

DevMe is like a README for your development environment - it shows you the current state of your project, external service connections, git status, and more. Think of it as a "health check" for your entire development setup.

## Quick Start

```bash
pip install devme
cd your-project
devme
```

## Features

- **Project Health**: Git status, recent commits, branch information
- **Configuration Status**: Environment variables, external service connections
- **File Presence**: README, tests, documentation checks
- **Export Options**: Generate markdown or HTML reports for sharing

## Usage

```bash
# Show project dashboard
devme

# Start web server
devme serve

# Export project status
devme export --md
devme export --html

# Show version
devme --version
```

## Use Cases

- **Code Reviews**: "Here's my devme before the PR"
- **Team Onboarding**: "Check the devme to see what's configured"
- **Debugging**: "My devme shows these issues..."
- **Project Health**: Quick overview of project state

## Development Status

This is an early alpha release to claim the package name and establish the foundation. More features coming soon!

## License

MIT License