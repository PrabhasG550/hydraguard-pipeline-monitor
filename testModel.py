import pandas as pd
from modelAlgo import determineHydrate, genXYSequences
from tensorflow.keras.models import load_model

# Load the model
model = load_model('hydrate_detection.h5')

# Replace with your desired data file
newData = pd.read_csv('Valiant_505H-09_22-09_30.csv')
print('FILLNA\n')
df = newData.fillna(method='ffill').fillna(method='bfill')
#print(df)

# Convert 'Time' column to datetime, then extract useful features (e.g., hour, day, etc.)
newData['Time'] = pd.to_datetime(newData['Time'], errors='coerce')  # Convert to datetime, coercing errors to NaT
newData['hour'] = newData['Time'].dt.hour  # Extract hour as a feature
newData['day'] = newData['Time'].dt.day   # Extract day as a feature
newData['month'] = newData['Time'].dt.month  # Extract month as a feature
newData['year'] = newData['Time'].dt.year  # Extract year as a feature

# Drop the original 'Time' column, as it's no longer needed
newData = newData.drop(columns=['Time'])

# Handle missing values (NaN) by filling or dropping them
newData = newData.fillna(0)  # Or use any other strategy like .dropna() or interpolation

# Loop through the rows to check for hydrate detection
for i in range(1, len(newData)):
    hydrateStatus = determineHydrate(newData.iloc[i], newData.iloc[i - 1])
    if hydrateStatus == 1:
        print('HYDRATE DETECTED AT ROW', i, ':', newData.iloc[i])

XYSequences = genXYSequences('Bold_744H-10_31-11_07.csv')
X = XYSequences[0]

# Make predictions using the model
probs = model.predict(X)

# Print the data and predictions
print(newData)
print(probs)

print(df)
