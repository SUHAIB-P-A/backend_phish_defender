# 1st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 2ed
data = pd.read_csv('Dataset Phising Website.csv')

# 3ed
data = data.drop('index', axis=1)


# 4th
X = data.drop('Result', axis=1)
# print(X)
# print(X.isnull().sum())
# ['having_IP_Address','URL_Length','Shortining_Service','having_At_Symbol','double_slash_redirecting','Prefix_Suffix','having_Sub_Domain','SSLfinal_State','Domain_registeration_length','Favicon','port','HTTPS_token','Request_URL','URL_of_Anchor','Links_in_tags','SFH','Submitting_to_email','Abnormal_URL','Redirect','on_mouseover','RightClick','popUpWidnow','Iframe','age_of_domain','DNSRecord','web_traffic','Page_Rank','Google_Index','Links_pointing_to_page','Statistical_report']
Y = data['Result']

# 5th
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42)

#print(X_train)
#print(X_test)
#print(Y_train)
#print(Y_test)

# 6th
rf_classifier = RandomForestClassifier(random_state=42)
#print(rf_classifier)

# 7th
rf_classifier.fit(X_train,Y_train)