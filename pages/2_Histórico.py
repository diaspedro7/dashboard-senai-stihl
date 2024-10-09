import streamlit as st
import pandas as pd
import time
import mysql.connector
import locale

# Configuração para PT-BR
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

TEMPO = 10  # 10s eh pouco tempo, o que gasta bastante memoria do pc. Em fase final, mudar para cada 1min

#Configuração da página
st.set_page_config(layout="wide", page_icon="🧼", page_title="Dashboard")

# Conectar ao MySQL
mydb = mysql.connector.connect(
    host="bwd3bxnuruinssz8cgmv-mysql.services.clever-cloud.com",
    user="ulijg1pspqatdfta",
    password="fDLM9NgbEYZTiMOXCZLP",
    database="bwd3bxnuruinssz8cgmv",
)
# Cria uma consulta SQL
query = "SELECT * FROM tb_consumo_itens"

# Para retornar os dados no formato de dicionário de dados
cursor = mydb.cursor(dictionary=True)
cursor.execute("SET time_zone = '-03:00';")
cursor.execute(query)
resultado = cursor.fetchall()
cursor.close()

# Carregar os dados no DataFrame
df_data = pd.DataFrame(resultado)

# Formatar a coluna 'data_cons' para o formato desejado
df_data['data_cons'] = pd.to_datetime(df_data['data_cons']).dt.strftime('%d/%b/%Y - %H:%M')


#Renomear as colunas
df_data = df_data.rename(columns={
        "id_cons": "Número",
        "data_cons": "Data de consumo",
        "matricula_func": "Matrícula do funcionário",
        "nome_func": "Nome do funcionário",
        "setor_func": "Setor do funcionário",
        "nome_prod": "Nome do produto",
        "qtde_consumo_prod": "Quantidade de consumo",
        "un_med_prod": "Unidade de medida",
})

# Ordena a tabela pela coluna 'id_cons' em ordem decrescente
df_data = df_data.sort_values(by="Número", ascending=False)


st.write("# HISTÓRICO DE CONSUMO DE ITENS")

st.dataframe(df_data, use_container_width=True, hide_index=True,column_config={
    "Quantidade de consumo": st.column_config.ProgressColumn("Quantidade de consumo", format="%d", min_value=0, max_value=5),
})

# Tempo de espera
time.sleep(TEMPO)

#Funcao para recarregar a página
st.rerun()
