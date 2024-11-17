import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import joblib

import sys
import io

# Force stdout and stderr to use UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def determineHydrate(row, prevRow):
    if prevRow is not None:
        if row['Inj Gas Meter Volume Instantaneous'] < prevRow['Inj Gas Meter Volume Instantaneous'] and row['Inj Gas Valve Percent Open'] >= prevRow['Inj Gas Valve Percent Open']:
            return 1  # if hydrate detected
    return 0  # if no hydrate detected

def generateHydrate(data):
    data['Hydrate_Status'] = 0  # Initialize hydrate status column
    for i in range(1, len(data)):
        data['Hydrate_Status'].iloc[i] = determineHydrate(data.iloc[i], data.iloc[i - 1])
    return data

def genXYSequences(filename):
    # Load training data
    df = pd.read_csv(filename)
    originalData = df.fillna(method='ffill').fillna(method='bfill')

    # Forward fill 'Inj Gas Valve Percent Open' if there's a missing value
    originalData['Inj Gas Valve Percent Open'] = originalData['Inj Gas Valve Percent Open'].fillna(method='ffill')

    originalData['Rate_of_Change'] = originalData['Inj Gas Meter Volume Instantaneous'].diff()
    originalData['Valve_Effectiveness'] = originalData['Inj Gas Meter Volume Instantaneous'] / originalData['Inj Gas Valve Percent Open']
    originalData['Rolling_Avg'] = originalData['Inj Gas Meter Volume Instantaneous'].rolling(window=3).mean()

    # dataframe
    data = generateHydrate(originalData)

    # Drop rows with NaN values
    data.dropna(inplace=True)

    # X and Y
    X = data[['Inj Gas Meter Volume Instantaneous', 'Rate_of_Change', 'Valve_Effectiveness', 'Rolling_Avg']]
    y = data['Hydrate_Status']

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Reshape the data into sequences for LSTM (samples, timesteps, features)
    time_steps = 5  # Define the number of time steps you want to look back
    X_sequences = []
    y_sequences = []

    for i in range(time_steps, len(X_scaled)):
        X_sequences.append(X_scaled[i - time_steps:i])  # Take the previous 'time_steps' rows as the sequence
        y_sequences.append(y.iloc[i])  # Take the hydrate status at the current time step

    X_sequences = np.array(X_sequences)
    y_sequences = np.array(y_sequences)

    return [X_sequences, y_sequences]

def train():
    sequences = genXYSequences('Fearless_709H-10_31-11_07.csv')
    X_sequences = sequences[0]
    y_sequences = sequences[1]

    # Split the data into training and testing sets
    xTrain, xTest, yTrain, yTest = train_test_split(X_sequences, y_sequences, test_size=0.2, random_state=42)

    # LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=False, input_shape=(xTrain.shape[1], xTrain.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    # Adam optimizer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(xTrain, yTrain, epochs=10, batch_size=32, validation_data=(xTest, yTest))

    # Predict probabilities of hydrate formation
    hydrate_probabilities = model.predict(xTest)
    print('HYDRATE PROBABILITIES:\n')
    print(hydrate_probabilities)

    # Save the trained model
    model.save('hydrate_detection.h5')
    print("Model saved successfully!")

# Train the model
train()
