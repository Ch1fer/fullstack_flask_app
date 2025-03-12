from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timezone
from os import environ
import qrcode
import base64
from io import BytesIO


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


def generate_qrcode_base64(qr_data):
    img = qrcode.make(qr_data)

    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")

    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

    return img_base64


class QrCode(db.Model):
    __tablename__ = 'qrcodes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=False)
    qr_name = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    text = db.Column(db.String(150), unique=False, nullable=False)

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



# create a qrcode
@app.route('/api/flask/qrcodes', methods=['POST'])
def create_qrcode():

    try:
        data = request.get_json()
        date_value = data.get('date', None)
        if date_value is not None and not date_value.strip():
            date_value = None

        new_qrcode = QrCode(author=data['author'], qr_name=data['qr_name'], date=date_value, text=data['text'])
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
@app.route('/api/flask/qrcodes', methods=['GET'])
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
@app.route('/api/flask/qrcodes/<id>', methods=['GET'])
def get_qrcode(id):

    try:
        qrcode = QrCode.query.filter_by(id=id).first()
        if qrcode:
            
            qr_code_base64 = generate_qrcode_base64(qrcode.text)

            response_data = {
                'qrcode': qrcode.json(),
                'qrcode_image': qr_code_base64
            }

            return make_response(jsonify(response_data), 200)
        return make_response(jsonify({'message': 'qrcode not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting qrcode', 'error': str(e)}), 500)
    
# update qr code
@app.route('/api/flask/qrcodes/<id>', methods=['PUT'])
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
@app.route('/api/flask/qrcodes/<id>', methods=['DELETE'])
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