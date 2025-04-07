from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)

    # Import routes and register blueprints
    from app.transaction.routes import transaction_bp
    app.register_blueprint(transaction_bp)

    # Create database tables (only on first run)
    with app.app_context():
        from app.transaction.models import Transaction  # fixed this line
        db.create_all()

    return app
