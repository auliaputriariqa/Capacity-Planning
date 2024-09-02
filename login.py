import streamlit as st

# Fungsi untuk memeriksa login
def check_login(username, password):
    # Contoh validasi sederhana (di dunia nyata, sebaiknya menggunakan database)
    if username == "admin" and password == "admin123":
        return True
    else:
        return False

# Judul aplikasi
st.title("Aplikasi Login dengan Streamlit")

# Membuat form login
def login_form():
    st.markdown("<h2 style='text-align: center; color: black;'>Login</h2>", unsafe_allow_html=True)
    
    # Membuat kolom untuk memusatkan form login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Membuat form login
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        
        login_button = st.button("Login")

    return login_button, username, password

# Tampilkan form login dan tangani input
login_button, username, password = login_form()

# Cek apakah tombol login diklik
if login_button:
    if check_login(username, password):
        st.success(f"Selamat datang, {username}!")
        st.markdown("<h3 style='text-align: center; color: green;'>Login berhasil!</h3>", unsafe_allow_html=True)
    else:
        st.error("Login gagal. Periksa username dan password Anda.")
