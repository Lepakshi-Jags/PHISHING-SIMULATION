import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from url_features import extract_features


# Load dataset
data = pd.read_csv("data/real_phishing_urls.csv")

# Keep URL and label only
data = data[["URL", "label"]]
data = data.rename(columns={"URL": "url"})

# Convert labels
data["label"] = data["label"].map({
    1: "legitimate",
    0: "phishing"
})

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)
print("\nLabel distribution:")
print(data["label"].value_counts())

# Extract features
print("\nExtracting features...")
features = data["url"].apply(extract_features)
X = pd.DataFrame(list(features))
y = data["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Models to compare
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

results = []

print("\nTraining and comparing models...")

for model_name, model in models.items():
    print(f"\nTraining {model_name}...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    results.append({
        "Model": model_name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, pos_label="phishing"),
        "Recall": recall_score(y_test, y_pred, pos_label="phishing"),
        "F1 Score": f1_score(y_test, y_pred, pos_label="phishing")
    })

# Convert results to dataframe
results_df = pd.DataFrame(results)

print("\nModel Comparison Results:")
print(results_df)

# Save results
results_df.to_csv("models/model_comparison_results.csv", index=False)

# Plot model comparison
plt.figure(figsize=(10, 6))
plt.bar(results_df["Model"], results_df["F1 Score"])
plt.title("Model Comparison Based on F1 Score")
plt.xlabel("Machine Learning Model")
plt.ylabel("F1 Score")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("models/model_comparison_f1.png")
plt.close()

# Save best model based on F1 score
best_model_name = results_df.sort_values(by="F1 Score", ascending=False).iloc[0]["Model"]
best_model = models[best_model_name]

joblib.dump(best_model, "models/best_phishing_model.pkl")

print(f"\nBest Model: {best_model_name}")
print("Comparison results saved in models/model_comparison_results.csv")
print("F1 score chart saved in models/model_comparison_f1.png")
print("Best model saved as models/best_phishing_model.pkl")