
from flask import Blueprint, request, jsonify, render_template
import joblib
import numpy as np

bp = Blueprint('main', __name__)
model = joblib.load('model/isolation_model.pkl')

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    heart_rate = data.get('heart_rate')
    blood_oxygen = data.get('blood_oxygen')

    X = np.array([[heart_rate, blood_oxygen]])
    prediction = model.predict(X)
    label = "Anomaly" if prediction[0] == -1 else "Normal"

    return jsonify({'status': label})
