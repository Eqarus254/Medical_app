from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

app = Flask(__name__)
MODEL_PATH = os.path.join("app", "model.pkl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])
        model = joblib.load(MODEL_PATH)
        prediction = model.predict(df)
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api', methods=['GET'])
def api_status():
    return "AI Health Monitor API is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)