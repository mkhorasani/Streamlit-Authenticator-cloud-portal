import streamlit as st
from PIL import Image
import pandas as pd
import json

from utils import *

class VerificationError(Exception):
    """
    Raised when the verification code is incorrect.
    """
    pass

class SubscriptionError(Exception):
    """
    Raised when there is an issue with subscribing or unsubscribing.
    """
    pass

# Load and set page icon
icon: Image.Image = Image.open('icon.png')

st.set_page_config(
    page_title="Streamlit Authenticator",
    page_icon=icon
)

# Hide Streamlit menu and footer
hide_menu_style: str = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def register_verification_code(app_name: str, email_register: str) -> None:
    """
    Displays the verification code input field and processes the code for registration.
    
    Parameters
    ----------
    app_name : str
        The name of the application being registered.
    email_register : str
        The email address used for registration.
    """
    st.info('Please check your email for the verification code')
    code: str = st.text_input('Code', autocomplete='off')
    if st.button('Verify code'):
        try:
            if not check_hash(code, st.session_state['register_code']):
                raise VerificationError('Code is incorrect')
            result = create_api_key(app_name, email_register, 'None', 'None', 'FREE')
            st.session_state.pop('register_code', None)
            if 'sent to email successfully' not in result['message']:
                raise SubscriptionError('Unable to subscribe')
            st.success('API key sent to email')
        except (VerificationError, SubscriptionError) as e:
            st.error(str(e))

def unsubscribe_account_verification_code(email_unsubscribe: str) -> None:
    """
    Displays the verification code input field and processes the code for account unsubscription.
    
    Parameters
    ----------
    email_unsubscribe : str
        The email address used for unsubscription.
    """
    st.info('Please check your email for the verification code')
    code: str = st.text_input('Code', autocomplete='off')
    if st.button('Verify code'):
        try:
            if not check_hash(code, st.session_state['unsubscribe_code']):
                raise VerificationError('Code is incorrect')
            result = unsubscribe_account(email_unsubscribe)
            st.session_state.pop('unsubscribe_code', None)
            if 'deleted successfully' not in result['message']:
                raise SubscriptionError('Unable to unsubscribe')
            st.success('Account unsubscribed successfully')
        except (VerificationError, SubscriptionError) as e:
            st.error(str(e))
            
# Display logo
st.image('logo.png')
tab1, tab2, tab3, tab4 = st.tabs(['Register', 'Unsubscribe', 'Stats', 'Contact'])

# Registration tab
with tab1:
    st.markdown("""Register to receive a free API key to use Streamlit Authenticator's
        **two factor authentication** and **send email** features""")
    app_name: str = st.text_input('Your application name', autocomplete='off')
    email_register: str = st.text_input('Email', key='email_register', autocomplete='off')
    
    if 'register_code' not in st.session_state:
        st.session_state['register_code'] = None

    if st.button('Register'):
        try:
            if not validate_email(email_register):
                raise ValueError('Email is not valid')
            if not validate_length(app_name):
                raise ValueError('Application name is not valid')
            result = email_previously_registered(email_register)
            if 'not previously registered' in result['message']:
                register_code: str = generate_random_verification_code()
                st.session_state['register_code'] = hash(register_code)
                send_email_general('Streamlit Authenticator Verification Code',
                                   register_code, email_register, '2FA')
            else:
                raise ValueError('Email is already registered')
        except ValueError as e:
            st.error(str(e))
    
    if st.session_state['register_code'] is not None:
        register_verification_code(app_name, email_register)

# Unsubscribe tab
with tab2:
    st.markdown("""Use the form below to unsubscribe and delete your account""")
    email_unsubscribe: str = st.text_input('Email', key='email_unsubscribe', autocomplete='off')
    
    if 'unsubscribe_code' not in st.session_state:
        st.session_state['unsubscribe_code'] = None

    if st.button('Unsubscribe'):
        try:
            if not validate_email(email_unsubscribe):
                raise ValueError('Email is not valid')
            result = email_previously_registered(email_unsubscribe)
            if 'not previously registered' in result['message']:
                raise ValueError('An account with this email does not exist')
            unsubscribe_code: str = generate_random_verification_code()
            st.session_state['unsubscribe_code'] = hash(unsubscribe_code)
            send_email_general('Streamlit Authenticator Verification Code',
                               unsubscribe_code, email_unsubscribe, '2FA')
        except ValueError as e:
            st.error(str(e))
    
    if st.session_state['unsubscribe_code'] is not None:
        unsubscribe_account_verification_code(email_unsubscribe)
        
# Stats tab
with tab3:
    st.markdown("""Use the form below to retrieve the number of times your users have used the **two factor authentication** and/or **send email** features""")
    api_key: str = st.text_input('API key', key='api_key', autocomplete='off')
    if st.button('Check'):
        try:
            if not validate_length(api_key, min_length=32, max_length=32):
                raise ValueError('API key is not correct')
            result = count_calls(api_key)
            if 'None' in result['message']:
                raise ValueError('An account with this API key does not exist')
            result = json.loads(result['message'].replace("'", '"'))
            result = pd.DataFrame.from_dict(result, orient='index', columns=['Calls'])
            st.write('___')
            st.metric('Total number of calls', int(result['Calls'].sum()))
            if int(result['Calls'].sum()) > 0:
                st.bar_chart(result)
        except ValueError as e:
            st.error(str(e))

# Contact tab
with tab4:
    st.markdown("""Use the form below to contact us for any queries""")
    sender_email = st.text_input('Email')
    contact_message = st.text_area('Message')
    if st.button('Send'):
        try:
            if not validate_email(sender_email):
                raise ValueError('Email is not valid')
            if not validate_length(contact_message):
                raise ValueError('Message cannot be empty')
            send_email_general('Streamlit Authenticator Contact',
                           contact_message, sender_email, 'CONTACT')
            st.success('Message sent successfully')
        except ValueError as e:
            st.error(str(e))

# Footer
st.write('___')
st.markdown(
'''<div class="markdown-text-container stText" style="width: 698px;"><footer><p></p></footer><div style="font-size: 12px;"> 
<a href="https://github.com/mkhorasani/Streamlit-Authenticator">GitHub Homepage</a></div><div style="font-size: 12px;"> 
Streamlit Authenticator</div></div>''',
unsafe_allow_html=True)
