
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

def train_and_save_model():
    df = pd.DataFrame({
        'heart_rate': np.random.randint(60, 100, 100),
        'blood_oxygen': np.random.randint(90, 100, 100)
    })
    model = IsolationForest(contamination=0.1)
    model.fit(df[['heart_rate', 'blood_oxygen']])
    joblib.dump(model, 'model/isolation_model.pkl')

if __name__ == "__main__":
    train_and_save_model()
