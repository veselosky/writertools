# Writer Tools

A Django project for my writer tools website.

## Roadmap

## Development

Check out the code and run:

`python ./manage.py devsetup`

This will create a virtual environment and install requirements. Note that the version
of Python used to run `devsetup` will be the one used in your virtual environment.

## Dependency Management

This project includes pip-tools for dependency management. There are two requirements
files: requirements.in provides the acceptable ranges of packages to install in a
production environment (or any other environment); requirements-dev.in provides packages
to install in development environments. Both of these have corresponding "pin" files:
requirements.txt and requirements-dev.txt.

To add a new dependency, add it to the correct .in file, and then run manage.py pipsync
to regenerate the pin files and synchronize your current virtual environment with the
new pin files.

Any arguments passed to manage.py pipsync will be passed through to the underlying
pip-compile command. For example, to bump to the latest Django patch release use
manage.py pipsync --upgrade-package django. See the pip-tools docs for complete details.

The pin files are not included in the template repository, but will be generated when
you run manage.py devsetup. This ensures you will get the latest version of Django and
related packages when starting a new project.
