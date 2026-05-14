# FlavorMap

FlavorMap is a Django-based web application for restaurant discovery and reviews. Users can search and filter restaurants, explore menus, save favorites, and leave 1-5 star reviews.

## Features

- Restaurant listing, detail pages, creation, editing, and deletion
- Filtering by category, price range, location, minimum rating, and photo availability
- Restaurant ratings, written reviews, and replies to reviews
- Menu item and opening hours management
- User registration/login, profile page, and favorites list
- Restaurant owner submission flow with admin approval status
- Photo uploads and a responsive Bootstrap 5 interface

## Tech Stack

- Python 3.10+
- Django 5
- SQLite
- Bootstrap 5
- Pillow

## Installation

```bash
git clone https://github.com/EmreSndkc/flavormap.git
cd flavormap

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
```

## Running the App

```bash
python3 manage.py runserver
```

Application: `http://127.0.0.1:8000/`  
Admin panel: `http://127.0.0.1:8000/admin/`

## Seed Data

To load sample categories, restaurants, menu items, and reviews:

```bash
python3 manage.py shell < seed_data.py
```

> Note: This command may clear and recreate existing sample data.

## Project Structure

```text
flavormap/
├── flavormap/      # Django project settings
├── restaurants/    # Restaurant, review, menu, and user flows
├── templates/      # HTML templates
├── static/         # CSS and JavaScript files
├── media/          # Uploaded restaurant images
├── seed_data.py    # Sample data script
└── manage.py
```
