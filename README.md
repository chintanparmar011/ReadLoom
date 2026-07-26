This is Ebook web application

## Setup Instructions

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your database credentials.
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

### Database Configuration
- This project uses PostgreSQL.
- Set your database details in a `.env` file (copy from `.env.example`).
- Do not commit `.env` to the repository.

## Deploy on Render

This project includes a `render.yaml` blueprint.

1. Push this repository to GitHub.
2. In Render, click **New +** -> **Blueprint** and select your repo.
3. Render will create:
	- A web service named `readloom`
	- A PostgreSQL database named `readloom-db`
4. The build command runs:
	- `pip install -r requirements.txt`
	- `python manage.py collectstatic --noinput`
	- `python manage.py migrate`
5. The start command runs:
	- `gunicorn readloom.wsgi:application --bind 0.0.0.0:$PORT`

Set these environment variables if needed:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL` (auto-wired by `render.yaml`)
