from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load model and scaler
model = joblib.load(open('health_rf_model.pkl', 'rb'))
scaler = joblib.load(open('health_seq_scaler.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    prediction_result = None
    category = None

    if request.method == 'POST':
        try:
            age = float(request.form['age'])
            heart_rate = float(request.form['heart_rate'])
            bp = float(request.form['bp'])
            glucose = float(request.form['glucose'])
            bmi = float(request.form['bmi'])
            oxygen = float(request.form['oxygen'])
            gender = 1 if request.form['gender'] == 'Male' else 0

            input_data = np.array([[age, heart_rate, bp, glucose, bmi, oxygen, gender]])
            scaled = scaler.transform(input_data)
            prediction = model.predict(scaled)[0]

            prediction_result = prediction
            if prediction == 0:
                category = "Normal"
            elif prediction == 1:
                category = "Risk"
            else:
                category = "Critical"

        except Exception as e:
            prediction_result = "Error in input"

    return render_template('dashboard.html', prediction=prediction_result, category=category)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
