from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models
class Episode(db.Model):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationship to appearances
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')
    
    def to_dict(self, include_appearances=False):
        episode_dict = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        if include_appearances:
            episode_dict['appearances'] = [appearance.to_dict() for appearance in self.appearances]
        return episode_dict

class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    
    # Relationship to appearances
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id,
            'episode': self.episode.to_dict(),
            'guest': self.guest.to_dict()
        }

# API Routes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    return jsonify(episode.to_dict(include_appearances=True))

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()
        
        # Check if all required fields are present
        if not all(key in data for key in ['rating', 'episode_id', 'guest_id']):
            return jsonify({'errors': ['Missing required fields']}), 400
        
        # Make sure episode and guest exist
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        
        if not episode or not guest:
            return jsonify({'errors': ['Episode or Guest not found']}), 400
        
        new_appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(new_appearance)
        db.session.commit()
        
        return jsonify(new_appearance.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        return jsonify({'errors': ['Failed to create appearance']}), 400

@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    db.session.delete(episode)
    db.session.commit()
    
    return jsonify({'message': 'Episode deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)