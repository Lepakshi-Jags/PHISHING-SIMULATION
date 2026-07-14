import streamlit as st
import pandas as pd
import joblib
import os
from urllib.parse import urlparse

from url_features import extract_features


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🔐",
    layout="wide"
)

model = joblib.load("models/best_phishing_model.pkl")


# ---------------- TRUSTED DOMAIN OVERRIDE ----------------

TRUSTED_DOMAINS = [
    "google.com",
    "chatgpt.com",
    "openai.com",
    "microsoft.com",
    "apple.com",
    "amazon.in",
    "wikipedia.org",
    "github.com",
    "linkedin.com",
    "kaggle.com",
    "streamlit.io",
]


def normalize_url(input_url):
    input_url = input_url.strip()

    if not input_url.startswith(("http://", "https://")):
        input_url = "https://" + input_url

    return input_url


def get_clean_domain(input_url):
    input_url = normalize_url(input_url)
    parsed_url = urlparse(input_url)
    domain = parsed_url.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def is_trusted_domain(input_url):
    domain = get_clean_domain(input_url)

    for trusted_domain in TRUSTED_DOMAINS:
        if domain == trusted_domain or domain.endswith("." + trusted_domain):
            return True

    return False


# ---------------- SESSION STATE ----------------

if "page" not in st.session_state:
    st.session_state.page = "scanner"

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"


# ---------------- SIDEBAR SETTINGS ----------------

with st.sidebar:
    st.markdown("## Settings")
    st.session_state.theme = st.radio(
        "Choose Theme",
        ["Dark", "Light"],
        horizontal=True
    )

    st.markdown("---")
    st.markdown("### Project Info")
    st.markdown("**Dataset:** 235,795 URLs")
    st.markdown("**Best Model:** Random Forest")
    st.markdown("**Accuracy:** 99.57%")


# ---------------- THEME COLORS ----------------

if st.session_state.theme == "Dark":
    bg = "linear-gradient(135deg, #0f172a 0%, #111827 45%, #020617 100%)"
    card_bg = "rgba(30, 41, 59, 0.82)"
    card_border = "rgba(148, 163, 184, 0.22)"
    text = "#f8fafc"
    muted = "#cbd5e1"
    input_bg = "rgba(15, 23, 42, 0.95)"
    hero_bg = "linear-gradient(135deg, rgba(59,130,246,0.30), rgba(168,85,247,0.25))"
    info_bg = "rgba(14,165,233,0.12)"
    info_border = "rgba(56,189,248,0.32)"
    info_text = "#bae6fd"
    footer_text = "#94a3b8"
else:
    bg = "linear-gradient(135deg, #f8fafc 0%, #e0f2fe 45%, #f5f3ff 100%)"
    card_bg = "rgba(255, 255, 255, 0.88)"
    card_border = "rgba(37, 99, 235, 0.18)"
    text = "#0f172a"
    muted = "#334155"
    input_bg = "#ffffff"
    hero_bg = "linear-gradient(135deg, rgba(219,234,254,0.95), rgba(237,233,254,0.95))"
    info_bg = "rgba(224,242,254,0.85)"
    info_border = "rgba(14,165,233,0.25)"
    info_text = "#0f172a"
    footer_text = "#475569"


# ---------------- CUSTOM CSS ----------------

