import streamlit as st
import pandas as pd

# TODO: Limitar o número de linhas exibidas. Para 5 talvez?

def trocar_meses_para_portugues(data_str):
    meses_en_pt = {
        'Jan': 'Jan',
        'Feb': 'Fev',
        'Mar': 'Mar',
        'Apr': 'Abr',
        'May': 'Mai',
        'Jun': 'Jun',
        'Jul': 'Jul',
        'Aug': 'Ago',
        'Sep': 'Set',
        'Oct': 'Out',
        'Nov': 'Nov',
        'Dec': 'Dez'    }
    
    # Substituir os meses no formato 'Mês' pelo mês correspondente em português
    for mes_en, mes_pt in meses_en_pt.items():
        data_str = data_str.replace(mes_en, mes_pt)
    return data_str

def mostrar_historico(mydb):
    # Cria uma consulta SQL
    query2 = "SELECT * FROM tb_consumo_itens"

    # Para retornar os dados no formato de dicionário de dados
    cursor2 = mydb.cursor(dictionary=True)
    cursor2.execute("SET time_zone = '-03:00';")
    cursor2.execute(query2)
    resultado2 = cursor2.fetchall()
    cursor2.close()

    # Carregar os dados no DataFrame
    df_data2 = pd.DataFrame(resultado2)

    # Formatar a coluna 'data_cons' para o formato desejado
    df_data2['data_cons'] = pd.to_datetime(df_data2['data_cons']).dt.strftime('%d/%b/%Y - %H:%M')

    # Trocar os nomes dos meses de inglês para português
    df_data2['data_cons'] = df_data2['data_cons'].apply(trocar_meses_para_portugues)

    # Renomear as colunas
    df_data2 = df_data2.rename(columns={
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
    df_data2 = df_data2.sort_values(by="Número", ascending=False)

    # Obter a quantidade disponível de cada produto
    quantidade_query = "SELECT nome_prod, qtde_atual_prod FROM tb_produtos"  # Ajuste a consulta conforme necessário
    cursor2 = mydb.cursor(dictionary=True)
    cursor2.execute(quantidade_query)
    estoque_resultado = cursor2.fetchall()
    cursor2.close()

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
    styled_df2 = df_data2.style.apply(highlight_row, axis=1)

    st.write("# HISTÓRICO DE CONSUMO DE ITENS")

    # Exibir a tabela estilizada
    st.dataframe(styled_df2, use_container_width=True, hide_index=True,
                column_config={
                    "Quantidade de consumo": st.column_config.ProgressColumn("Quantidade de consumo", format="%d", min_value=0, max_value=5),
                })