# Late Show API

A Flask API for managing episodes, guests, and appearances on a late-night talk show.

## Features

- Manage episodes with dates and numbers
- Track guests with names and occupations
- Record appearances with ratings (1-5)
- Full CRUD operations with proper validations
- RESTful API design

## Setup

1. **Install dependencies:**
```bash
pipenv install
# or
pip install -r requirements.txt
```

2. **Initialize the database:**
```bash
pipenv run python seed.py
```

3. **Run the application:**
```bash
pipenv run python app.py
```

The API will be available at `http://localhost:5000`

## Database Models

### Episode
- `id`: Primary key
- `date`: Episode air date (string)
- `number`: Episode number (integer)
- **Relationships**: Has many guests through appearances

### Guest
- `id`: Primary key
- `name`: Guest name (string)
- `occupation`: Guest occupation (string)
- **Relationships**: Has many episodes through appearances

### Appearance
- `id`: Primary key
- `rating`: Rating from 1-5 (integer, validated)
- `episode_id`: Foreign key to Episode
- `guest_id`: Foreign key to Guest
- **Relationships**: Belongs to episode and guest
- **Validations**: Rating must be between 1 and 5 (inclusive)

## API Endpoints

### GET /episodes
**Description**: Returns all episodes

**Response**:
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
**Description**: Returns a specific episode with its appearances

**Success Response**:
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

**Error Response** (404):
```json
{
  "error": "Episode not found"
}
```

### GET /guests
**Description**: Returns all guests

**Response**:
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
**Description**: Creates a new appearance

**Request Body**:
```json
{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 2
}
```

**Success Response** (201):
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

**Error Response** (400):
```json
{
  "errors": ["Rating must be between 1 and 5"]
}
```

## Testing with Postman

1. Import the provided Postman collection: `lateshow-api.postman_collection.json`
2. Start the Flask application
3. Run the requests in the collection to test all endpoints

## Project Structure

```
├── app.py                              # Main Flask application
├── seed.py                             # Database seeding script
├── requirements.txt                    # Python dependencies
├── Pipfile                            # Pipenv configuration
├── lateshow-api.postman_collection.json # Postman test collection
└── README.md                          # This file
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migrations
- **SQLite**: Database (default)

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the provided Postman collection
5. Submit a pull request