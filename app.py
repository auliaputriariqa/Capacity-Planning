import streamlit as st
import yaml
from streamlit import session_state as session
from hashlib import sha256

# Load users from YAML file
def load_users(filename):
    with open(filename, 'r') as file:
        users = yaml.safe_load(file)
    return users['users']

# Function to authenticate user
def authenticate(username, password, users):
    hashed_password = sha256(password.encode()).hexdigest()
    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            return True
    return False

# Function to show login page
def show_login_page():
    st.title("CapLan - Data Management Team")
    st.markdown("<h2 style='text-align: center; color: black;'>Login</h2>", unsafe_allow_html=True)
    # st.title('Login')
    
    # Membuat kolom untuk memusatkan form login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            if authenticate(username, password, load_users('users.yaml')):
                session['authenticated'] = True
                session['username'] = username
                st.rerun()
            else:
                st.error('Invalid username or password')

# Function to show sidebar navigation
def show_sidebar():
    st.sidebar.title(f"Welcome, {session['username']}")
    page = st.sidebar.selectbox("Pilih Menu", ["Home", "DWH", "REPORT_TMP", "BRINSENTIVE", "Penentuan Model"])
    
    if st.sidebar.button("Logout"):
        session['authenticated'] = False
        st.rerun()
    
    return page

# Main function to run the Streamlit app
def main():
    if 'authenticated' not in session:
        session['authenticated'] = False

    if not session['authenticated']:
        show_login_page()
    else:
        page = show_sidebar()
        
        if page == "Home":
            from server_77.home import show_home
            show_home()
        elif page == "DWH":
            from server_77.DWH import show_page2
            show_page2()
        elif page == "REPORT_TMP":
            from server_77.REPORT_TMP import show_page3
            show_page3()
        elif page == "BRINSENTIVE":
            from server_77.page2 import show_page4
            show_page4()
        elif page == "Penentuan Model":
            from server_77.principle import show_page1
            show_page1()

if __name__ == '__main__':
    main()
