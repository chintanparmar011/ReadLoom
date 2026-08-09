# ReadLoom

ReadLoom is a Django web app where people can read books online, and authors can upload their own books for others to read.

## What it does

- Users can sign up, browse books, and read them right in the browser
- Authors can upload a book (PDF + cover image) and track how it's doing
- Reading progress is saved automatically as you read
- Books can be rated, and there's a leaderboard for authors
- Books are organized by category (fiction, science, philosophy, etc.)

## Built with

- Django 6.0
- PostgreSQL (hosted on Neon)
- Cloudinary (for storing PDFs, cover images and Badges)
- WhiteNoise (for serving static files)
- Render (for hosting)

## Getting it running locally

1. Clone the repo
   ```bash
   git clone https://github.com/chintanparmar011/ReadLoom
   cd ReadLoom
   ```

2. Create a virtual environment and activate it
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

3. Install the requirements
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your own values
   ```bash
   cp .env.example .env
   ```
   You'll need a Postgres database and a free Cloudinary account for this to work.

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Collect static files
   ```bash
   python manage.py collectstatic --no-input
   ```

7. Run the server
   ```bash
   python manage.py runserver
   ```

That's it — the app should be running at `127.0.0.1:8000`.

## A few things worth knowing

- **Database**: This uses PostgreSQL. Locally you can point it at any Postgres instance, but in production it runs on Neon. Connection details come from the `.env` file, not hardcoded anywhere.
- **File uploads**: PDFs and cover images don't get saved to the local `media/` folder — they go straight to Cloudinary. This matters because most free hosting platforms wipe local files on every redeploy, so storing them locally would lose everyone's uploaded books. Free tier caps PDFs at 10MB each.
- **Static files**: CSS/JS get collected into a `staticfiles/` folder and served through WhiteNoise, with compression and cache-busting filenames enabled for production.
- **Don't commit your `.env`** — it's already ignored in `.gitignore`, but worth double-checking before you push.

## Deploying

This is set up to deploy on Render:
- Build command: `./build.sh`
- Start command: `gunicorn readloom.wsgi:application`
- All the environment variables from `.env` need to be added in Render's dashboard too, plus `ALLOWED_HOSTS` set to whatever your live Render URL ends up being.

One thing to know about Render's free tier — the app goes to sleep after about 15 minutes of no traffic, and takes 30-60 seconds to wake back up on the next visit. Fine for a demo, not great for real users yet.

## Project layout

```
ReadLoom/
├── authentication/   → login, signup, custom user model
├── books/            → everything book-related: upload, reading, ratings
├── shelves/          → user bookshelves
├── static/           → source CSS/JS files
├── templates/        → HTML templates
├── build.sh          → used by Render to build the app
└── readloom/         → main project settings
```
