# OceanCrow_Scaffolder - Created by Sheldon Kenny Salmon (@OceanCrowtt)
# A Python project scaffolding tool to kickstart your coding journey!
# Follow @OceanCrowtt on X for updates and support.

import click
import os
import sys
from pathlib import Path
import shutil
import logging
import subprocess
import platform
from time import sleep

# Configure logging with a clean format
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Helper function to print messages with bold styling
def cprint(message, bold=False):
    """Print messages with optional bold styling using asterisks."""
    if bold:
        print(f"**{message}**")
    else:
        print(message)

# Helper function to highlight specific words with quotes
def cprint_with_highlighted_words(message, words_to_highlight, bold=False):
    """Print a message with specific words highlighted using quotes."""
    for word in words_to_highlight:
        message = message.replace(word, f"'{word}'")
    if bold:
        print(f"**{message}**")
    else:
        print(message)

# Helper function to display a wave animation
def show_wave_animation():
    """Display a short wave animation for the CLI welcome."""
    waves = ["~ ", " ~ ", " ~"]
    for _ in range(2):
        for wave in waves:
            print(f"\r{wave} OceanCrow_Scaffolder Loading...", end="")
            sleep(0.2)
    print("\r" + " " * 40, end="\r") # Clear the line

# Helper function to display a simple progress bar
def show_progress(steps=5, delay=0.2):
    """Display a simple ASCII progress bar."""
    cprint("Initializing...", bold=True)
    for i in range(steps):
        print(f"\r[{'█' * (i + 1)}{' ' * (steps - i - 1)}]", end="")
        sleep(delay)
    print("\r" + " " * (steps + 2), end="\r") # Clear the line

# Helper function to display a spinner for tasks
def show_spinner(task_name):
    """Display a spinning cursor for a task."""
    cprint(f"{task_name}...")
    spinners = ["|", "/", "-", "\\"]
    for _ in range(4):
        for spinner in spinners:
            print(f"\r{spinner} Working...", end="")
            sleep(0.1)
    print("\r" + " " * 20, end="\r") # Clear the line

# Helper function to display a success banner
def show_success_banner(project_name):
    """Display a formatted success banner."""
    border = "=" * (len(project_name) + 20)
    cprint(f"+{border}+", bold=True)
    cprint(f"| Project {project_name} is ready! Happy coding! |", bold=True)
    cprint(f"+{border}+", bold=True)

# Helper function to get OC_Scaffold root directory
def get_oc_scaffold_root():
    """Return the OC_Scaffold root directory in the user's home directory."""
    return Path.home() / 'OC_Scaffold'

# Helper function to check if Scripts/bin is in PATH
def check_scripts_in_path():
    """Check if Scripts/bin directory is in PATH."""
    scripts_path = Path(sys.prefix) / ('Scripts' if platform.system() == 'Windows' else 'bin')
    path_env = os.environ.get('PATH', '').split(os.pathsep)
    return str(scripts_path) in path_env

# Helper function to get template directory
def get_template_dir():
    """Return the template directory within the package."""
    return Path(__file__).parent / 'templates'

# Helper function to create project structure
def create_project_structure(project_path):
    """Create the directory structure for your awesome project."""
    for folder in ['src', 'tests', 'docs', 'private']:
        (project_path / folder).mkdir(exist_ok=True)
        cprint(f"Created folder: {folder}")

