import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('../data/CICDDoS2019.csv')

# Preprocess data (implement cleaning, encoding, normalization as needed)
# For example purposes, assume 'features' and 'labels' are prepared

features = data.drop('Label', axis=1)
labels = data['Label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
