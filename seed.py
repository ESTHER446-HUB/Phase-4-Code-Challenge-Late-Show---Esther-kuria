from app import app, db, Episode, Guest, Appearance

def seed_data():
    with app.app_context():
        # Drop and recreate tables
        db.drop_all()
        db.create_all()
        
        # Add some episodes
        episode1 = Episode(date="1/11/99", number=1)
        episode2 = Episode(date="1/12/99", number=2)
        episode3 = Episode(date="1/13/99", number=3)
        
        # Add some guests
        guest1 = Guest(name="Michael J. Fox", occupation="actor")
        guest2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        guest3 = Guest(name="Tracey Ullman", occupation="television actress")
        
        # Save episodes and guests first
        db.session.add_all([episode1, episode2, episode3])
        db.session.add_all([guest1, guest2, guest3])
        db.session.commit()
        
        # Now add appearances
        appearance1 = Appearance(rating=4, episode_id=1, guest_id=1)
        appearance2 = Appearance(rating=5, episode_id=2, guest_id=2)
        appearance3 = Appearance(rating=3, episode_id=3, guest_id=3)
        
        db.session.add_all([appearance1, appearance2, appearance3])
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()