# Late Show API

A Flask API for managing episodes, guests, and appearances on a late-night talk show.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python seed.py
```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### GET /episodes
Returns all episodes.

### GET /episodes/:id
Returns a specific episode with its appearances.

### GET /guests
Returns all guests.

### POST /appearances
Creates a new appearance. Requires JSON body with:
- rating (1-5)
- episode_id
- guest_id

## Models

- **Episode**: Has many guests through appearances
- **Guest**: Has many episodes through appearances  
- **Appearance**: Belongs to episode and guest, has rating validation (1-5)