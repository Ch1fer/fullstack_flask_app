from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}
    
class QrCode(db.Model):
    __tablename__ = 'qrcodes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), unique=True, nullable=False)
    qr_name = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.String(150), unique=True, nullable=False)

    def json(self):
        return {
                'id': self.id,
                'author': self.author,
                'qr_name': self.qr_name,
                'date': self.date,
                'text': self.text
            }


db.create_all()


# create a test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'The server is running'})


# create a user
@app.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id' : new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }), 201

    except Exception as e:
        return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)


# get all users
@app.route('/api/flask/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)
    

# get a user by id
@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)


# update a user by id
@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)
    

# delete a user by id
@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)



# create a qrcode
@app.route('api/flask/qrcodes', methods=['POST'])
def create_qrcode():

    try:
        data = request.get_json()
        new_qrcode = QrCode(author=data['author'], qr_name=data['qr_name'], date=data['date'], text=data['text'])
        db.session.add(new_qrcode)
        db.session.commit()

        return jsonify({
            'id': new_qrcode.id,
            'author': new_qrcode.author,
            'qr_name': new_qrcode.qr_name,
            'date': new_qrcode.date,
            'text': new_qrcode.text
        }), 201
    except Exception as e:
        return make_response(jsonify({'message': 'error creating qr_code', 'error': str(e)}), 500)
    
# get all qr codes
@app.route('api/flask/qrcodes', methods=['GET'])
def get_qrcodes():
    try:
        qrcodes = QrCode.query.all()
        qrcodes_data = [
            {
            'id': qrcode.id,
            'author': qrcode.author,
            'qr_name': qrcode.qr_name,
            'date': qrcode.date,
            'text': qrcode.text} for qrcode in qrcodes]

        return jsonify(qrcodes_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting qr codes', 'error': str(e)}), 500)

# get a qr_code by id
@app.route('api/flask/qrcodes/<id>', methods=['GET'])
def get_qrcode(id):

    try:
        qrcode = QrCode.query.filter_by(id=id).first()
        if qrcode:
            return make_response(jsonify({'qrcode': qrcode.json()}), 200)
        return make_response(jsonify({'message': 'qrcode not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting qrcode', 'error': str(e)}), 500)
    
# update qr code
@app.route('api/flask/qrcodes/<id>', methods=['PUT'])
def update_qrcode(id):
    try:
        qrcode =  QrCode.query.filter_by(id=id).first()
        if qrcode:
            data = request.get_json()
            qrcode.author = data['author']
            qrcode.qr_name = data['qr_name']
            qrcode.date = data['date']
            qrcode.text = data['text']
            db.session.commit()
            return make_response(jsonify({'message': 'qr code updated'}), 200)
        return make_response(jsonify({'message': 'qr code not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating qr code', 'error': str(e)}), 500)


# delete a qr code by id
@app.route('api/flask/qrcodes/<id>', methods=['DELETE'])
def delete_qrcode(id):
    try:
        qrcode = QrCode.query.filter_by(id=id).first()
        if qrcode:
            db.session.delete(qrcode)
            db.session.commit()
            return make_response(jsonify({'message': 'qr code deleted'}), 200)
        return make_response(jsonify({'message': 'qr code not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting qrcode', 'error': str(e)}), 500)