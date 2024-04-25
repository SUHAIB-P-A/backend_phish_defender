import joblib
import feature_extraction
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

model = joblib.load("random_forest_model.pkl")
print(model)

url = 'https://djsindia.in/e/?n=Rafeek-'

x_new=[]
x_new= feature_extraction.generate_dataset(url)
print(x_new)
x_new[0]=np.array(x_new[0]).reshape(1,-1)
print(x_new[0])

try:
    prediction = model.predict(x_new[0])
    print(prediction[0])
    if prediction == 1:
        print("Good Website")
    else:
        print("Bad Website")    

except Exception as e:
    print(e)    