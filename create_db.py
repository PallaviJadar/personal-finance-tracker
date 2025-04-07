from app import app
from extensions import db
from transaction.models import Transaction

with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")
