import streamlit as st
import requests
import string
import random
import re

def send_email_general(subject, content, recipient, email_type):
    try:
        email_data = {
            "subject": subject,
            "content": content,
            "recipient": recipient,
            "email_type": email_type
        }
        # url = st.secrets['SERVER_URL'] + st.secrets['SEND_EMAIL_GENERAL']
        url = "https://mkhorasani.pythonanywhere.com/send_email_general"
        # headers = {'Authorization': f'Bearer {st.secrets['API_KEY']}'}
        headers = {'Authorization': f'Bearer nP3tLSK80h4ecXnHi_5WMAMMqn0qkt-234z81ItlMEQ='}
        response = requests.post(url, headers=headers, json=email_data, timeout=30)
    except Exception as e:
        print(e)
    return True

def generate_random_verification_code():
    return ''.join(random.choice(string.digits) for i in range(4)).replace(' ','')

def validate_length(variable: str, min_length: int=1, max_length: int=254):
    pattern = rf"^.{{{min_length},{max_length}}}$"
    return bool(re.match(pattern, variable))
    
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]{1,254}@[a-zA-Z0-9.-]{1,253}\.[a-zA-Z]{2,63}$"
    return bool(re.match(pattern, email))

def create_api_key(app_name, email, first_name, last_name, plan):
    # url = st.secrets['SERVER_URL'] + st.secrets['CREATE_API']
    url = "https://mkhorasani.pythonanywhere.com/create_api_key"
    # headers = {'Authorization': f'Bearer {st.secrets['API_KEY']}'}
    headers = {'Authorization': f'Bearer nP3tLSK80h4ecXnHi_5WMAMMqn0qkt-234z81ItlMEQ='}
    dict_data = {
        'app_name'      :   app_name,
        'email'         :   f'{email}',
        'first_name'    :   first_name,
        'last_name'     :   last_name,
        'plan'          :   plan
        }
    response = requests.post(url, headers=headers, json=dict_data)
    if response.status_code == 200:
        data = response.json()
        return data
    return f"Error: {response.status_code} - {response.text}"

def unsubscribe_account(email):
    # url = st.secrets['SERVER_URL'] + st.secrets['UNSUBSCRIBE_ACCOUNT']
    url = "https://mkhorasani.pythonanywhere.com/unsubscribe_account"
    # headers = {'Authorization': f'Bearer {st.secrets['API_KEY']}'}
    headers = {'Authorization': f'Bearer nP3tLSK80h4ecXnHi_5WMAMMqn0qkt-234z81ItlMEQ='}
    dict_data = {
        'email'         :   f'{email}'
        }
    response = requests.post(url, headers=headers, json=dict_data)
    if response.status_code == 200:
        data = response.json()
        return data
    return f"Error: {response.status_code} - {response.text}"