# Helper function to create project files
def create_project_files(project_path, project_name, project_type):
    """Create project files based on the specified type with dynamic naming."""
    src_dir = project_path / 'src'
    template_dir = get_template_dir()
    template_files = {
        'basic': ('main.py', 'main.py'),
        'flask': ('app.py', 'app.py'),
        'datascience': ('notebook.py', 'notebook.py')
    }
    requirements_files = {
        'flask': 'requirements_flask.txt',
        'datascience': 'requirements_datascience.txt'
    }

    # Copy and process template file
    template_file, target_file = template_files.get(project_type.lower(), ('main.py', 'main.py'))
    template_path = template_dir / template_file
    target_path = src_dir / target_file
    if template_path.exists():
        with open(template_path, 'r') as f:
            content = f.read()
        content = content.replace("{project_name}", project_name)
        with open(target_path, 'w') as f:
            f.write(content)
        cprint(f"Copied {project_type} template: {target_file}")
    else:
        # Fallback: create default file
        default_contents = {
            'basic': (
                f"# {project_name} - Main Script\n"
                f"# Created by OceanCrow_Scaffolder (@OceanCrowtt)\n\n"
                f"def main():\n"
                f" print('Hello from {project_name}!')\n\n"
                f"if __name__ == '__main__':\n"
                f" main()"
            ),
            'flask': (
                f"# {project_name} - Flask Web App\n"
                f"# Created by OceanCrow_Scaffolder (@OceanCrowtt)\n\n"
                f"from flask import Flask\n\n"
                f"app = Flask(__name__)\n\n"
                f"@app.route('/')\n"
                f"def hello():\n"
                f" return 'Hello from {project_name}!'\n\n"
                f"if __name__ == '__main__':\n"
                f" app.run(debug=True)"
            ),
            'datascience': (
                f"# {project_name} - Data Science Notebook\n"
                f"# Created by OceanCrow_Scaffolder (@OceanCrowtt)\n\n"
                f"import pandas as pd\n"
                f"import numpy as np\n\n"
                f"# Example data analysis\n"
                f"data = pd.DataFrame({{'column1': np.random.randn(100)}})\n"
                f"print(data.describe())"
            )
        }
        content = default_contents.get(project_type.lower(), default_contents['basic'])
        content = content.replace("{project_name}", project_name)
        with open(target_path, 'w') as f:
            f.write(content)
        cprint(f"Created default {project_type} template: {target_file}")

    # Copy requirements file if applicable
    if project_type.lower() in requirements_files:
        req_file = requirements_files[project_type.lower()]
        if (template_dir / req_file).exists():
            shutil.copy(template_dir / req_file, project_path / 'requirements.txt')
        else:
            with open(project_path / 'requirements.txt', 'w') as f:
                f.write("flask>=2.0.0" if project_type.lower() == 'flask' else "pandas>=2.0.0\nnumpy>=1.26.0\nmatplotlib>=3.8.0\nscikit-learn>=1.4.0")
        cprint("Created requirements.txt")

# Helper function to create start_project script
def create_start_project_script(project_path, project_name, project_type):
    """Create a start_project script to launch your project."""
    start_file = 'start_project.bat' if platform.system() == 'Windows' else 'start_project.sh'
    main_file = 'app.py' if project_type.lower() == 'flask' else 'notebook.py' if project_type.lower() == 'datascience' else 'main.py'
    script_content = (
        f"@echo off\n"
        f"echo OceanCrow_Scaffolder: Activating {project_name}...\n"
        f"cd /d {project_path}\n"
        f"call env\\Scripts\\activate\n"
        f"echo Run: python src\\{main_file} to start your project\n"
        f"cmd /k"
        if platform.system() == 'Windows' else
        f"#!/bin/bash\n"
        f"echo 'OceanCrow_Scaffolder: Activating {project_name}...'\n"
        f"cd {project_path}\n"
        f"source env/bin/activate\n"
        f"echo 'Run: python3 src/{main_file} to start your project'\n"
        f"bash"
    )
    with open(project_path / start_file, 'w') as f:
        f.write(script_content)
    if platform.system() != 'Windows':
        os.chmod(project_path / start_file, 0o755)
    cprint("Created start_project script")

