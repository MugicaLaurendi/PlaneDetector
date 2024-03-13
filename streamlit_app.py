import altair as alt
import pandas as pd
import streamlit as st
import requests
"""
# Bienvenue sur mon API Wine

Ce streamlit est un exercice

"""

alcohol = st.slider('Alcohol', 8.0, 15.0, 10.0,step=0.1)
sulphates = st.slider('Sulphates', 0.0, 3.0, 1.0,step=0.1)
citric_acid = st.slider('Citric acid', 0.0, 1.0, 0.5,step=0.01)

response = requests.get(f"https://1f07-82-126-158-181.eu.ngrok.io/lr_red_wine?alcohol={alcohol}&sulphates={sulphates}&citric_acid={citric_acid}").json()

quality = round(response["Wine quality"])

st.write(f"## Wine quality : {quality}/10")
