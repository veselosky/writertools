# writertools

A Django project for my writer tools website.

## Development

After checking out the code, setup your dev environment:

```sh
python3.8 -m venv --prompt writertools venv
. venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
-e .env || cp example.env .env
python manage.py migrate
```
