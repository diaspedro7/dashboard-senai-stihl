import streamlit as st
import pandas as pd


def mostrar_tabela(mydb):
        
    # Cria uma consulta SQL
    query = "SELECT * FROM tb_produtos"

    # Para retornar os dados no formato de dicionário de dados
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()

    # Carregar os dados no DataFrame
    df_data = pd.DataFrame(resultado)

    # Cria uma coluna 'Necessário reposição?' e o valor que possuirá dependendo do valor da coluna 'qtde_atual_prod'
    if "qtde_atual_prod" in df_data.columns:
            df_data["Necessário reposição?"] = df_data["qtde_atual_prod"].apply(
                lambda x: "Sim ❌" if x < 3 else "Não ✔️" #Se a quantidade de produto for <3, o valor é 'Sim ❌', caso contrário, 'Não ✔️'
            )
    else:
            print("A coluna 'quant_atual_prod' não existe no DataFrame")


    # Renomear as colunas para ficarem mais bonitas
    df_data = df_data.rename(columns={
            "id_prod": "Identificador",
            "nome_prod": "Nome do produto",
            "qtde_atual_prod": "Quantidade",
            "un_med_prod": "Unidade de medida",
    })

    # Cria uma função que adiciona o "#" ao identificador para ficar mais bonito
    

    #Aplica a função addHash na coluna 'Identificador'
    df_data["Identificador"] = df_data["Identificador"].apply(addHash)

    df_data = df_data.sort_values(by="Necessário reposição?", ascending=False)



    # Função para destacar as linhas com a cor vermelha onde a coluna 'Necessário reposição?' é 'Sim'
    def highlight_reposicao(row):
        return ['background-color: rgba(255, 111, 97, 0.1)' if row['Necessário reposição?'] == "Sim ❌" else '' for _ in row]

    # Aplica a funcao de destaque das linhas com a cor vermelha
    styled_df = df_data.style.apply(highlight_reposicao, axis=1)

    # Titulo
    st.markdown(
    """
    <h3 style="text-align: center;">QUANTIDADE ATUAL DE PRODUTOS</h3>
    """, unsafe_allow_html=True
)
    # Lembrete: Ajustar o width para ter o mesmo tamanho do título, caso ele seja grande.
    #Tabela
    st.dataframe(styled_df,   width=800,use_container_width=True,
                column_config={
                    "Quantidade": st.column_config.ProgressColumn("Quantidade", format="%d", min_value=0, max_value=5, #width=200
                                                                  ),
                }, hide_index=True)

def addHash(identificador):
            return f"#{identificador}"