import streamlit as st
import pandas as pd
import time
import mysql.connector
from components.historico import mostrar_historico
from components.historico import trocar_meses_para_portugues


#Configuração da página
st.set_page_config(layout="wide", page_icon="🖥️", page_title="Monitoramento de Higiene Stihl",initial_sidebar_state="collapsed")


TEMPO = 10  # 10s eh pouco tempo, o que gasta bastante memoria do pc. Em fase final, mudar para cada 1min

# Conectar ao MySQL
mydb = mysql.connector.connect(
    host="bwd3bxnuruinssz8cgmv-mysql.services.clever-cloud.com",
    user="ulijg1pspqatdfta",
    password="fDLM9NgbEYZTiMOXCZLP",
    database="bwd3bxnuruinssz8cgmv",
)
#Debuggar a conexão
print("Database: " + str(mydb))

mostrar_historico(mydb)

# Tempo de espera para página recarregar
time.sleep(TEMPO)

#Funcao para recarregar a página
st.rerun()