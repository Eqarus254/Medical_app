from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import numpy as np
import joblib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the model
model_path = 'model/health_rf_model.pkl'
model = joblib.load(model_path)

# Dummy user credentials
users = {'admin': 'password'}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [float(request.form[key]) for key in request.form]
        features = np.array(data).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({'prediction': int(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
