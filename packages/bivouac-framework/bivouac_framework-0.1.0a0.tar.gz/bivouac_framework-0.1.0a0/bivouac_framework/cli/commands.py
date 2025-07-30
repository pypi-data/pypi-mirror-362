"""
CLI Commands for Bivouac Framework.

This module provides command-line interface commands for managing
Bivouac Framework applications.
"""

import os
import sys
import click
from pathlib import Path
from .. import __version__


@click.group()
@click.version_option(version=__version__, prog_name="bivouac-framework")
def main():
    """
    Bivouac Framework CLI
    
    A command-line interface for managing Bivouac Framework applications.
    """
    pass


@main.command()
@click.argument('app_name')
@click.option('--template', '-t', default='basic', 
              help='Application template to use')
@click.option('--directory', '-d', default=None,
              help='Directory to create the application in')
def create_app(app_name, template, directory):
    """
    Create a new Bivouac Framework application.
    
    This command creates a new application with the basic structure
    and configuration files.
    """
    if directory is None:
        directory = app_name
    
    app_path = Path(directory)
    
    if app_path.exists():
        click.echo(f"Error: Directory '{directory}' already exists", err=True)
        sys.exit(1)
    
    try:
        # Create application directory
        app_path.mkdir(parents=True)
        
        # Create basic application structure
        _create_app_structure(app_path, app_name, template)
        
        click.echo(f"✅ Created Bivouac Framework application '{app_name}' in '{directory}'")
        click.echo(f"📁 Application structure created successfully")
        click.echo(f"🚀 To get started:")
        click.echo(f"   cd {directory}")
        click.echo(f"   python app.py")
        
    except Exception as e:
        click.echo(f"Error creating application: {e}", err=True)
        sys.exit(1)


@main.command()
def list_modules():
    """
    List available modules in the current application.
    """
    try:
        from ..core.module_registry import ModuleRegistry
        
        modules = ModuleRegistry.get_all_modules()
        
        if not modules:
            click.echo("No modules found.")
            return
        
        click.echo("Available modules:")
        click.echo("-" * 50)
        
        for module in modules:
            status = "✅ Active" if ModuleRegistry.is_active(module.name) else "❌ Inactive"
            click.echo(f"{module.name} v{module.version} - {status}")
            
            if module.description:
                click.echo(f"  Description: {module.description}")
            
            if module.dependencies:
                click.echo(f"  Dependencies: {', '.join(module.dependencies)}")
            
            if module.optional_dependencies:
                click.echo(f"  Optional: {', '.join(module.optional_dependencies)}")
            
            click.echo()
            
    except ImportError:
        click.echo("Error: Could not import module registry", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error listing modules: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config', '-c', default='development',
              help='Configuration to use (development, testing, production)')
def init_db(config):
    """
    Initialize the database for the current application.
    """
    try:
        from ..core.config import config as config_map
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        # Create Flask app with configuration
        app = Flask(__name__)
        config_class = config_map.get(config, config_map['default'])
        app.config.from_object(config_class)
        
        # Initialize database
        db = SQLAlchemy(app)
        
        with app.app_context():
            db.create_all()
            click.echo(f"✅ Database initialized successfully with '{config}' configuration")
            
    except Exception as e:
        click.echo(f"Error initializing database: {e}", err=True)
        sys.exit(1)


def _create_app_structure(app_path, app_name, template):
    """
    Create the basic application structure.
    
    Args:
        app_path: Path to the application directory
        app_name: Name of the application
        template: Template to use
    """
    # Create main application file
    app_py_content = f'''"""
{app_name} - A Bivouac Framework Application

This is a Flask application built with the Bivouac Framework.
"""

from bivouac_framework import create_app
from bivouac_framework.core.config import DevelopmentConfig

# Create and configure the application
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open(app_path / 'app.py', 'w') as f:
        f.write(app_py_content)
    
    # Create requirements.txt
    requirements_content = '''bivouac-framework>=0.1.0-alpha
Flask>=2.3.0
Flask-SQLAlchemy>=3.0.0
Flask-User>=1.0.0
Flask-WTF>=1.1.0
WTForms>=3.0.0
SQLAlchemy>=2.0.0
Werkzeug>=2.3.0
click>=8.0.0
python-dotenv>=1.0.0
'''
    
    with open(app_path / 'requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    # Create .env file
    env_content = '''# Environment Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///app.db
'''
    
    with open(app_path / '.env', 'w') as f:
        f.write(env_content)
    
    # Create .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env

# Database
*.db
*.sqlite

# Logs
*.log

# OS
.DS_Store
Thumbs.db
'''
    
    with open(app_path / '.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    # Create README.md
    readme_content = f'''# {app_name}

A Flask application built with the Bivouac Framework.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Initialize the database:
   ```bash
   bivouac init-db
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Development

This application is built using the Bivouac Framework, which provides:

- Modular architecture
- Authentication system
- Role-based permissions
- Multi-tenant support
- CLI tools

For more information, see the [Bivouac Framework documentation](https://github.com/bivouac-framework/bivouac-framework).

## License

This project is licensed under the MIT License.
'''
    
    with open(app_path / 'README.md', 'w') as f:
        f.write(readme_content)
    
    # Create modules directory
    modules_path = app_path / 'modules'
    modules_path.mkdir()
    
    # Create __init__.py in modules directory
    with open(modules_path / '__init__.py', 'w') as f:
        f.write('# Modules package\n')
    
    # Create static and templates directories
    (app_path / 'static').mkdir()
    (app_path / 'templates').mkdir()
    
    # Create basic template
    base_template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ app_name }}{% endblock %}</title>
    {% block styles %}{% endblock %}
</head>
<body>
    <header>
        <h1>{{ app_name }}</h1>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2024 {{ app_name }}. Built with Bivouac Framework.</p>
    </footer>
    
    {% block scripts %}{% endblock %}
</body>
</html>
'''
    
    with open(app_path / 'templates' / 'base.html', 'w') as f:
        f.write(base_template_content)
    
    # Create index template
    index_template_content = '''{% extends "base.html" %}

{% block title %}{{ app_name }} - Home{% endblock %}

{% block content %}
<div class="container">
    <h2>Welcome to {{ app_name }}</h2>
    <p>This is a Bivouac Framework application.</p>
    
    <div class="features">
        <h3>Features</h3>
        <ul>
            <li>Modular architecture</li>
            <li>Authentication system</li>
            <li>Role-based permissions</li>
            <li>Multi-tenant support</li>
        </ul>
    </div>
</div>
{% endblock %}
'''
    
    with open(app_path / 'templates' / 'index.html', 'w') as f:
        f.write(index_template_content)


if __name__ == '__main__':
    main() 