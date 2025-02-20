import streamlit as st
from PIL import Image

from utils import *

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

@st.dialog('Verification code')
def register_verification_code(app_name, email_register):
    st.info('Please check your email for the verification code')
    code = st.text_input('Code', autocomplete='off')
    if st.button('Verify code'):
        if st.session_state['register_code'] == code:
            result = create_api_key(app_name, email_register, 'None', 'None', 'FREE')
            if 'previous' in result:
                del st.session_state['register_code']
                st.error('Email previously registered')
            else:
                del st.session_state['register_code']
                st.success('API key sent to email')
        else:
            st.error('Code is incorrect')

@st.dialog('Verification code')
def unsubscribe_account_verification_code(email_unsubscribe):
    st.info('Please check your email for the verification code')
    code = st.text_input('Code', autocomplete='off')
    if st.button('Verify code'):
        if st.session_state['unsubscribe_code'] == code:
            result = unsubscribe_account(email_unsubscribe)
            if 'deleted successfully' in result:
                del st.session_state['unsubscribe_code']
                st.success('Account unsubscribed successfully')
            else:
                del st.session_state['unsubscribe_code']
                st.success('Unable to unsubscribe')
        else:
            st.error('Code is incorrect')

st.image('logo.png')

tab1, tab2 = st.tabs(['Register', 'Unsubscribe'])

with tab1:
    st.markdown("""Register to receive a free API key to use Streamlit Authenticator's
        **two factor authentication** and **send email** features""")
    app_name = st.text_input('Application name')
    email_register = st.text_input('Email', key='email_register')

    if 'register_code' not in st.session_state:
        st.session_state['register_code'] = None

    if st.button('Generate API key'):
        if not validate_email(email_register):
            st.error('Email is not valid')
        elif not validate_length(app_name):
            st.error('Application name is not valid')
        else:
            st.session_state['register_code'] = generate_random_verification_code()
            send_email_general('Streamlit Authenticator Verification Code',
                               st.session_state['register_code'], email_register, '2FA')

    if st.session_state['register_code'] != None:
        register_verification_code(app_name, email_register)

with tab2:
    st.markdown("""Use the form below to unsubscribe and delete your account""")
    email_unsubscribe = st.text_input('Email', key='email_unsubscribe')

    if 'unsubscribe_code' not in st.session_state:
        st.session_state['unsubscribe_code'] = None

    if st.button('Unsubscribe'):
        if 'not previously registered' not in email_previously_registered(email_unsubscribe):
            st.session_state['unsubscribe_code'] = generate_random_verification_code()
            send_email_general('Streamlit Authenticator Verification Code',
                                st.session_state['unsubscribe_code'], email_register, '2FA')
        else:
            st.error('An account with this email does not exist')
    if st.session_state['unsubscribe_code'] != None:
        unsubscribe_account_verification_code(email_unsubscribe)

st.write('___')
st.markdown(
'''<div class="markdown-text-container stText" style="width: 698px;"><footer><p></p></footer><div style="font-size: 12px;"> 
<a href="https://github.com/mkhorasani/Streamlit-Authenticator">GitHub Homepage</a></div><div style="font-size: 12px;"> 
Streamlit Authenticator</div></div>''',
unsafe_allow_html=True)