st.markdown(
    f"""
    <style>

    .stApp {{
        background: {bg} !important;
        color: {text} !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: {bg} !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        padding-top: 3rem;
        padding-bottom: 3rem;
    }}

    .block-container p {{
        color: {muted} !important;
    }}

    .block-container label {{
        color: {muted} !important;
        font-weight: 600 !important;
    }}

    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(18px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .hero-card {{
        padding: 38px;
        border-radius: 28px;
        background: {hero_bg};
        border: 1px solid {card_border};
        box-shadow: 0 20px 60px rgba(0,0,0,0.18);
        margin-bottom: 28px;
        animation: fadeIn 0.9s ease-in-out;
    }}

    .badge {{
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(34,197,94,0.14);
        border: 1px solid rgba(34,197,94,0.35);
        color: #16a34a;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 16px;
    }}

    .hero-title {{
        font-size: 48px;
        font-weight: 900;
        line-height: 1.1;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 14px;
    }}

    .hero-subtitle {{
        font-size: 18px;
        color: {muted};
        max-width: 980px;
        line-height: 1.7;
    }}

    .info-box {{
        padding: 18px;
        border-radius: 16px;
        background: {info_bg};
        border: 1px solid {info_border};
        color: {info_text};
        line-height: 1.7;
        margin-bottom: 25px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.10);
    }}

    .warning-box {{
        padding: 18px;
        border-radius: 16px;
        background: rgba(245,158,11,0.14);
        border: 1px solid rgba(245,158,11,0.35);
        color: {text};
        line-height: 1.7;
        margin-top: 15px;
        margin-bottom: 15px;
    }}

    .success-box {{
        padding: 22px;
        border-radius: 18px;
        background: rgba(34,197,94,0.14);
        border: 1px solid rgba(34,197,94,0.35);
        color: {text};
        font-size: 18px;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 15px;
    }}

    .danger-box {{
        padding: 22px;
        border-radius: 18px;
        background: rgba(239,68,68,0.14);
        border: 1px solid rgba(248,113,113,0.38);
        color: {text};
        font-size: 18px;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 15px;
    }}

    .tips-box {{
        padding: 24px;
        border-radius: 22px;
        background: {card_bg};
        border: 1px solid {card_border};
        box-shadow: 0 14px 40px rgba(0,0,0,0.12);
        color: {text};
        line-height: 1.8;
    }}

    .tips-box h3 {{
        color: {text} !important;
    }}

    .tips-box li {{
        color: {muted} !important;
        margin-bottom: 8px;
    }}

    .footer {{
        margin-top: 35px;
        padding: 18px;
        text-align: center;
        color: {footer_text};
        font-size: 14px;
    }}

    h1, h2, h3 {{
        color: {text} !important;
    }}

    div[data-baseweb="input"] {{
        background: {input_bg} !important;
        border-radius: 14px !important;
        border: 1px solid {card_border} !important;
    }}

    div[data-baseweb="input"] input {{
        background: {input_bg} !important;
        color: {text} !important;
        border-radius: 14px !important;
    }}

    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border: 1px solid {card_border} !important;
    }}

    input::placeholder {{
        color: {muted} !important;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.4rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 10px 26px rgba(37,99,235,0.25) !important;
    }}

    .stButton > button:hover {{
        transform: scale(1.03);
        box-shadow: 0 12px 32px rgba(124,58,237,0.35) !important;
        color: white !important;
    }}

    .stButton > button * {{
        color: white !important;
    }}

    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {card_border};
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    }}

    div[data-testid="stMetric"] label {{
        color: {muted} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {text} !important;
        font-weight: 900;
    }}

    [data-testid="stDataFrame"] {{
        background: {card_bg} !important;
        border-radius: 16px !important;
        border: 1px solid {card_border} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- HERO SECTION ----------------

st.markdown(
    """
    <div class="hero-card">
        <div class="badge">Machine Learning • Cybersecurity • Streamlit Dashboard</div>
        <div class="hero-title">AI-Powered Phishing URL Detection Dashboard</div>
        <div class="hero-subtitle">
            This dashboard uses machine learning to classify URLs as <b>legitimate</b> or <b>phishing</b>
            based on URL structure, lexical patterns, and suspicious indicators.
            The project includes model comparison, feature importance analysis, risk scoring, and cybersecurity awareness.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        Model trained on a real phishing URL dataset with <b>235,795 URLs</b>. 
        This project is for cybersecurity learning, portfolio demonstration, and ML practice.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- TOP NAVIGATION BUTTONS ----------------

col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    if st.button("URL Scanner", use_container_width=True):
        st.session_state.page = "scanner"

with col_nav2:
    if st.button("Model Performance", use_container_width=True):
        st.session_state.page = "performance"

with col_nav3:
    if st.button("Feature Importance", use_container_width=True):
        st.session_state.page = "features"

with col_nav4:
    if st.button("Safety Tips", use_container_width=True):
        st.session_state.page = "tips"

st.markdown("---")


# ---------------- PAGE 1: URL SCANNER ----------------

if st.session_state.page == "scanner":
    st.header("Scan a URL")

    url = st.text_input("Enter a URL to scan:")

    if st.button("Check URL"):
        if url.strip() == "":
            st.warning("Please enter a URL.")
        else:
            features = extract_features(url)
            features_df = pd.DataFrame([features])

            trusted = is_trusted_domain(url)

            if trusted:
                prediction = "legitimate"
                confidence = 100
                phishing_probability = 0
            else:
                prediction = model.predict(features_df)[0]

                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(features_df)[0]
                    classes = model.classes_
                    confidence = max(probabilities) * 100

                    phishing_probability = 0
                    if "phishing" in classes:
                        phishing_index = list(classes).index("phishing")
                        phishing_probability = probabilities[phishing_index] * 100
                else:
                    confidence = 0
                    phishing_probability = 0

            st.subheader("Prediction Result")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Prediction", prediction.upper())

            with col2:
                st.metric("Model Confidence", f"{confidence:.2f}%")

            with col3:
                st.metric("Phishing Risk Score", f"{phishing_probability:.2f}%")

            if trusted:
                st.markdown(
                    """
                    <div class="success-box">
                        This URL belongs to a trusted domain and is marked as legitimate.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif prediction == "phishing":
                st.markdown(
                    """
                    <div class="danger-box">
                        This URL is likely a phishing website.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="success-box">
                        This URL is likely legitimate.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                """
                <div class="warning-box">
                    <b>Model Limitation:</b> Machine learning models can sometimes give false positives,
                    especially for very long legitimate URLs containing many digits, slashes, or session IDs.
                    This dashboard is for learning and portfolio demonstration, not final cybersecurity decision-making.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("Extracted URL Features")
            st.dataframe(features_df, use_container_width=True)

            st.markdown(
                """
                <div class="info-box">
                    <b>Feature Meaning</b><br><br>
                    • <b>has_https</b>: Checks whether the URL uses HTTPS.<br>
                    • <b>url_length</b>: Longer URLs may be more suspicious.<br>
                    • <b>digit_count</b>: Too many digits can indicate suspicious patterns.<br>
                    • <b>special_char_count</b>: Many special characters can indicate obfuscation.<br>
                    • <b>subdomain_count</b>: Excessive subdomains may be used in phishing URLs.<br>
                    • <b>has_suspicious_words</b>: Detects words like login, verify, secure, bank, free, gift.
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------------- PAGE 2: MODEL PERFORMANCE ----------------

elif st.session_state.page == "performance":
    st.header("Model Performance")

    st.write("The project compares multiple machine learning models and selects the best-performing one.")

    comparison_path = "models/model_comparison_results.csv"
    chart_path = "models/model_comparison_f1.png"
    confusion_path = "models/confusion_matrix.png"

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Dataset Size", "235,795 URLs")

    with col_b:
        st.metric("Best Model", "Random Forest")

    with col_c:
        st.metric("Test Accuracy", "99.57%")

    if os.path.exists(comparison_path):
        results_df = pd.read_csv(comparison_path)
        st.subheader("Model Comparison Table")
        st.dataframe(results_df, use_container_width=True)
    else:
        st.warning("Model comparison results not found. Run model_comparison.py first.")

    col1, col2 = st.columns(2)

    with col1:
        if os.path.exists(chart_path):
            st.subheader("Model Comparison Chart")
            st.image(chart_path, use_container_width=True)
        else:
            st.warning("Model comparison chart not found.")

    with col2:
        if os.path.exists(confusion_path):
            st.subheader("Confusion Matrix")
            st.image(confusion_path, use_container_width=True)
        else:
            st.warning("Confusion matrix not found. Run model_analysis.py first.")


# ---------------- PAGE 3: FEATURE IMPORTANCE ----------------

elif st.session_state.page == "features":
    st.header("Feature Importance")

    st.write(
        "Feature importance explains which URL-based characteristics influenced the Random Forest model most."
    )

    importance_csv = "models/feature_importance.csv"
    importance_img = "models/feature_importance.png"

    col1, col2 = st.columns([1, 1])

    with col1:
        if os.path.exists(importance_csv):
            importance_df = pd.read_csv(importance_csv)
            st.subheader("Feature Importance Table")
            st.dataframe(importance_df, use_container_width=True)
        else:
            st.warning("Feature importance CSV not found.")

    with col2:
        if os.path.exists(importance_img):
            st.subheader("Feature Importance Chart")
            st.image(importance_img, use_container_width=True)
        else:
            st.warning("Feature importance chart not found.")


# ---------------- PAGE 4: SAFETY TIPS ----------------

elif st.session_state.page == "tips":
    st.header("Phishing Safety Tips")

    st.markdown(
        """
        <div class="tips-box">
            <h3>Common warning signs</h3>
            <ul>
                <li>Fake login pages asking for credentials</li>
                <li>Urgent messages asking for account verification</li>
                <li>Suspicious domains with extra words or misspellings</li>
                <li>Too many redirects or strange URL structures</li>
                <li>Offers that look too good to be true</li>
                <li>URLs using words like <code>secure</code>, <code>verify</code>, <code>update</code>, <code>bank</code>, <code>free</code>, or <code>gift</code></li>
            </ul>

            <h3>Safety advice</h3>
            <ul>
                <li>Do not enter passwords on unknown websites.</li>
                <li>Check the domain carefully before logging in.</li>
                <li>Avoid clicking suspicious links from emails or messages.</li>
                <li>Use multi-factor authentication.</li>
                <li>Use official apps or manually type website URLs.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- FOOTER ----------------

st.markdown(
    """
    <div class="footer">
        Built with Python, Scikit-learn, Random Forest and Streamlit • Cybersecurity ML Portfolio Project
    </div>
    """,
    unsafe_allow_html=True
)