import streamlit as st
import pandas as pd
import time
import mysql.connector
from components.tabela import mostrar_tabela
from components.historico import mostrar_historico
from components.historico import trocar_meses_para_portugues
from components.estatisticas import mostrar_grafico_barras
from components.estatisticas import mostrar_grafico_pizza

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


# Título (Em duvida se boto ou nao)
# st.markdown(
#     """
#     <h1 style='text-align: center;'>MONITORAMENTO DE ITENS DE HIGIENE STIHL</h1>
#     """,
#     unsafe_allow_html=True
# )
# st.divider()

mostrar_tabela(mydb)

# Historico de Consumo de Itens
#mostrar_historico(mydb)

st.divider()

col1, col2 = st.columns([1, 1])

# Chamar a função de mostrar a tabela na primeira coluna
with col1:
    mostrar_grafico_barras(mydb) # Função para exibir o gráfico em barras


# Chamar a função de mostrar o gráfico de pizza na segunda coluna
with col2:
    mostrar_grafico_pizza(mydb)  # Função para exibir o gráfico de pizza




# Tempo de espera para página recarregar
time.sleep(TEMPO)

#Funcao para recarregar a página
st.rerun()
