import streamlit as st
import requests
import pandas as pd

st.title("Weather Forecaster")

st.write("Enter today's weather conditions to predict tomorrow's temperature.")

# Input fields for weather data
today_temp = st.number_input("Today's Temperature (°C)", value=20.0)
humidity = st.number_input("Humidity (%)", value=60.0)
wind_speed = st.number_input("Wind Speed (km/h)", value=10.0)

if st.button("Predict Tomorrow's Temperature"):
    try:
        payload = {
            "today_temp": today_temp,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
        response = requests.post(
            "http://backend:8000/predict",
            json=payload
        )
        response.raise_for_status()
        prediction = response.json()["prediction"]
        st.subheader("Prediction")
        st.write(f"Tomorrow's predicted temperature is: **{prediction[0]:.2f}°C**")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")