# Helper function to create .gitignore
def create_gitignore(project_path):
    """Create a .gitignore file for the project."""
    gitignore_content = (
        "# OceanCrow_Scaffolder .gitignore\n"
        "# Virtual environment\n"
        "env/\n"
        "venv/\n\n"
        "# Python cache\n"
        "__pycache__/\n"
        "*.pyc\n"
        "*.pyo\n"
        "*.pyd\n"
        "*.egg-info/\n\n"
        "# Sensitive files\n"
        "private/\n"
        ".env\n"
        "config.py\n"
        "secrets.json\n"
        "*.key\n"
        "*.pem\n"
        "*.pwd\n\n"
        "# Build files\n"
        "dist/\n"
        "build/\n"
        "*.whl\n"
        "*.tar.gz\n\n"
        "# IDE files\n"
        ".vscode/\n"
        ".idea/\n"
        "*.sublime-project\n\n"
        "# OS-specific\n"
        ".DS_Store\n"
        "Thumbs.db\n"
        "desktop.ini\n\n"
        "# Logs and databases\n"
        "*.log\n"
        "*.sqlite3\n"
        "*.db\n\n"
        "# Testing\n"
        ".pytest_cache/\n"
        "coverage/\n"
        "*.cov\n\n"
        "# Miscellaneous\n"
        "*.bak\n"
        "*.swp\n"
        "*.tmp\n"
    )
    with open(project_path / '.gitignore', 'w') as f:
        f.write(gitignore_content)
    cprint("Created .gitignore")

# Helper function to create commands.txt
def create_commands_txt(project_path, project_name, project_type):
    """Create a commands.txt file with project-specific commands."""
    python_cmd = 'python' if platform.system() == 'Windows' else 'python3'
    activate_cmd = f"{project_path}\\env\\Scripts\\activate" if platform.system() == 'Windows' else f"source {project_path}/env/bin/activate"
    start_script = f"{project_path}{os.sep}start_project.{'bat' if platform.system() == 'Windows' else 'sh'}"
    main_file = 'app.py' if project_type.lower() == 'flask' else 'notebook.py' if project_type.lower() == 'datascience' else 'main.py'
    commands_content = (
        f"# OceanCrow_Scaffolder Commands for {project_name}\n"
        f"# Created by Sheldon Kenny Salmon (@OceanCrowtt)\n"
        f"# -----------------------------------------------\n\n"
        f"## Quick Start\n"
        f"Double-click {start_script} to activate the virtual environment\n"
        f"OR run:\n"
        f" {activate_cmd} # {'Windows' if platform.system() == 'Windows' else 'macOS/Linux'}\n"
        f" deactivate # Exit virtual environment (or close the terminal)\n\n"
        f"## Software Verification\n"
        f" {python_cmd} --version\n"
        f" {python_cmd} -c \"import platform; print(platform.architecture())\"\n"
        f" git --version\n"
        f" pip --version\n"
        f" pip list\n\n"
        f"## Scaffold Commands\n"
        f" scaffold create {project_name} --type {project_type}\n"
        f" scaffold update {project_name}\n"
        f" scaffold --help\n\n"
        f"## Dependency Management\n"
        f" pip install -r requirements.txt\n"
        f" pip freeze > requirements.txt\n\n"
        f"## Git Workflow\n"
        f" git config --global user.name \"Your Name\"\n"
        f" git config --global user.email \"your.email@example.com\"\n"
        f" git init\n"
        f" git add .\n"
        f" git commit -m \"Initial commit\"\n"
        f" git remote add origin https://github.com/yourusername/{project_name}.git\n"
        f" git push -u origin main\n\n"
        f"## Testing and Running\n"
        f" pytest tests/\n"
        f" {python_cmd} {project_path}{os.sep}src{os.sep}{main_file}\n"
        f" flake8 {project_path}{os.sep}src > {project_path}{os.sep}docs{os.sep}code_quality.txt\n\n"
        f"## Troubleshooting\n"
        f" {'icacls C:\\ProgramData\\Git\\config /grant Users:F' if platform.system() == 'Windows' else '# No equivalent needed for macOS/Linux'}\n"
        f" {python_cmd} -m pip install package_name\n"
        f" where python\n"
        f" where git\n\n"
        f"## Contact\n"
        f"For support or custom coding, DM @OceanCrowtt on X\n"
        f"Love this tool? Follow @OceanCrowtt for updates!\n"
    )
    with open(project_path / 'commands.txt', 'w') as f:
        f.write(commands_content)
    cprint("Created commands.txt")

