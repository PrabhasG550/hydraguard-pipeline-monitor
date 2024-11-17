import joblib
import pandas as pd
import sklearn

from trainModel import determineHydrate

model = joblib.load('hydrate_detection.joblib')

# replace newData with desired data file
newData = pd.read_csv('Bold_744H-10_31-11_07.csv')

for i in range(1,len(newData)):
   hydrateStatus = determineHydrate(newData.iloc[i],newData.iloc[i-1])
   if hydrateStatus == 1:
      print('HYDRATE DETECTED AT ROW', i, ':', newData.iloc[i])
