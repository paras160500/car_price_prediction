import streamlit as st
import pickle
import pandas as pd

# Load saved data and pipeline
dict_data = pickle.load(open("dict_data.pkl", "rb"))
pipe = pickle.load(open("lrm.pkl", "rb"))

# Extract lists
company_list = dict_data['company_list']
fuel_type_list = dict_data['fuel_type_list']
car_model_list = dict_data['car_model_list']

# ---------------- UI ---------------- #
st.set_page_config(page_title="🚗 Car Price Predictor", layout="centered")

# Apply custom CSS for styling
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            color: #333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stSelectbox>div>div>div>input {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ddd;
        }
        .stNumberInput>div>div>div>input {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ddd;
        }
        .stSlider>div>div>div>input {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ddd;
        }
        .stTextInput>div>div>div>input {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚗 Car Price Predictor")
st.markdown("Predict the price of your car in **Rupees** easily!")

st.markdown("---")

# --- Car Selection --- #
st.subheader("Select Your Car Details")

# Company selection
company = st.selectbox("🏢 Car Company:", ["Select a company"] + company_list)

# Model selection depends on company
if company != "Select a company":
    model_options = [m for m in car_model_list if company in m]
    model = st.selectbox("🚘 Car Model:", model_options)
else:
    model = st.selectbox("🚘 Car Model:", [], disabled=True)

# Year and Kms
col1, col2 = st.columns(2)
with col1:
    year = st.select_slider(
        "📅 Year Made:",
        options=list(range(1995, 2026)),
        value=2008
    )
with col2:
    kms_driven = st.number_input("🛣️ Kms Driven:", min_value=0, value=5000, step=100)

# Fuel type
fuel = st.selectbox("⛽ Fuel Type:", fuel_type_list)

st.markdown("---")

# Button to predict price
if st.button("💰 Check Price"):
    if company == "Select a company" or not model:
        st.warning("Please select a valid company and model to predict the price.")
    else:
        # Prepare data for prediction
        input_data = pd.DataFrame([{
            'name': model,
            'company': company,
            'year': year,
            'kms_driven': kms_driven,
            'fuel_type': fuel
        }])
        predicted_price = pipe.predict(input_data)[0]
        st.success(f"🎉 Estimated Price: **₹ {int(predicted_price):,}**")

st.markdown("---")
st.markdown("Made with ❤️ by You | Simple and intuitive UI for easy car price prediction")
