from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

# Load data
data = pd.read_csv("Fearless_709H-10_31-11_07.csv", parse_dates=['time'])
data['time'] = pd.to_datetime(data['time'])

# Feature engineering
data['Rate_of_Change'] = data['Inj Gas Meter Volume Instantaneous'].diff()
data['Valve_Effectiveness'] = data['Inj Gas Meter Volume Instantaneous'] / data['Inj Gas Valve Percent Open']
data['Rolling_Avg'] = data['Inj Gas Meter Volume Instantaneous'].rolling(window=3).mean()
data = data.dropna()  # Drop rows with NaN from rolling/diff calculations

# Labeling (example: high risk if rate of change < -10)
data['Hydrate_Risk'] = (data['Rate_of_Change'] < -10).astype(int)

# Split data
X = data[['Inj Gas Meter Volume Instantaneous', 'Rate_of_Change', 'Valve_Effectiveness', 'Rolling_Avg']]
y = data['Hydrate_Risk']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Feature importance
importances = model.feature_importances_
features = X.columns
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance:.4f}")
