import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Load data
df = pd.read_csv('sensor_data.csv')

# Preprocess data
scaler = StandardScaler()
X = scaler.fit_transform(df[['temperature', 'co2']])

# Train Isolation Forest model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

# Save model
joblib.dump(model, 'isolation_forest_model.pkl')
