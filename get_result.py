import joblib
import feature_extraction
import numpy as np
import requests
from requests.exceptions import ConnectionError




from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

model = joblib.load("random_forest_model.pkl")
print(model)

#url = 'google.com'
# https://djsindia.in/e/?n=Rafeek-
def get_resultfunc(url):
    x_new=[]
    res=get_url(url)
    if res == -1:
        return "suspicious😈 \n or \n connection not found"
    else:
        x_new = feature_extraction.generate_dataset(url)
    print(x_new)
    x_new[0] = np.array(x_new[0]).reshape(1, -1)
    print(x_new[0])

    try:
        prediction = model.predict(x_new[0])
        print(prediction[0])
        if prediction == 1:
            # print("")
            return "legitimate 😇"
        else:
            # print("Bad Website")
            return "suspicious 😈"

    except Exception as e:
        # print(e)
        return "suspicious 😈"


def get_url(url):
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url)
            return response.text
        except ConnectionError as e:
            print("Connection error occurred:", e)
            retry_count += 1

    print("Failed to retrieve URL after", max_retries, "attempts.")
    return -1
