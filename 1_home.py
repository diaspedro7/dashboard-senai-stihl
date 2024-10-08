import streamlit as st
import pandas as pd
import time
import mysql.connector

st.set_page_config(layout="wide", page_icon="🧼", page_title="Dashboard")

TEMPO = 10  # 10s eh pouco tempo, o que gasta bastante memoria do pc. Em fase final, mudar para cada 1min


mydb = mysql.connector.connect(
    host="bwd3bxnuruinssz8cgmv-mysql.services.clever-cloud.com",
    user="ulijg1pspqatdfta",
    password="fDLM9NgbEYZTiMOXCZLP",
    database="bwd3bxnuruinssz8cgmv",
)

print("Database: " + str(mydb))


def carregar_dados():
    query = "SELECT * FROM tb_produtos"

    # Para retornar os dados no formato de dicionário
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()

    # Carregar os dados no DataFrame
    df_data = pd.DataFrame(resultado)

    if "quant_atual_prod" in df_data.columns:
        df_data["Necessário reposição?"] = df_data["quant_atual_prod"].apply(
            lambda x: "Sim ❌" if x < 5 else "Não ✔️"
        )
    else:
        print("A coluna 'quant_atual_prod' não existe no DataFrame")

    # Renomear as colunas
    df_data = df_data.rename(columns={
        "id_produto": "Identificador",
        "nome_produto": "Nome do produto",
        "quant_atual_prod": "Quantidade",
        "unid_med_prod": "Unidade de medida",
    })
    # Cria uma função que adiciona o "#" ao valor
    def addHash(identificador):
        return f"#{identificador}"

    df_data["Identificador"] = df_data["Identificador"].apply(addHash)

    return df_data


df_data = carregar_dados()
# df_data = df_data.T

# Função para destacar as linhas onde a coluna 'Necessário reposição?' é 'Sim'


def highlight_reposicao(row):
    return ['background-color: rgba(255, 111, 97, 0.1)' if row['Necessário reposição?'] == "Sim ❌" else '' for _ in row]


# Aplicar o estilo ao DataFrame
styled_df = df_data.style.apply(highlight_reposicao, axis=1)

st.write("# QUANTIDADE ATUAL DE PRODUTOS")

# Lembrete: Ajustar o width para ter o mesmo tamanho do título, caso ele seja grande.
st.dataframe(styled_df,   width=800, use_container_width=True,
             column_config={
                 "Quantidade": st.column_config.ProgressColumn("Quantidade", format="%d", min_value=0, max_value=10, width=200),
             }, hide_index=True)

time.sleep(TEMPO)

st.rerun()
