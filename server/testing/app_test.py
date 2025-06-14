from datetime import datetime
from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

    with app.app_context():
        # Clear old test data
        m = Message.query.filter(
            Message.body == "Hello 👋"
        ).filter(Message.username == "Liza")

        for message in m:
            db.session.delete(message)

        db.session.commit()

    def test_has_correct_columns(self):
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert type(hello_from_liza.created_at) == datetime

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            assert response.status_code == 200
            assert isinstance(response.json, list)

            for message in response.json:
                assert message['id'] in [record.id for record in records]
                assert message['body'] in [record.body for record in records]

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():
            app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert h

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert response.json["body"] == "Hello 👋"
            assert response.json["username"] == "Liza"

            h = Message.query.filter_by(body="Hello 👋").first()
            assert h

            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        '''updates the body of a message in the database.'''
        with app.app_context():
            message = Message(body="Original body", username="TestUser")
            db.session.add(message)
            db.session.commit()

            id = message.id
            original_body = message.body

            app.test_client().patch(
                f'/messages/{id}',
                json={"body": "Updated body 👋"}
            )

            updated = db.session.get(Message, id)
            assert updated.body == "Updated body 👋"

            # Clean up
            db.session.delete(updated)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        '''returns data for the updated message as JSON.'''
        with app.app_context():
            message = Message(body="Original body", username="TestUser")
            db.session.add(message)
            db.session.commit()

            id = message.id

            response = app.test_client().patch(
                f'/messages/{id}',
                json={"body": "Updated body 👋"}
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert response.json["body"] == "Updated body 👋"

            db.session.delete(db.session.get(Message, id))
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert not h
