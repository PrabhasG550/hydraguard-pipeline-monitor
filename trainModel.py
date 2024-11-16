import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# loading the data
data = pd.read_csv('Fearless_709H-10_31-11_07.csv')


data['Rate_of_Change'] = data['Inj Gas Meter Volume Instantaneous'].diff()
data['Valve_Effectiveness'] = data['Inj Gas Meter Volume Instantaneous'] / data['Inj Gas Valve Percent Open']
data['Rolling_Avg'] = data['Inj Gas Meter Volume Instantaneous'].rolling(window=3).mean()

def hydrateLabel(row,prevRow):
    if prevRow is not None:
        if row['Inj Gas Meter Volume Instantaneous'] <prevRow['Inj Gas Meter Volume Instantaneous'] and  row['Inj Gas Valve Percent Open'] >= prevRow['Inj Gas Valve Percent Open']:
         return 1 #if hydrate detected
    return 0 #if no hydrate detected
data['Hydrate_Status']=0
for i in range(1,len(data)):
   data['Hydrate_Status'].iloc[i]=hydrateLabel(data.iloc[i],data.iloc[i-1])
data = data.dropna()  

# Define (X) and target (y)
X = data[['Inj Gas Meter Volume Instantaneous', 'Rate_of_Change', 'Valve_Effectiveness', 'Rolling_Avg']]
y = data['Hydrate_Status']  # Assume this is the column indicating hydrate status (1 = hydrate, 0 = no hydrate)

# training and testing sets
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
