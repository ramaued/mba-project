import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'c0ny6eduzgm_88NL7y4Md7hFKqiecmcJ2o4EJGVtE6to'

deta = Deta(DETA_KEY)

db = deta.Base('LoginAuth')

def insert_users(email, username, password):
    date_joined = str(datetime.datetime.now())

    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def fetch_users():
    users = db.fetch()
    return users.items


def get_emails():
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
    pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    pattern = "^[A-a-zA-Z0-9]"
    if re.match(pattern, username):
        return True
    return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Daftar Akun')
        email = st.text_input('Email')
        username = st.text_input('Username')
        password1 = st.text_input('Password', type='password')
        password2 = st.text_input('Confirm Password', type='password')

        if email:
            if validate_email(email):
                if email not in get_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_users(email, username, hashed_password[0])
                                        st.success('Akun kamu berhasil dibuat!')
                                    else:
                                        st.warning('Password tidak cocok!')
                                else:
                                    st.warning('Password terlalu pendek!')
                            else:
                                st.warning('Username terlalu pendek!')
                        else:
                            st.warning('Username sudah dipakai!')

                    else:
                        st.warning('Username tidak valid!')
                else:
                    st.warning('Email sudah dipakai!')
            else:
                st.warning('Email tidak valid!')

        st.form_submit_button('Sign Up')
