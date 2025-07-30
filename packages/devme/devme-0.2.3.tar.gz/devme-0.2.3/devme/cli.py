"""
DevMe CLI - Command Line Interface
"""

import click
import sys
from pathlib import Path
from .core import DevMe
from .server import serve_dashboard
from .export import export_markdown, export_html


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version and exit')
@click.pass_context
def main(ctx, version):
    """DevMe - Developer Dashboard Tool
    
    Shows project health, configuration status, and development environment info.
    """
    if version:
        from . import __version__
        click.echo(f"DevMe version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        # Default behavior - show dashboard
        devme = DevMe()
        status = devme.get_status()
        
        click.echo("🔍 DevMe - Project Status")
        click.echo("=" * 40)
        
        # Git status
        git_info = status.get('git', {})
        if git_info:
            click.echo(f"📁 Repository: {git_info.get('name', 'Unknown')}")
            click.echo(f"🌿 Branch: {git_info.get('current_branch', 'Unknown')}")
            click.echo(f"📝 Recent commits: {git_info.get('recent_commits', 0)}")
        else:
            click.echo("📁 No git repository found")
        
        # File checks
        files = status.get('files', {})
        click.echo(f"📄 README: {'✅' if files.get('readme') else '❌'}")
        click.echo(f"🧪 Tests: {'✅' if files.get('tests') else '❌'}")
        click.echo(f"📦 Package config: {'✅' if files.get('package_config') else '❌'}")
        
        # Quick stats
        click.echo(f"\n📊 Project files: {status.get('file_count', 0)}")
        click.echo(f"⏰ Last updated: {status.get('last_updated', 'Unknown')}")


@main.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=6174, help='Port to bind to (default: 6174 - Kaprekar\'s constant)')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--open', 'open_browser', is_flag=True, help='Open browser automatically')
def serve(host, port, debug, open_browser):
    """Start the DevMe web dashboard server"""
    url = f"http://{host}:{port}"
    click.echo(f"🚀 Starting DevMe dashboard at {url}")
    if open_browser:
        click.echo("🌐 Opening browser...")
    click.echo("Press Ctrl+C to stop")
    
    # Open browser if requested
    if open_browser:
        import webbrowser
        import threading
        import time
        
        def open_browser_delayed():
            time.sleep(1.5)  # Give server time to start
            webbrowser.open(url)
        
        threading.Thread(target=open_browser_delayed, daemon=True).start()
    
    try:
        serve_dashboard(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        click.echo("\n👋 DevMe dashboard stopped")
    except Exception as e:
        click.echo(f"❌ Error starting server: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--format', type=click.Choice(['md', 'html']), default='md', help='Export format')
@click.option('--output', help='Output file path')
@click.option('--open', 'open_file', is_flag=True, help='Open exported file after creation')
def export(format, output, open_file):
    """Export project status to markdown or HTML"""
    devme = DevMe()
    
    if format == 'md':
        if not output:
            output = 'DEVME.md'
        export_markdown(devme, output)
        click.echo(f"📄 Exported to {output}")
    elif format == 'html':
        if not output:
            output = 'devme.html'
        export_html(devme, output)
        click.echo(f"🌐 Exported to {output}")
    
    if open_file:
        import webbrowser
        webbrowser.open(f'file://{Path(output).absolute()}')


@main.command()
def init():
    """Initialize DevMe configuration in current directory"""
    devme_dir = Path('.devme')
    legacy_config = Path('.devme.json')
    
    # Check if any configuration already exists
    if devme_dir.exists() or legacy_config.exists():
        click.echo("⚠️  DevMe configuration already exists")
        return
    
    # Create .devme directory structure
    import json
    devme_dir.mkdir(exist_ok=True)
    
    # Main configuration file
    config = {
        "project_name": Path.cwd().name,
        "env_file_patterns": [
            ".env*",
            "server/.env*", 
            "client/.env*",
            "api/.env*",
            "backend/.env*",
            "frontend/.env*",
            "config/.env*",
            "environments/.env*"
        ],
        "search_depth": 3,
        "ignore_patterns": [".git", "__pycache__", "node_modules", ".venv", "dist", "build"],
        "external_services": {},
        "custom_checks": []
    }
    
    config_file = devme_dir / 'config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Create additional configuration files
    env_paths_file = devme_dir / 'env-paths.json'
    env_paths = {
        "description": "Custom environment file paths for complex projects",
        "additional_paths": [
            "examples: 'docker/.env', 'scripts/local.env', 'deployment/staging.env'"
        ]
    }
    with open(env_paths_file, 'w') as f:
        json.dump(env_paths, f, indent=2)
    
    # Create ignore file
    ignore_file = devme_dir / 'ignore.txt'
    with open(ignore_file, 'w') as f:
        f.write("# Additional patterns to ignore during file counting\n")
        f.write("# One pattern per line\n")
        f.write("*.log\n")
        f.write("*.tmp\n")
        f.write("coverage/\n")
    
    # Create README
    readme_file = devme_dir / 'README.md'
    with open(readme_file, 'w') as f:
        f.write("""# DevMe Configuration

This directory contains DevMe configuration files:

- **config.json**: Main configuration
- **env-paths.json**: Additional environment file paths
- **ignore.txt**: Additional ignore patterns
- **custom-services.yaml**: Custom service definitions (create as needed)

## Configuration Options

### env_file_patterns
Patterns for finding environment files recursively:
```json
[
  ".env*",
  "server/.env*",
  "config/.env*"
]
```

### search_depth
How deep to search for environment files (default: 3)

### ignore_patterns
Patterns to ignore when counting project files
""")
    
    click.echo(f"✅ Created .devme/ directory with configuration files")
    click.echo("📁 Files created:")
    click.echo(f"   - {config_file}")
    click.echo(f"   - {env_paths_file}")
    click.echo(f"   - {ignore_file}")
    click.echo(f"   - {readme_file}")
    click.echo("\n📝 Edit these files to customize your DevMe configuration")
    click.echo("🔍 DevMe will now recursively search for .env files in subdirectories")


if __name__ == '__main__':
    main()