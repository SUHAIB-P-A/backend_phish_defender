import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('Dataset Phising Website.csv')

# Remove the first column from the dataseta
data = data.drop('index', axis=1)

# Split the dataset into features (X) and target (Y)
X = data.drop('Result', axis=1)
Y = data['Result']

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42)

# Define the parameter grid for grid search
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Create a Random Forest Classifier instance
rf_classifier = RandomForestClassifier(random_state=42)

# Perform grid search
grid_search = GridSearchCV(estimator=rf_classifier,
                           param_grid=param_grid, cv=5, scoring='accuracy')
print(grid_search)
grid_search.fit(X_train, Y_train)

# Get the best parameters and best estimator
best_params = grid_search.best_params_
print(best_params)
best_rf_classifier = grid_search.best_estimator_
print(best_rf_classifier)

# Model training with best parameters
best_rf_classifier.fit(X_train, Y_train)

# Make predictions
y_predict = best_rf_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(Y_test, y_predict)
print("Accuracy:", accuracy*100)

# Save the best model
joblib.dump(best_rf_classifier, 'random_forest_model.pkl')
