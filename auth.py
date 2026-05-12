import streamlit as st

# =====================================================
# PASSWORD
# =====================================================

APP_PASSWORD = "ronald371011"

# =====================================================
# LOGIN CHECK
# =====================================================

def check_login():

    if "login_berhasil" not in st.session_state:
        st.session_state["login_berhasil"] = False

    if not st.session_state["login_berhasil"]:

        st.title("Login Web")

        password = st.text_input(
            "Masukkan Password",
            type="password"
        )

        if st.button("Masuk"):

            if password == APP_PASSWORD:

                st.session_state["login_berhasil"] = True

                st.rerun()

            else:

                st.error("Password salah.")

        st.stop()