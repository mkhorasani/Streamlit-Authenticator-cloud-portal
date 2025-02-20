import streamlit as st
from PIL import Image

from utils import *

class VerificationError(Exception):
    pass

class SubscriptionError(Exception):
    pass

icon = Image.open('icon.png')

st.set_page_config(
    page_title="Streamlit Authenticator",
    page_icon=icon
)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.write(st.session_state)
@st.dialog('Verification code')
def register_verification_code(app_name, email_register):
    st.info('Please check your email for the verification code')
    code = st.text_input('Code', autocomplete='off')
    if st.button('Verify code'):
        try:
            if not check_hash(code, st.session_state['register_code']):
                raise VerificationError('Code is incorrect')
            result = create_api_key(app_name, email_register, 'None', 'None', 'FREE')
            st.session_state.pop('register_code', None)
            if 'sent to email successfully' not in result['message']:
                raise SubscriptionError('Unable to subscribe')
            st.success('API key sent to email')
        except VerificationError as e:
            st.error(str(e))
        except SubscriptionError as e:
            st.error(str(e))

@st.dialog('Verification code')
def unsubscribe_account_verification_code(email_unsubscribe):
    st.info('Please check your email for the verification code')
    code = st.text_input('Code', autocomplete='off')
    if st.button('Verify code'):
        try:
            if not check_hash(code, st.session_state['unsubscribe_code']):
                raise VerificationError('Code is incorrect')
            result = unsubscribe_account(email_unsubscribe)
            st.session_state.pop('unsubscribe_code', None)
            if 'deleted successfully' not in result['message']:
                raise SubscriptionError('Unable to unsubscribe')
            st.success('Account unsubscribed successfully')
        except VerificationError as e:
            st.error(str(e))
        except SubscriptionError as e:
            st.error(str(e))

st.image('logo.png')
tab1, tab2 = st.tabs(['Register', 'Unsubscribe'])

with tab1:
    st.markdown("""Register to receive a free API key to use Streamlit Authenticator's
        **two factor authentication** and **send email** features""")
    app_name = st.text_input('Application name', autocomplete='off')
    email_register = st.text_input('Email', key='email_register', autocomplete='off')
    if 'register_code' not in st.session_state:
        st.session_state['register_code'] = None

    if st.button('Generate API key'):
        try:
            if not validate_email(email_register):
                raise ValueError('Email is not valid')
            if not validate_length(app_name):
                raise ValueError('Application name is not valid')
            result = email_previously_registered(email_register)
            if 'not previously registered' in result['message']:
                register_code = generate_random_verification_code()
                st.session_state['register_code'] = hash(register_code)
                send_email_general('Streamlit Authenticator Verification Code',
                                   register_code, email_register, '2FA')
            else:
                raise ValueError('Email is already registered')
        except ValueError as e:
            st.error(str(e))
    if st.session_state['register_code'] is not None:
        register_verification_code(app_name, email_register)

with tab2:
    st.markdown("""Use the form below to unsubscribe and delete your account""")
    email_unsubscribe = st.text_input('Email', key='email_unsubscribe', autocomplete='off')
    if 'unsubscribe_code' not in st.session_state:
        st.session_state['unsubscribe_code'] = None
    if st.button('Unsubscribe'):
        try:
            if not validate_email(email_unsubscribe):
                raise ValueError('Email is not valid')
            result = email_previously_registered(email_unsubscribe)
            if 'not previously registered' in result['message']:
                raise ValueError('An account with this email does not exist')
            unsubscribe_code = generate_random_verification_code()
            st.session_state['unsubscribe_code'] = hash(unsubscribe_code)
            send_email_general('Streamlit Authenticator Verification Code',
                               unsubscribe_code, email_unsubscribe, '2FA')
        except ValueError as e:
            st.error(str(e))
    if st.session_state['unsubscribe_code'] is not None:
        unsubscribe_account_verification_code(email_unsubscribe)

st.write('___')
st.markdown(
'''<div class="markdown-text-container stText" style="width: 698px;"><footer><p></p></footer><div style="font-size: 12px;"> 
<a href="https://github.com/mkhorasani/Streamlit-Authenticator">GitHub Homepage</a></div><div style="font-size: 12px;"> 
Streamlit Authenticator</div></div>''',
unsafe_allow_html=True)
