import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#used keras apis for the neural network
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import joblib

def generateHydrate(data):
    data['Hydrate_Status'] = 0  # Initialize hydrate status column
    for i in range(1, len(data)):
        data['Hydrate_Status'].iloc[i] = generateHydrate(data.iloc[i], data.iloc[i-1])
    return data

def train():
    # Load training data 
    originalData = pd.read_csv('Fearless_709H-10_31-11_07.csv')

    # Forward fill 'Inj Gas Valve Percent Open' if there's a missing value
    originalData['Inj Gas Valve Percent Open'] = originalData['Inj Gas Valve Percent Open'].fillna(method='ffill')

    
    originalData['Rate_of_Change'] = originalData['Inj Gas Meter Volume Instantaneous'].diff()
    originalData['Valve_Effectiveness'] = originalData['Inj Gas Meter Volume Instantaneous'] / originalData['Inj Gas Valve Percent Open']
    originalData['Rolling_Avg'] = originalData['Inj Gas Meter Volume Instantaneous'].rolling(window=3).mean()

    # dataframe
    data = generateHydrate(originalData)

    
    #data = data.dropna()

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
        X_sequences.append(X_scaled[i-time_steps:i])  # Take the previous 'time_steps' rows as the sequence
        y_sequences.append(y.iloc[i])  # Take the hydrate status at the current time step

    X_sequences = np.array(X_sequences)
    y_sequences = np.array(y_sequences)

    # Split the data into training and testing sets
    xTrain, xTest, yTrain, yTest = train_test_split(X_sequences, y_sequences, test_size=0.2, random_state=42)

    # LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=False, input_shape=(xTrain.shape[1], xTrain.shape[2])))
    model.add(Dropout(0.2))  
    model.add(Dense(1, activation='sigmoid'))  
    #adam optimizer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(xTrain, yTrain, epochs=10, batch_size=32, validation_data=(xTest, yTest))

    # Predict probabilities of hydrate formation
    hydrate_probabilities = model.predict(xTest)

    # Display probabilities for each row
    result_df = pd.DataFrame(xTest.reshape(xTest.shape[0], -1))  
    result_df['Hydrate_Probability'] = hydrate_probabilities
    print(result_df)

    # Save the trained model
    model.save('hydrate_detection.h5')
    print("Model saved successfully!")

# Train the model
train()