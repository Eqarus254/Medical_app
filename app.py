
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

app = Flask(__name__)
MODEL_PATH = "model/isolation_model.pkl"

def train_model():
    data = {
        'heart_rate': np.random.randint(60, 100, 100),
        'blood_oxygen': np.random.randint(90, 100, 100)
    }
    df = pd.DataFrame(data)
    model = IsolationForest(contamination=0.1)
    model.fit(df[['heart_rate', 'blood_oxygen']])
    joblib.dump(model, MODEL_PATH)
    return model

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = train_model()

@app.route("/")
def home():
    return "AI Health Monitor API is Running!"

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        heart_rate = data.get("heart_rate")
        blood_oxygen = data.get("blood_oxygen")

        if heart_rate is None or blood_oxygen is None:
            return jsonify({"error": "Missing data"}), 400

        input_df = pd.DataFrame([[heart_rate, blood_oxygen]], columns=["heart_rate", "blood_oxygen"])
        prediction = model.predict(input_df)[0]
        result = "Anomaly" if prediction == -1 else "Normal"

        return jsonify({
            "heart_rate": heart_rate,
            "blood_oxygen": blood_oxygen,
            "prediction": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
