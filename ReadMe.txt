# Cafe API

A RESTful API built with Python and Flask for managing a database of cafes. The API allows users to retrieve cafe information, filter cafes by amenities, add new cafes, update coffee prices, and delete records.

## Features

- Retrieve all cafes or a random cafe suggestion.
- Search for a cafe by name.
- Filter cafes offering Wi-Fi.
- Add new cafes to the database.
- Update coffee prices.
- Delete cafes by ID.
- Return cafe data in JSON format.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SinceSlicedBread/cafe-api.git
   ```

2. Navigate to the project directory:

   ```bash
   cd cafe-api
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

The API will run locally using Flask's development server.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/suggestion` | Returns a random cafe |
| GET | `/all` | Returns all cafes |
| GET | `/wifi` | Returns cafes with Wi-Fi |
| GET | `/cafe/<name>` | Retrieves a cafe by name |
| GET | `/add` | Adds a new cafe using query parameters |
| PATCH | `/update_price/<cafe_id>?price=<price>` | Updates a cafe's coffee price |
| DELETE | `/delete/<cafe_id>` | Deletes a cafe by ID |

## Database

Cafe information is stored in a SQLite database (`cafes.db`), with details including location, seating, amenities, map and image URLs, and coffee prices.

## Purpose

This project demonstrates REST API development, database integration, CRUD operations, and JSON responses using Python and Flask.