import streamlit as st
import pandas as pd
import time
import mysql.connector
import locale

# Configuração para PT-BR
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

TEMPO = 10  # Tempo de atualização da página

# Configuração da página
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

# Renomear as colunas
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

# Obter a quantidade disponível de cada produto
quantidade_query = "SELECT nome_prod, qtde_atual_prod FROM tb_produtos"  # Ajuste a consulta conforme necessário
cursor = mydb.cursor(dictionary=True)
cursor.execute(quantidade_query)
estoque_resultado = cursor.fetchall()
cursor.close()

# Criar um DataFrame para as quantidades em estoque
df_estoque = pd.DataFrame(estoque_resultado)

# Verificar se cada produto está esgotado
def highlight_row(row):
    if row['Nome do produto'] in df_estoque['nome_prod'].values:
        estoque = df_estoque.loc[df_estoque['nome_prod'] == row['Nome do produto'], 'qtde_atual_prod'].values[0]
        if estoque == 0:
            return ['background-color: rgba(255, 111, 97, 0.1)'] * len(row)
    return [''] * len(row)

# Aplica a função de destaque
styled_df = df_data.style.apply(highlight_row, axis=1)

st.write("# HISTÓRICO DE CONSUMO DE ITENS")

# Exibir a tabela estilizada
st.dataframe(styled_df, use_container_width=True, hide_index=True,
              column_config={
                  "Quantidade de consumo": st.column_config.ProgressColumn("Quantidade de consumo", format="%d", min_value=0, max_value=5),
              })

# Tempo de espera
time.sleep(TEMPO)

# Função para recarregar a página
st.rerun()
