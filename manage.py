#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks, with project extras.

The `devsetup` command is not a proper management command. It is meant to be used
before Django is installed to bootstrap the Django environment.

If you want to override the default arguments to any Django commands, you can intercept
the command in the execute section at the bottom, calling `django_command` with your
special arguments. Alternatively, you could implement the command in the project to shadow
the Django command.
"""
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path


def devsetup(rebuild=False):
    """Set up an environment for local development."""
    this = Path(sys.argv[0]).resolve(strict=True)
    venvdir = this.parent / "venv"
    if rebuild:
        # Nuke the venv and recreate
        print("Rebuilding virtualenv")
        venv.create(str(venvdir), clear=True, with_pip=True, prompt="writertools")
    elif not venvdir.exists():
        print("Creating virtualenv")
        venv.create(str(venvdir), with_pip=True, prompt="writertools")

    python = venvdir / "bin" / "python"

    # Upgrade pip in virtualenv. Need pip >= 21.3.1 for -e with pyproject.toml
    # 3.8's pip won't cut it.
    print("Upgrading virtualenv to latest pip")
    subprocess.run([python, "-m", "pip", "install", "-q", "-U", "pip", "wheel"])

    print("Installing requirements. May take a bit. Grab a coffee.")
    subprocess.run(
        [python, "-m", "pip", "install", "-q", "-r", "etc/pip/requirements-dev.txt"]
    )

    # FIXME HACK support editable genericsite
    print("HACK Installing editable django-genericsite for development only.")
    subprocess.run(
        [
            python,
            "-m",
            "pip",
            "install",
            "-q",
            "-e",
            "../django-genericsite/",
        ]
    )

    # If no .env, copy example.env to .env
    dotenv = this.parent / ".env"
    if not dotenv.exists():
        print("Creating local .env file")
        shutil.copy(this.parent.joinpath("example.env"), dotenv)

    # Create the dev database
    print("Applying database migrations")
    subprocess.run([python, "manage.py", "migrate"])

    print("Dev setup complete. Activate your virtualenv with: . venv/bin/activate")


def upgrade_requirements():
    this = Path(sys.argv[0]).resolve(strict=True)
    venvdir = this.parent / "venv"
    python = venvdir / "bin" / "python"
    env = os.environ.copy()
    env.setdefault("CUSTOM_COMPILE_COMMAND", "./manage.py upgrade_requirements")
    subprocess.run(
        [
            python,
            "-m",
            "piptools",
            "compile",
            "--upgrade",
            "--generate-hashes",
            "--reuse-hashes",
            "--no-emit-index-url",
            "--output-file=requirements.txt",
            "etc/pip/requirements.in",
        ],
        env=env,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        [
            python,
            "-m",
            "piptools",
            "compile",
            "--upgrade",
            "--generate-hashes",
            "--reuse-hashes",
            "--no-emit-index-url",
            "--output-file=requirements-test.txt",
            "etc/pip/requirements-test.in",
        ],
        env=env,
        capture_output=True,
        check=True,
    )


def django_command(args=None):
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "writertools.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    if sys.argv[1] == "devsetup":
        rebuild = False
        if len(sys.argv) > 2 and sys.argv[2] in ["--rebuild", "-r"]:
            rebuild = True
        devsetup(rebuild=rebuild)
    elif sys.argv[1] == "upgrade_requirements":
        upgrade_requirements()
    else:
        django_command()
