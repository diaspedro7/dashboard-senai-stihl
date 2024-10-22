import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_funcionarios(mydb):
    
    from components.historico import trocar_meses_para_portugues

    query_setores = "SELECT DISTINCT setor_func FROM tb_funcionarios" # Consulta para obter os setores
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_setores)
    resultado_setores = cursor.fetchall()
    cursor.close()

    lista_setores = [setor['setor_func'] for setor in resultado_setores] # Transformar os resultados em uma lista de setores


    setor_selecionado = st.sidebar.selectbox("Selecione o Setor", lista_setores) # Selecionar o setor na barra lateral

    query_funcionarios = "SELECT nome_func FROM tb_funcionarios WHERE setor_func = %s" # Consulta para obter os funcionários do setor selecionado
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_funcionarios, (setor_selecionado,)) # Params: a consulta sql, e o setor selecionado
    resultado_funcionarios = cursor.fetchall()
    cursor.close()

    lista_funcionarios = [func['nome_func'] for func in resultado_funcionarios] # Transformar os resultados em uma lista de funcionários

    funcionario_selecionado = st.sidebar.selectbox("Selecione o Funcionário", lista_funcionarios) # Selecionar o funcionário na barra lateral


    query_matricula = "SELECT matricula_func FROM tb_funcionarios WHERE nome_func = %s AND setor_func = %s"# o %s sao parametros para a consulta
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_matricula, (funcionario_selecionado, setor_selecionado)) #Params: consulta, e os dois parametros pedidos pela consulta
    resultado_matricula = cursor.fetchone()
    cursor.close()

    try: 
        query_consumos = "SELECT * FROM tb_consumo_itens WHERE matricula_func = %s"# o %s sao parametros para a consulta
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(query_consumos, (resultado_matricula['matricula_func'],)) #Params: consulta, e os dois parametros pedidos pela consulta
        resultado_consumos = cursor.fetchall()
        cursor.close()
        
        tb_consumo_func = pd.DataFrame(resultado_consumos)
        # Formatar a coluna 'data_cons' para o formato desejado
        tb_consumo_func['data_cons'] = pd.to_datetime(tb_consumo_func['data_cons']).dt.strftime('%d/%b/%Y - %H:%M')

        tb_consumo_func['data_cons'] = tb_consumo_func['data_cons'].apply(trocar_meses_para_portugues)

        tb_consumo_func = tb_consumo_func.rename(columns={
                "id_cons": "Número",
                "data_cons": "Data de consumo",
                "matricula_func": "Matrícula",
                "nome_func": "Nome do funcionário",
                "setor_func": "Setor",
                "nome_prod": "Nome do produto",
                "qtde_consumo_prod": "Quantidade",
                "un_med_prod": "Unidade de medida",
            })

        tb_consumo_func = tb_consumo_func.sort_values(by="Número", ascending=False)

        soma_quantidade_consumo = tb_consumo_func['Quantidade'].sum()
    except Exception as e:
        print("Erro ao carregar consumo de dados do funcionários")

    col1, col2 = st.columns([2.3, 1])


    with col1:
        st.title(f"{funcionario_selecionado}") # Mostrar o funcionário selecionado


        st.write(f"###### Matrícula: {resultado_matricula['matricula_func']}") # O colchetes serve para pegar apenas o valor, senao iria imprimir o key e o value juntos
        try:
            st.write(f"###### Total de itens consumidos: {soma_quantidade_consumo}")
        except Exception:
            st.write("###### Total de itens consumidos: 0")

        st.divider()
        try:
            st.dataframe(tb_consumo_func, use_container_width=True, hide_index=True, 
                    column_config={
            "Nome do produto": st.column_config.TextColumn(
                "Nome do produto", width=200)})
        except Exception:
            st.write("Vazio")
    


    query_pie = "SELECT nome_prod, SUM(qtde_consumo_prod) as total_consumido FROM tb_consumo_itens where matricula_func = %s GROUP BY nome_prod"

        # Para retornar os dados no formato de dicionário de dados
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(query_pie, (resultado_matricula['matricula_func'],))
    resultado_pie = cursor.fetchall()
    cursor.close()

    # Carregar os dados no DataFrame
    df_data_pie = pd.DataFrame(resultado_pie)
        #st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)   

        #st.write("##### GRÁFICO DE ITENS MAIS CONSUMIDOS")


        # Criar o gráfico de pizza usando Plotly
    try:
        fig_pie = px.pie(df_data_pie, 
                    values='total_consumido', 
                    names='nome_prod', 
                    hole=0.3, 
                    color_discrete_sequence=['#FF8C00', '#FF6F00', '#FF4500', '#C72C41'])
        fig_pie.update_layout(
                width=600,   # Ajuste a largura do gráfico
                height=420,)  # Ajuste a altura do gráfico
    except Exception:
        print("Erro ao construir grafico")
        
    
            
    with col2:
        # Exibir o gráfico de pizza no Streamlit
        st.markdown(
        """
        <h5 style="text-align: center;">GRÁFICO DE ITENS MAIS CONSUMIDOS</h5>
        """, unsafe_allow_html=True
    )
        try:
            st.plotly_chart(fig_pie, use_container_width=False, )
        except Exception:
            st.write("Nenhum produto foi consumido ainda")