# Helper function to create documentation files
def create_docs(project_path, project_name, project_type):
    """Create documentation files (README, contribution, LICENSE) with style."""
    python_cmd = 'python' if platform.system() == 'Windows' else 'python3'
    start_script = f"{project_path}{os.sep}start_project.{'bat' if platform.system() == 'Windows' else 'sh'}"
    activate_cmd = f"{project_path}\\env\\Scripts\\activate" if platform.system() == 'Windows' else f"source {project_path}/env/bin/activate"
    main_file = 'app.py' if project_type.lower() == 'flask' else 'notebook.py' if project_type.lower() == 'datascience' else 'main.py'
    
    with open(project_path / 'docs' / 'README.md', 'w') as f:
        f.write(
            f"# {project_name}\n\n"
            f"Welcome to your {project_type} project, crafted by OceanCrow_Scaffolder!\n"
            f"Created by Sheldon Kenny Salmon (@OceanCrowtt)\n\n"
            f"## Quick Start\n"
            f"1. Activate: Double-click `{start_script}`\n"
            f" OR run: `{activate_cmd}`\n"
            f"2. Install: `pip install -r requirements.txt`\n"
            f"3. Run: `{python_cmd} src/{main_file}`\n\n"
            f"## Testing\n"
            f"Run `pytest tests/` to execute tests.\n\n"
            f"## Project Structure\n"
            f"- `src/`: Your {project_type} source code\n"
            f"- `tests/`: Unit tests\n"
            f"- `docs/`: Documentation (you're here!)\n"
            f"- `private/`: Sensitive files\n"
            f"- `env/`: Virtual environment\n\n"
            f"## Contact\n"
            f"DM @OceanCrowtt on X for support or custom coding.\n"
            f"Follow @OceanCrowtt to stay updated!\n"
        )
    
    with open(project_path / 'docs' / 'contribution.md', 'w') as f:
        f.write(
            f"# Contribution Guidelines for {project_name}\n\n"
            f"Want to make {project_name} even better? Here's how:\n\n"
            f"1. Fork the repository\n"
            f"2. Create a branch: `git checkout -b feature/your-feature`\n"
            f"3. Commit changes: `git commit -m 'Add your feature'`\n"
            f"4. Push: `git push origin feature/your-feature`\n"
            f"5. Submit a pull request\n\n"
            f"Thanks for contributing to {project_name}!\n"
            f"Created by Sheldon Kenny Salmon (@OceanCrowtt)\n"
        )
    
    with open(project_path / 'docs' / 'LICENSE', 'w') as f:
        f.write(
            f"# MIT License\n\n"
            f"Copyright (c) 2025 Sheldon Kenny Salmon (@OceanCrowtt)\n\n"
            f"Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            f"of this software and associated documentation files (the \"Software\"), to deal\n"
            f"in the Software without restriction, including without limitation the rights\n"
            f"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            f"copies of the Software, and to permit persons to whom the Software is\n"
            f"furnished to do so, subject to the following conditions:\n\n"
            f"The above copyright notice and this permission notice shall be included in all\n"
            f"copies or substantial portions of the Software.\n\n"
            f"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            f"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            f"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            f"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            f"LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            f"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            f"SOFTWARE.\n"
        )
    cprint("Created documentation files")

# CLI group with a clean style
@click.group()
def cli():
    """OceanCrow_Scaffolder CLI
    A tool to scaffold Python projects by Sheldon Kenny Salmon (@OceanCrowtt)."""
    show_wave_animation()
    cprint("Welcome to OceanCrow_Scaffolder! Let's create something awesome!", bold=True)

# Command: version
@cli.command()
def version():
    """Display the version of OceanCrow_Scaffolder."""
    cprint_with_highlighted_words(
        "OceanCrow_Scaffolder v0.1.0 by Sheldon Kenny Salmon (@OceanCrowtt)",
        ["OceanCrow_Scaffolder", "v0.1.0"],
        bold=True
    )

# Command: create
@cli.command()
@click.argument('project_name')
@click.option('--type', default='basic', type=click.Choice(['basic', 'flask', 'datascience'], case_sensitive=False),
              help='Project type: basic, flask, or datascience')
def create(project_name, type):
    """Create a new project with a predefined structure."""
    root_path = get_oc_scaffold_root()
    projects_path = root_path / 'Projects'
    project_path = projects_path / project_name
    python_cmd = 'python' if platform.system() == 'Windows' else 'python3'

    cprint_with_highlighted_words(
        f"Creating project {project_name} ({type})...",
        [project_name, type],
        bold=True
    )
    show_progress()

    # Check if Scripts is in PATH
    if not check_scripts_in_path():
        scripts_dir = Path(sys.prefix) / ('Scripts' if platform.system() == 'Windows' else 'bin')
        cprint(f"Warning: {scripts_dir} not in PATH. 'scaffold' may not work.")
        cprint("Fix: Add the Scripts directory to your PATH environment variable.")
        if platform.system() == 'Windows':
            cprint("Press Win + R, type sysdm.cpl, go to Advanced > Environment Variables, edit Path, add:")
            cprint(f" {scripts_dir}")
        else:
            cprint("Edit ~/.bashrc or ~/.zshrc and add:")
            cprint(f" export PATH=\"$PATH:{scripts_dir}\"")
        cprint("Then restart your terminal.")

    # Check for Python and Git
    try:
        subprocess.run([python_cmd, '--version'], check=True, capture_output=True)
        cprint("Python check passed")
    except:
        cprint(f"Error: Python not found. Install from https://python.org/downloads (64-bit).")
        return
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        cprint("Git check passed")
    except:
        cprint(f"Error: Git not found. Install from https://git-scm.com/download.")
        return

    # Initialize OC_Scaffold if it doesn't exist
    if not root_path.exists():
        try:
            root_path.mkdir(parents=True, exist_ok=True)
            for folder in ['Projects', 'Tools', 'Templates', 'Config', 'Packages', 'OceanCrow']:
                (root_path / folder).mkdir()
            cprint(f"Created {root_path} with subfolders")
            
            # Create Packages/README.md
            with open(root_path / 'Packages' / 'README.md', 'w') as f:
                f.write(
                    "# OceanCrow_Scaffolder Prerequisites\n\n"
                    "Get ready to scaffold with these tools:\n\n"
                    "- Python 3.12+: python.org/downloads (64-bit)\n"
                    "- Git: git-scm.com/download\n"
                    "- Microsoft Visual C++ Redistributable (Windows): learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist (x64)\n"
                    "- Optional Tools:\n"
                    " - Notepad++: notepad-plus-plus.org\n"
                    " - 7-Zip: 7-zip.org\n"
                    " - VS Code: code.visualstudio.com\n\n"
                    "Store installers in this folder or download as needed.\n"
                    "Created by Sheldon Kenny Salmon (@OceanCrowtt)"
                )
            
            # Create OceanCrow/README.md
            with open(root_path / 'OceanCrow' / 'README.md', 'w') as f:
                f.write(
                    "# OceanCrow_Scaffolder\n\n"
                    "Created by Sheldon Kenny Salmon (@OceanCrowtt)\n\n"
                    "This tool simplifies Python project setup with a single command.\n"
                    "For installation and usage, see the main README.md at:\n"
                    "https://github.com/OceanCrow/OceanCrow_Scaffolder\n\n"
                    "- Contact: DM @OceanCrowtt on X for support or custom coding\n"
                    "- Support: Love this tool? Follow @OceanCrowtt on X!\n"
                    "Copyright (c) 2025 Sheldon Kenny Salmon"
                )
        except Exception as e:
            logging.error(f"Failed to create {root_path}: {e}")
            cprint("Error initializing OC_Scaffold. Check permissions or disk space.")
            return

    # Check if project exists
    if project_path.exists():
        cprint_with_highlighted_words(
            f"Warning: Project {project_name} exists at {project_path}",
            [project_name, str(project_path)]
        )
        while True:
            overwrite = input(f"Overwrite {project_name}? [y/N]: ").lower()
            if overwrite in ['y', 'yes']:
                try:
                    shutil.rmtree(project_path)
                    cprint_with_highlighted_words(
                        f"Removed existing project {project_name}",
                        [project_name]
                    )
                    break
                except Exception as e:
                    logging.error(f"Failed to remove existing project: {e}")
                    cprint("Error removing existing project")
                    return
            elif overwrite in ['n', 'no', '']:
                cprint("Aborted")
                return
            else:
                cprint("Please enter 'y' or 'n'")

    # Create project structure
    try:
        project_path.mkdir(parents=True, exist_ok=True)
        create_project_structure(project_path)
        cprint_with_highlighted_words(
            f"Created project {project_name} at {project_path}",
            [project_name, str(project_path)],
            bold=True
        )
    except Exception as e:
        logging.error(f"Failed to create project directory: {e}")
        cprint("Error creating project")
        return

    # Create virtual environment
    try:
        show_spinner("Creating virtual environment")
        subprocess.run([sys.executable, '-m', 'venv', str(project_path / 'env')], check=True, capture_output=True)
        cprint("Created virtual environment")
        start_script = f"{project_path}{os.sep}start_project.{'bat' if platform.system() == 'Windows' else 'sh'}"
        cprint_with_highlighted_words(
            f"To start, run: {start_script}",
            [start_script]
        )
        cprint("Or close the terminal to deactivate the virtual environment")
    except Exception as e:
        logging.error(f"Failed to create virtual environment: {e}")
        cprint("Error creating virtual environment. See Packages/README.md")

    # Create project files
    create_project_files(project_path, project_name, type)
    create_start_project_script(project_path, project_name, type)
    create_gitignore(project_path)
    create_commands_txt(project_path, project_name, type)
    create_docs(project_path, project_name, type)

    # Initialize Git repository
    try:
        show_spinner("Initializing Git repository")
        subprocess.run(['git', 'init'], cwd=project_path, check=True, capture_output=True)
        cprint("Initialized Git repository")
    except Exception as e:
        logging.error(f"Failed to initialize Git repository: {e}")
        cprint("Failed to initialize Git repository. Ensure Git is installed")

    # Show success banner and command hints
    show_success_banner(project_name)
    cprint("Next steps:", bold=True)
    cprint_with_highlighted_words(
        " Run scaffold --help for more commands",
        ["scaffold --help"]
    )
    cprint_with_highlighted_words(
        f" Check commands.txt for project-specific tips",
        ["commands.txt"]
    )

# Command: update
@cli.command()
@click.argument('project_name')
def update(project_name):
    """Update an existing project with missing files or dependencies."""
    root_path = get_oc_scaffold_root()
    project_path = root_path / 'Projects' / project_name
    python_cmd = 'python' if platform.system() == 'Windows' else 'python3'

    if not project_path.exists():
        cprint_with_highlighted_words(
            f"Error: Project {project_name} does not exist at {project_path}",
            [project_name, str(project_path)]
        )
        return

    cprint_with_highlighted_words(
        f"Updating project {project_name}...",
        [project_name],
        bold=True
    )
    show_progress()

    # Recreate missing files
    create_project_structure(project_path)
    create_gitignore(project_path)
    create_commands_txt(project_path, project_name, 'basic') # Assume basic type for updates
    create_docs(project_path, project_name, 'basic') # Assume basic type for updates
    cprint_with_highlighted_words(
        f"Project {project_name} updated successfully",
        [project_name],
        bold=True
    )

    # Show command hints
    cprint("Next steps:", bold=True)
    cprint_with_highlighted_words(
        " Run scaffold --help for more commands",
        ["scaffold --help"]
    )
    cprint_with_highlighted_words(
        f" Check commands.txt for project-specific tips",
        ["commands.txt"]
    )

if __name__ == '__main__':
    cli()