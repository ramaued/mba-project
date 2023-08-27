import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from auth import sign_up, fetch_users
from apriori import runApriori, dataFromFile, to_str_results

st.set_page_config(page_title='MBA Project', layout='wide', initial_sidebar_state='expanded')

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
        
    Authenticator = stauth.Authenticate(credentials, "cookie_name", "random_key", cookie_expiry_days=30)

    col1, col2, col3, col4 = st.columns(4)

    with col2:
        email, authentication_status, username = Authenticator.login('Masuk Aplikasi', 'main')

    with col3:
        if not authentication_status:
            sign_up()

    info1, info2, info3, info4 = st.columns(4)

    if username:
        if username in usernames:
            if authentication_status:
                    with st.sidebar:
                        st.header("Dashboard")
                        st.markdown("\n")
                        #st.subheader(f'Welcome {username}')
                        default_csv = st.selectbox("Silakan pilih file di bawah", ("mba_dataset.csv", "lainnya"))

                        st.markdown("\n")

                        support_helper = ''' > Support(A) = (Jumlah transaksi mengandung A)/(Transaksi Total) '''
                        confidence_helper = ''' > Confidence(A->B) = Support(AUB)/Support(A)') '''

                        support = st.slider("Masukkan nilai minimal support", min_value=0.001, max_value=0.9, value=0.03, help=support_helper)

                        st.markdown("\n")
                            
                        confidence = st.slider("Masukkan nilai minimal confidence", min_value=0.1, max_value=0.9, value=0.2, help=confidence_helper)

                        st.markdown("---")
                        Authenticator.logout('Log Out', 'sidebar')
                        
                    def main():
                        # title body
                        #st.title("Market Basket Analysis dengan Algoritma Apriori")
                        #st.markdown("\n")

                        df = pd.read_csv(default_csv, header=None, lineterminator="\n")
                        #st.write(df[0].str.split("\,", expand=True).head())

                        #st.markdown("---")

                        st.subheader("Inputs")
                        st.markdown('''
                            **Support** menampilkan transaksi dengan barang yang dibeli bersamaan dalam satu transaksi.\n
                            **Confidence** menampilkan transaksi di mana barang dibeli satu demi satu.\n
                            Support dan Confidence untuk Itemsets A and B dapat direpresentasikan berdasarkan rumus.''')

                        st.markdown("---")

                        inFile = dataFromFile(default_csv)

                        items, rules = runApriori(inFile, support, confidence)

                        i, r = to_str_results(items, rules)

                        st.subheader("Results")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Frequent Itemsets**")
                            st.write(i)

                        with col2:
                            st.markdown("**Frequent Rules**")
                            st.write(r)
                    main()
                
            elif not authentication_status:
                with info2:
                    st.error('Password atau Username tidak benar!')
            else:
                with info2:
                    st.error('Silakan masukkan identitas kamu!')
        else:
            with info2:
                st.error('Username tidak ada, silakan Sign Up!')

except:
    st.warning('Halaman tidak dapat dimuat, coba yang lain!')
