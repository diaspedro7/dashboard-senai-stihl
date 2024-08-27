import streamlit as st
import pandas as pd
import requests
import json
st. set_page_config(layout="wide")


link = "https://dashboard-senai-default-rtdb.firebaseio.com/"
requisicao = requests.get(f'{link}Produtos/.json')

df_data = pd.read_json(requisicao.text)
df_data = df_data.T

st.write("# VAMO LA GURIZADA, GANHADORES DO INOVA SENAI!")

df_data
