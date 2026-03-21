# Commerce (Django Auctions)

A Django web application for creating and managing auction listings, built as a project for Harvard's CS50W (Web Programming with Python and JavaScript) course. Users can register, create listings, place bids, comment, manage watchlists, browse categories, and close auctions.

## Features

- User authentication (register, login, logout)
- Create auction listings with title, description, starting bid, image URL, and category
- View active listings and listing details
- Place bids with bid validation
- Add and remove items from watchlist
- Browse listings by category
- Add comments on listings
- Close auctions and automatically assign winner to highest bidder

## Tech Stack

- Python
- Django (project generated with Django 3.x)
- SQLite (`db.sqlite3`)

## Project Structure

```
commerce/
├── auctions/           # Main app (models, views, URLs, templates)
├── commerce/           # Project settings and root URLs
├── manage.py
└── db.sqlite3
```

## Setup

### 1) Clone repository

```bash
git clone https://github.com/Utpal-Kalita/commerce.git
cd commerce
```

### 2) Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install django
```

### 4) Apply migrations

```bash
python manage.py migrate
```

### 5) Run server

```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Useful Commands

Create superuser:

```bash
python manage.py createsuperuser
```

Collect static files (if needed):

```bash
python manage.py collectstatic
```

## Notes

- Uses a custom user model: `auctions.User`
- Default database is SQLite
- Development settings currently have `DEBUG = True`