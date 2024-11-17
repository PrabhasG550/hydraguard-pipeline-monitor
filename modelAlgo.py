import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def determineHydrate(row,prevRow):
    if prevRow is not None:
        if row['Inj Gas Meter Volume Instantaneous'] <prevRow['Inj Gas Meter Volume Instantaneous'] and  row['Inj Gas Valve Percent Open'] >= prevRow['Inj Gas Valve Percent Open']:
         return 1 #if hydrate detected
    return 0 #if no hydrate detected

def generateHydrate(data):
    data['Hydrate_Status']=0
    for i in range(1,len(data)):
        data['Hydrate_Status'].iloc[i]=determineHydrate(data.iloc[i],data.iloc[i-1])
    #data = data.dropna()
    return data

def train():
    # Load your data 
    originalData = pd.read_csv('Fearless_709H-10_31-11_07.csv')

    # Example of feature engineering based on your dataset
    originalData['Rate_of_Change'] = originalData['Inj Gas Meter Volume Instantaneous'].diff()
    originalData['Valve_Effectiveness'] = originalData['Inj Gas Meter Volume Instantaneous'] / originalData['Inj Gas Valve Percent Open']
    originalData['Rolling_Avg'] = originalData['Inj Gas Meter Volume Instantaneous'].rolling(window=3).mean()

    # generate dataframe from original data with hydrate values
    data = generateHydrate(originalData)

    # Define features (X) and target (y)
    X = data[['Inj Gas Meter Volume Instantaneous', 'Rate_of_Change', 'Valve_Effectiveness', 'Rolling_Avg']]
    y = data['Hydrate_Status']  # Assume this is the column indicating hydrate status (1 = hydrate, 0 = no hydrate)

    # Split the data into training and testing sets
    xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest model
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(xTrain, yTrain)

    # Evaluate the model (optional)
    y_pred = rf.predict(xTest)
    print(classification_report(yTest, y_pred))

    # Save the trained model using joblib
    joblib.dump(rf, 'hydrate_detection.joblib')
    print("Model saved successfully!")

#train()
