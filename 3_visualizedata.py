import pandas as pd
import matplotlib.pyplot as plt

# Load original and noisy data
df_original = pd.read_csv('sensor_data.csv')
df_noisy = pd.read_csv('sensor_data_noisy.csv')

# Convert 'timestamp' column to datetime
df_original['timestamp'] = pd.to_datetime(df_original['timestamp'])
df_noisy['timestamp'] = pd.to_datetime(df_noisy['timestamp'])

# Plot data
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(df_original['timestamp'], df_original['temperature'], marker='o', linestyle='-', color='b', label='Original Temperature')
plt.plot(df_noisy['timestamp'], df_noisy['temperature'], marker='x', linestyle='--', color='r', label='Noisy Temperature')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.title('Temperature Data')

plt.subplot(2, 1, 2)
plt.plot(df_original['timestamp'], df_original['co2'], marker='o', linestyle='-', color='b', label='Original CO2')
plt.plot(df_noisy['timestamp'], df_noisy['co2'], marker='x', linestyle='--', color='r', label='Noisy CO2')
plt.xlabel('Timestamp')
plt.ylabel('CO2 (ppm)')
plt.legend()
plt.title('CO2 Data')

plt.tight_layout()
plt.show()
