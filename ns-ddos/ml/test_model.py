import pandas as pd
import pickle
from sklearn.metrics import classification_report

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load test data
test_data = pd.read_csv('../data/test_data.csv')
features = test_data.drop('Label', axis=1)
labels = test_data['Label']

# Predict
predictions = model.predict(features)

# Evaluate
print(classification_report(labels, predictions))
