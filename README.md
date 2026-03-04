# Beanstalk - Freelance Marketplace

A premium, two-sided marketplace built with **Django REST Framework** (Backend) and **Vanilla HTML/JS + Tailwind CSS** (Frontend).

## Prerequisites
- Python 3.x
- Node or a simple HTTP Server (e.g. VS Code Live Server) to serve the frontend.

## Quick Start (Local Development)

### 1. Start the Backend
```bash
cd backend
# Activate the virtual environment if you wish, or just run using the python executable:
venv\Scripts\activate
# If running for the very first time (migrations are already run!):
# python manage.py makemigrations
# python manage.py migrate

# Start the Django server
python manage.py runserver
```
*The backend will run at `http://127.0.0.1:8000/`*

### 2. Start the Frontend
Since the frontend uses relative/API paths assuming Vanilla JS and Tailwind CDN, there is no build step required. 
Simply open `index.html` in your browser, or better yet, use a local server:

```bash
cd frontend
python -m http.server 3000
```
*The frontend will run at `http://127.0.0.1:3000/`*

### 3. Usage Flow
- Go to the frontend URL.
- **Sign Up** as a **Job Provider** to post jobs.
- Post a dummy job from the Provider Dashboard.
- **Sign Up** as a **Freelancer** in a new incognito window (or log out).
- Browse the Job Board on the Freelancer Dashboard and apply!

## Deployment Guide (Production)

The User interface is standard HTML, Javascript, and Tailwind. Real deployment involves:
1. **Frontend Hosting**: Deploy the `frontend/` directory to **Vercel**, **Netlify**, or **GitHub Pages**.
2. **Backend Hosting**: 
    - Deploy the Django App to **Render**, **Railway**, or **Heroku**.
    - Configure the `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` environment variables on the cloud platform to automatically connect to a managed **PostgreSQL** database instead of local SQLite.
    - Set `CORS_ALLOW_ALL_ORIGINS = False` in `settings.py` and strictly allow your frontend's deployed URL.
