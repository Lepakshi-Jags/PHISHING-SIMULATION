
# 🔐 AI-Powered Phishing URL Detection Dashboard

An end-to-end machine learning and cybersecurity project that detects whether a URL is legitimate or phishing based on URL structure, lexical features, and suspicious patterns.

The project includes model training, model comparison, feature importance analysis, confusion matrix visualization, and a Streamlit-based interactive dashboard.

---

## 🚀 Project Overview

Phishing websites are commonly used to steal sensitive information such as passwords, banking credentials, OTPs, and personal data. This project uses machine learning to classify URLs as either:

- Legitimate
- Phishing

The model is trained on a real-world phishing URL dataset containing more than 235,000 URLs.

---

## 📊 Dataset

The dataset contains:

- Total URLs: 235,795
- Legitimate URLs: 134,850
- Phishing URLs: 100,945

Main target column:

```text
label
1 = legitimate
0 = phishing
🧠 Features Engineered

The model extracts URL-based features such as:

URL length
Domain length
HTTPS presence
@ symbol presence
Dash presence
IP address presence
Dot count
Slash count
Subdomain count
Digit count
Special character count
Suspicious words such as login, verify, secure, update, bank, free, gift
🤖 Machine Learning Models Compared

The project compares multiple ML models:

Logistic Regression
Decision Tree
Random Forest
Gradient Boosting

The best-performing model was:

Random Forest
📈 Model Performance

Best model performance:

Accuracy: 99.57%
Phishing F1-score: 99.49%

Model comparison results:

Model	Accuracy	Precision	Recall	F1 Score
Logistic Regression	0.993299	0.999698	0.984645	0.992115
Decision Tree	0.995632	0.998901	0.990860	0.994878
Random Forest	0.995717	0.998802	0.991183	0.994978
Gradient Boosting	0.995420	0.999200	0.990094	0.994626
🔍 Important Features

Top features influencing the Random Forest model:

HTTPS presence
Slash count
Digit count
Special character count
URL length
Subdomain count
Domain length
🖥️ Streamlit Dashboard

The dashboard includes:

URL scanner
Prediction result
Model confidence score
Phishing risk score
Extracted URL features
Model comparison table
F1-score chart
Confusion matrix
Feature importance chart
Phishing safety tips
🛠️ Tech Stack
Python
Pandas
Scikit-learn
Matplotlib
Joblib
Streamlit
📁 Project Structure
Phishing-URL-Detector
│
├── app.py
├── train_model.py
├── model_comparison.py
├── model_analysis.py
├── url_features.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data
│   ├── phishing_urls.csv
│   └── real_phishing_urls.csv
│
└── models
    ├── model_comparison_results.csv
    ├── model_comparison_f1.png
    ├── confusion_matrix.png
    ├── feature_importance.csv
    └── feature_importance.png
▶️ How to Run the Project
1. Clone the repository
git clone <your-repository-link>
cd Phishing-URL-Detector
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Train the model
python train_model.py
5. Compare models
python model_comparison.py
6. Generate analysis graphs
python model_analysis.py
7. Run the Streamlit app
streamlit run app.py
📌 Future Improvements
Add WHOIS-based domain age features
Add DNS and IP reputation checks
Add real-time URL scanning APIs
Deploy the app on Streamlit Cloud
Add browser extension support
Improve model explainability using SHAP
Add deep learning-based URL classification
⚠️ Disclaimer

This project is built for educational, cybersecurity learning, and portfolio purposes. It should not be used as a replacement for professional cybersecurity tools.
=======
# PHISHING-SIMULATION
