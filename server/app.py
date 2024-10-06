from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        message_dict = [message.to_dict() for message in messages]
        response = make_response(jsonify(message_dict), 200, {"Content-Type": "application/json"})
        return response
    
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    if not data or not data.get('body') or not data.get('username'):
        return make_response(jsonify({"error": "Missing required fields"}))
    
    new_message = Message(
        body = data["body"],
        username = data["username"],
    )
    
    db.session.add(new_message)
    db.session.commit()
        
    new_message_dict = new_message.to_dict()
    response = make_response(new_message_dict, 201, {"Content-Type": "application/json"})
    
    return response
    

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    data = request.get_json()

    if 'body' in data:
        message.body = data['body']

    # for attr in message:
    #     setattr(message, attr, request.form.get(attr))
    # db.session.add(message)
    message.updated_at = datetime.utcnow()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)
    
    message_dict = message.to_dict()
    response = make_response(jsonify(message_dict), 200, {"Content-Type": "application/json"})
    
    return response

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    db.session.delete(message)
    db.session.commit()
    
    response_body = {
        "delete_successful": True,
        "message": "Message deleted."
    }
    
    response = make_response(jsonify(response_body), 200, {"Content-Type": "application/json"})
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)