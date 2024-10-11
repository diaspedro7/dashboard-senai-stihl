import streamlit as st
import pandas as pd

def mostrar_grafico_barras(mydb):
    import plotly.express as px
        
    # Cria uma consulta SQL para o gráfico de pizza
    query_pie = "SELECT nome_prod, SUM(qtde_consumo_prod) as total_consumido FROM tb_consumo_itens GROUP BY nome_prod"

    # Para retornar os dados no formato de dicionário de dados
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_pie)
    cursor.fetchall()
    cursor.close()

    

    st.markdown(
    """
    <h5 style="text-align: center;">GRÁFICO COM O CONSUMO DE ITENS EM DETERMINADA DATA</h5>
    """, unsafe_allow_html=True
)


    # Seleção de data
    selected_date = st.date_input("Selecione a data", pd.to_datetime("today"))

    # Cria uma consulta SQL para o gráfico de barras, filtrando pela data selecionada
    query_bar = """
    SELECT nome_prod, DATE(data_cons) as data, SUM(qtde_consumo_prod) as total_consumido 
    FROM tb_consumo_itens 
    WHERE DATE(data_cons) = %s 
    GROUP BY nome_prod, DATE(data_cons)
    """

    # Para retornar os dados no formato de dicionário de dados
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_bar, (selected_date,))
    resultado_bar = cursor.fetchall()
    cursor.close()

    # Carregar os dados no DataFrame
    df_data_bar = pd.DataFrame(resultado_bar)


    # Verifica se há dados para a data selecionada
    if not df_data_bar.empty:
        # Criar o gráfico de barras usando Plotly
        fig_bar = px.bar(df_data_bar, x='nome_prod', y='total_consumido', #title=f'Consumo de itens em {selected_date.strftime("%d/%m/%Y")}',
                        labels={'total_consumido': 'Total Consumido', 'nome_prod': 'Produto'},
                        color_discrete_sequence=['#FF8C00', '#FF6F00', '#FF4500', '#C72C41'],)
        
        fig_bar.update_layout(
            width=600,   # Ajuste a largura do gráfico
            height=300,  # Ajuste a altura do gráfico
            bargap=0.7
        )

        # Exibir o gráfico de barras no Streamlit
        st.plotly_chart(fig_bar, use_container_width=False) 
    else:
        st.warning("Nenhum dado encontrado para a data selecionada.")


def mostrar_grafico_pizza(mydb):
    import plotly.express as px
        
    # Cria uma consulta SQL para o gráfico de pizza
    query_pie = "SELECT nome_prod, SUM(qtde_consumo_prod) as total_consumido FROM tb_consumo_itens GROUP BY nome_prod"

    # Para retornar os dados no formato de dicionário de dados
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_pie)
    resultado_pie = cursor.fetchall()
    cursor.close()

    # Carregar os dados no DataFrame
    df_data_pie = pd.DataFrame(resultado_pie)
    #st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)   

    #st.write("##### GRÁFICO DE ITENS MAIS CONSUMIDOS")
    st.markdown(
    """
    <h5 style="text-align: center;">GRÁFICO DE ITENS MAIS CONSUMIDOS</h5>
    """, unsafe_allow_html=True
)

    # Criar o gráfico de pizza usando Plotly
    fig_pie = px.pie(df_data_pie, 
                 values='total_consumido', 
                 names='nome_prod', 
                 hole=0.3, 
                 color_discrete_sequence=['#FF8C00', '#FF6F00', '#FF4500', '#C72C41'])
    
    fig_pie.update_layout(
            width=600,   # Ajuste a largura do gráfico
            height=420,  # Ajuste a altura do gráfico
        )
    # Exibir o gráfico de pizza no Streamlit
    st.plotly_chart(fig_pie, use_container_width=False, )