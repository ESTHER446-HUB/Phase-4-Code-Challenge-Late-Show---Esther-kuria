# Late Show API

This is my Flask API project for managing episodes, guests, and appearances on a late-night talk show. I built this as part of my Phase 4 code challenge.

## What it does

- Keep track of episodes with their air dates and episode numbers
- Manage guest information including names and occupations
- Record guest appearances on episodes with ratings from 1-5
- Provide REST API endpoints for all operations

## Getting started

### Installation

First, install the required packages:

```bash
pipenv install
```

Or if you prefer pip:

```bash
pip install -r requirements.txt
```

### Database setup

Run the seed file to create and populate the database:

```bash
pipenv run python seed.py
```

### Running the app

Start the Flask server:

```bash
pipenv run python app.py
```

The API runs on `http://localhost:5555`

## How the database works

I designed three main models:

**Episode**
- id (primary key)
- date (when it aired)
- number (episode number)
- Connected to guests through appearances

**Guest** 
- id (primary key)
- name (guest's full name)
- occupation (what they do for work)
- Connected to episodes through appearances

**Appearance**
- id (primary key) 
- rating (1-5 scale, validated)
- episode_id (links to episode)
- guest_id (links to guest)
- This creates the many-to-many relationship between episodes and guests

I added validation so ratings must be between 1 and 5, and set up cascade deletes so removing an episode or guest also removes their appearances.

## API endpoints I built

### GET /episodes
Gets all episodes in the database.

Returns:
```json
[
  {
    "id": 1,
    "date": "1/11/99", 
    "number": 1
  }
]
```

### GET /episodes/:id
Gets one episode with all its guest appearances.

Success response:
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      },
      "guest_id": 1,
      "id": 1,
      "rating": 4
    }
  ]
}
```

If episode doesn't exist:
```json
{
  "error": "Episode not found"
}
```

### GET /guests
Gets all guests.

Returns:
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
]
```

### POST /appearances
Creates a new guest appearance on an episode.

Send this data:
```json
{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 2
}
```

Success response:
```json
{
  "id": 4,
  "rating": 5,
  "guest_id": 2,
  "episode_id": 1,
  "episode": {
    "date": "1/11/99",
    "id": 1,
    "number": 1
  },
  "guest": {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
}
```

If validation fails:
```json
{
  "errors": ["Rating must be between 1 and 5"]
}
```

### DELETE /episodes/:id
Deletes an episode and all its appearances.

## Testing

I've included a Postman collection (`lateshow-api.postman_collection.json`) that you can import to test all the endpoints. Just import it into Postman and run the requests.

## Project structure

```
├── app.py                    # Main Flask app with models and routes
├── seed.py                   # Database setup and sample data
├── requirements.txt          # Python dependencies
├── Pipfile                   # Pipenv config
├── lateshow-api.postman_collection.json  # API tests
└── README.md                 # This file
```

## Tech stack

- Flask for the web framework
- SQLAlchemy for database operations
- SQLite for the database
- Flask-Migrate for database migrations

**Author:** Esther Kuria

## Notes

This was a fun project to work on! The trickiest part was getting the many-to-many relationship right between episodes and guests through the appearances table. I made sure to include proper error handling and validation as required.