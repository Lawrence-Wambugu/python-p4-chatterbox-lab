# server/seed.py
from app import app
from models import db, Message

with app.app_context():
    Message.query.delete()

    m1 = Message(body="Hello 👋", username="Liza")
    m2 = Message(body="Hey there!", username="Ian")

    db.session.add_all([m1, m2])
    db.session.commit()
