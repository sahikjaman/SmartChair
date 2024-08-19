import pandas as pd
import numpy as np

def add_noise_to_dataset(file_path, output_path, noise_type='both', noise_level=0.1):
    df = pd.read_csv(file_path)
    
    for column in df.columns:
        if column in ['timestamp']:
            continue  # Skip the timestamp column
        if noise_type == 'both' or noise_type == column:
            if column == 'temperature':
                noise = np.random.uniform(-2, 2, df.shape[0])
            else:
                noise = noise_level * df[column] * np.random.randn(len(df))
            df[column] += noise
    
    df.to_csv(output_path, index=False)
    return df

# Add noise to both columns
file_path = 'sensor_data.csv'
output_path = 'sensor_data_noisy.csv'
noisy_df = add_noise_to_dataset(file_path, output_path, noise_type='both', noise_level=0.1)
