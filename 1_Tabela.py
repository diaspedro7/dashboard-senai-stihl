import streamlit as st
from components.database import get_database
from components.tabela import mostrar_tabela
from components.estatisticas import mostrar_grafico_barras
from components.estatisticas import mostrar_grafico_pizza
from components.database import get_database
from components.page_configs import page_config, rerun_page

page_config()

mydb = get_database()

mostrar_tabela(mydb)

st.divider()

col1, col2 = st.columns([1, 1])

# Chamar a função de mostrar a tabela na primeira coluna
with col1:
    mostrar_grafico_barras(mydb) # Função para exibir o gráfico em barras


# Chamar a função de mostrar o gráfico de pizza na segunda coluna
with col2:
    mostrar_grafico_pizza(mydb)  # Função para exibir o gráfico de pizza

rerun_page()
