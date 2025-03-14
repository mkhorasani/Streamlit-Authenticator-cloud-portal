import streamlit as st
import requests
import string
import random
import bcrypt
import re

def check_hash(string: str, hashed_string: str) -> bool:
    """Check if a given string matches a hashed string."""
    return bcrypt.checkpw(string.encode(), hashed_string.encode())

def hash(string: str) -> str:
    """Generate a hashed version of the given string using bcrypt."""
    return bcrypt.hashpw(string.encode(), bcrypt.gensalt()).decode()

def send_email_general(subject: str, content: str, recipient: str, email_type: str) -> bool:
    """Send a general email using stored API credentials."""
    try:
        email_data = {
            "subject": subject,
            "content": content,
            "recipient": recipient,
            "email_type": email_type
        }
        url = st.secrets['URL_1']
        headers = {'Authorization': f'Bearer {st.secrets["N1"]}'}
        response = requests.post(url, headers=headers, json=email_data, timeout=30)
    except Exception as e:
        print(e)
    return True

def generate_random_verification_code() -> str:
    """Generate a 4-digit random verification code."""
    return ''.join(random.choice(string.digits) for _ in range(4)).replace(' ', '')

def validate_length(variable: str, min_length: int = 1, max_length: int = 254) -> bool:
    """Validate the length of a given string within a specified range."""
    pattern = rf"^.{{{min_length},{max_length}}}$"
    return bool(re.match(pattern, variable))

def validate_email(email: str) -> bool:
    """Validate an email address using regex."""
    pattern = r"^[a-zA-Z0-9._%+-]{1,254}@[a-zA-Z0-9.-]{1,253}\.[a-zA-Z]{2,63}$"
    return bool(re.match(pattern, email))

def create_api_key(app_name: str, email: str, first_name: str, last_name: str, plan: str) -> dict:
    """Create an API key for a given user and application."""
    url = st.secrets['URL_2']
    headers = {'Authorization': f'Bearer {st.secrets["N1"]}'}
    dict_data = {
        'app_name': app_name,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'plan': plan
    }
    response = requests.post(url, headers=headers, json=dict_data)
    if response.status_code == 200:
        return response.json()
    return {"error": f"{response.status_code} - {response.text}"}

def unsubscribe_account(email: str) -> dict:
    """Unsubscribe a user account using the provided email address."""
    url = st.secrets['URL_3']
    headers = {'Authorization': f'Bearer {st.secrets["N1"]}'}
    dict_data = {'email': email}
    response = requests.post(url, headers=headers, json=dict_data)
    if response.status_code == 200:
        return response.json()
    return {"error": f"{response.status_code} - {response.text}"}

def email_previously_registered(email: str) -> dict:
    """Check if an email address is already registered."""
    url = st.secrets['URL_4']
    headers = {'Authorization': f'Bearer {st.secrets["N1"]}'}
    dict_data = {'email': email}
    response = requests.post(url, headers=headers, json=dict_data)
    if response.status_code == 200:
        return response.json()
    return {"error": f"{response.status_code} - {response.text}"}

def count_calls(api_key: str) -> dict:
    """Retrieves the number of calls made for an account."""
    url = st.secrets['URL_5']
    headers = {'Authorization': f'Bearer {st.secrets["N1"]}'}
    dict_data = {'api_key': api_key}
    response = requests.post(url, headers=headers, json=dict_data)
    if response.status_code == 200:
        return response.json()
    return {"error": f"{response.status_code} - {response.text}"}
