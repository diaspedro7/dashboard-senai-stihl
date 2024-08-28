import streamlit as st
import pandas as pd
import requests
import json
from io import StringIO
import time

st.set_page_config(layout="wide", page_icon="🧼", page_title="Dashboard")

TEMPO = 10  # 10s eh pouco tempo, o que gasta bastante memoria do pc. Em fase final, mudar para cada 1min

link = "https://dashboard-senai-default-rtdb.firebaseio.com/"
requisicao = requests.get(f'{link}Produtos/.json')

df_data = pd.read_json(StringIO(requisicao.text))
df_data = df_data.T

st.write("# VAMO LA GURIZADA, GANHADORES DO INOVA SENAI!")

# Lembrete: Ajustar o width para ter o mesmo tamanho do título, caso ele seja grande.
st.dataframe(df_data, width=800, use_container_width=True, column_config={})

time.sleep(TEMPO)

st.rerun()
