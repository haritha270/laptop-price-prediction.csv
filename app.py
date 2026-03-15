import streamlit as st
import numpy as np
import pickle
import os

# -----------------------------
# LIGHT PINK BACKGROUND WITH GREEN BUTTONS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #ffe6f0, #fff0f5); /* light pink gradient */
}

/* Headings */
h1, h2, h3 {
    color: #2c3e50;
    text-align: center;
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;  /* green button */
    color: white;                /* white text */
    border-radius: 8px;
    height: 40px;
    width: 150px;
}

/* Input fields */
div.stTextInput > div > div > input {
    background-color: #ffffff;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load ML Model
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# -----------------------------
# USER DATABASE FILE
# -----------------------------
USER_DB = "users.pkl"

if not os.path.exists(USER_DB):
    with open(USER_DB, "wb") as f:
        pickle.dump({}, f)

def load_users():
    with open(USER_DB, "rb") as f:
        return pickle.load(f)

def save_users(users):
    with open(USER_DB, "wb") as f:
        pickle.dump(users, f)

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# -----------------------------
# REGISTER PAGE
# -----------------------------
def register_page():
    st.title("📝 Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        users = load_users()
        if username in users:
            st.error("Username already exists")
        else:
            users[username] = password
            save_users(users)
            st.success("Registration successful! Please login.")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()

# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.page = "main"
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Create Account"):
        st.session_state.page = "register"
        st.rerun()

# -----------------------------
# MAIN APPLICATION
# -----------------------------
def main_app():
    st.title("💻 Laptop Price Prediction App")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    st.write("Enter laptop specifications to predict price")

    brand = st.number_input("Brand (Encoded value)", min_value=0)
    processor_speed = st.number_input("Processor Speed (GHz)", min_value=0.0)
    ram_size = st.number_input("RAM Size (GB)", min_value=1)
    storage_capacity = st.number_input("Storage Capacity (GB)", min_value=0)
    screen_size = st.number_input("Screen Size (inches)", min_value=0.0)
    weight = st.number_input("Weight (kg)", min_value=0.0)

    performance_index = processor_speed * ram_size

    features = np.array([[brand, processor_speed, ram_size,
                          storage_capacity, screen_size,
                          weight, performance_index]])

    features_scaled = scaler.transform(features)

    if st.button("Predict Price"):
        prediction = model.predict(features_scaled)
        st.success(f"Estimated Laptop Price: ₹ {round(prediction[0],2)}")

# -----------------------------
# PAGE ROUTING
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "main":
    if st.session_state.logged_in:
        main_app()
    else:
        st.session_state.page = "login"
        st.rerun()