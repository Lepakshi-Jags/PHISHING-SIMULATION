import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

from url_features import extract_features


# Load real dataset
data = pd.read_csv("data/real_phishing_urls.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)

# Keep only URL and label columns
data = data[["URL", "label"]]

# Rename URL column to lowercase for simplicity
data = data.rename(columns={"URL": "url"})

# Convert numeric labels to readable labels
# In this dataset:
# 1 = legitimate
# 0 = phishing
data["label"] = data["label"].map({
    1: "legitimate",
    0: "phishing"
})

print("\nLabel distribution:")
print(data["label"].value_counts())

# Extract features from URLs
print("\nExtracting URL features...")
features = data["url"].apply(extract_features)
X = pd.DataFrame(list(features))

# Target labels
y = data["label"]

print("\nFeature extraction completed!")
print("Feature columns:")
print(X.columns.tolist())

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train model
print("\nTraining model...")
model.fit(X_train, y_train)

# Test model
print("\nTesting model...")
y_pred = model.predict(X_test)

print("\nModel Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save trained model
joblib.dump(model, "models/phishing_model.pkl")

print("\nReal dataset model saved successfully in models/phishing_model.pkl")