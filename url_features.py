from urllib.parse import urlparse
import re


def normalize_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def has_ip_address(url):
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    return 1 if re.search(ip_pattern, url) else 0


def extract_features(url):
    url = normalize_url(url)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    suspicious_words = [
        "login", "verify", "secure", "account", "update",
        "bank", "free", "gift", "confirm", "password",
        "otp", "signin", "payment"
    ]

    features = {
        "url_length": len(url),
        "domain_length": len(domain),
        "has_https": 1 if parsed_url.scheme == "https" else 0,
        "has_at_symbol": 1 if "@" in url else 0,
        "has_dash": 1 if "-" in domain else 0,
        "has_ip_address": has_ip_address(url),
        "dot_count": url.count("."),
        "slash_count": url.count("/"),
        "subdomain_count": domain.count("."),
        "digit_count": sum(char.isdigit() for char in url),
        "special_char_count": sum(not char.isalnum() for char in url),
        "has_suspicious_words": 1 if any(
            word in url.lower() for word in suspicious_words
        ) else 0,
    }

    return features