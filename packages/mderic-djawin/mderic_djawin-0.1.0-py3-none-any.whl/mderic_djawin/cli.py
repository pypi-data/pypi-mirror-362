import subprocess
import sys
from pathlib import Path

def run(command, env=None):
    result = subprocess.run(command, shell=True, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)

def create_project(project_name):
    print(f"Creating Django project: {project_name}")
    base_dir = Path.cwd() / project_name
    venv_dir = base_dir / 'venv'

    base_dir.mkdir(exist_ok=True)
    print(f"[+] Created project folder: {base_dir}")

    run(f'python -m venv "{venv_dir}"')
    print(f"[+] Created virtual environment: {venv_dir}")

    pip_executable = venv_dir / 'Scripts' / 'pip.exe'  # For Windows
    run(f'"{pip_executable}" install django')
    print("[+] Installed Django")

    django_admin = venv_dir / 'Scripts' / 'django-admin.exe'
    run(f'"{django_admin}" startproject {project_name} "{base_dir}"')
    print(f"[+] Django project '{project_name}' created at: {base_dir}")

    print("\n[✓] Setup complete. To activate and run server:")
    print(f'cd {project_name}')
    print(f'env\\Scripts\\activate')
    print(f'python manage.py runserver')

def main():
    if len(sys.argv) < 2:
        print("Usage: mderic_djawin <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    create_project(project_name)