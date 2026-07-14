import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

from url_features import extract_features


# Load dataset
data = pd.read_csv("data/real_phishing_urls.csv")

# Keep URL and label columns
data = data[["URL", "label"]]
data = data.rename(columns={"URL": "url"})

# Convert labels
data["label"] = data["label"].map({
    1: "legitimate",
    0: "phishing"
})

# Extract features
print("Extracting features...")
features = data["url"].apply(extract_features)
X = pd.DataFrame(list(features))
y = data["label"]

# Split data same way as before
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Load best model
model = joblib.load("models/best_phishing_model.pkl")

# Predict
print("Generating predictions...")
y_pred = model.predict(X_test)

# Print classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=["legitimate", "phishing"])

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Legitimate", "Phishing"]
)

display.plot()
plt.title("Confusion Matrix - Phishing URL Detector")
plt.tight_layout()
plt.savefig("models/confusion_matrix.png")
plt.close()

print("Confusion matrix saved as models/confusion_matrix.png")

# Feature Importance
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(feature_importance)

feature_importance.to_csv("models/feature_importance.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance["Feature"], feature_importance["Importance"])
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Feature Importance - Random Forest")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("models/feature_importance.png")
plt.close()

print("Feature importance saved as models/feature_importance.png")