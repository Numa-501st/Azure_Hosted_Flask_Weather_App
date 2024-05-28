# init_db.py
from app import db, app

# Create a context for the application
with app.app_context():
    # Create all tables defined in the models
    db.create_all()

print("Database tables created successfully.")

