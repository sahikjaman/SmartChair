from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
csv_file = 'sensor_data.csv'
model = joblib.load('isolation_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

# Inisialisasi file CSV dengan header jika belum ada
if not os.path.isfile(csv_file):
    df = pd.DataFrame(columns=['timestamp', 'temperature', 'co2'])
    df.to_csv(csv_file, index=False)

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if 'temperature' in data and 'co2' in data:
            timestamp = datetime.now().isoformat()
            new_data = pd.DataFrame([{'timestamp': timestamp, 'temperature': data['temperature'], 'co2': data['co2']}])
            df = pd.read_csv(csv_file)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(csv_file, index=False)

            # Analisisi data dan deteksi outlier
            df_scaled = scaler.transform(df[['temperature', 'co2']])
            predictions = model.predict(df_scaled)
            warnings = []
            for idx, pred in enumerate(predictions):
                if pred == -1:
                    warnings.append(f"Outlier detected at index {idx}: Temperature {df.loc[idx, 'temperature']}°C, CO2 {df.loc[idx, 'co2']} ppm")

            if warnings:
                return jsonify({'message': 'Data received and saved', 'warnings': warnings}), 200
            else:
                return jsonify({'message': 'Data received and saved', 'warnings': 'No warnings'}), 200
        else:
            return jsonify({'message': 'Invalid data: missing temperature or co2'}), 400
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'message': f'Internal server error: {e}'}), 500

@app.route('/download_csv', methods=['GET'])
def download_csv():
    try:
        return send_file(csv_file, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error sending file: {e}")
        return jsonify({'message': f'Internal server error: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
