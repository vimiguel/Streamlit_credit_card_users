import streamlit as st
import pandas as pd
#-------------- 
# Acessar a lista armazenada na sessão
if 'dadosNegativos' in st.session_state:
    dadosNaoElegiveis = st.session_state['dadosNegativos']
else:
    dadosNaoElegiveis = []
#-------------- 
df = pd.DataFrame(dadosNaoElegiveis)
#aqui eu trato dessa forma porque nao é um csv igual no outro, é uma lista
#-------------- 
# Mostrar os dados não elegíveis na segunda página
st.title("Explorar conjunto de dados")
st.write("Dados Não Elegíveis:")

if 'Age' not in df.columns:
    st.error("Voce recarregou a página e os calculos foram perdidosm volte a pasta Elegiveis para recarregar os dados corretamente.")
else:
    # Obter os valores mínimo e máximo da coluna 'Age'
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())

    #ober valores de renda
    min_income = int(df["Total_income"].min())
    max_income = int(df["Total_income"].max())

    # Mapear os valores de 'Gender' para opções legíveis
    options = ['Todos', 'Homem', 'Mulher']

    # Criar duas colunas para o layout

    col1, col2 = st.columns(2)
    # Colocar o selectbox na primeira coluna
    with col1:
        gender_filter = st.selectbox('Selecione o gênero para filtrar:', options=options)

    # Colocar o slider na primeira coluna
    with col1:
        age_filter = st.slider(
            label='Selecione a idade:',
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
            step=1,
            format="%d anos"
        )

    #slider de renda
    with col1:
        income_filter = st.slider(
            label= "Seleciona a renda anual do usuário", 
            min_value=  min_income, 
            max_value= max_income,
            value= (min_income, max_income),
            step=1,
            format="%d dolares por ano"
    ) 
    with col1:
        tem_emprego = st.selectbox("Tem emprego?", options= ["Sim", "Não"])

    with col1:
        num_children = df[["Num_children"]]
        has_child = st.selectbox("selecionar se essa pessoa tem filhos", options = ["Sim", "Não"])

    with col1:
        family_status = df["Family_status"].unique()
        #aqui eu retorno os valore únicos dentro de uma Series, se eu salvasse como um dataframe não iria funcioanr
        select_family_status = st.selectbox("Selecione o status civil dos usuários", options= family_status)   

    with col1:
         yearsEmployed = df["Years_employed"]
         yearsEmployed = st.selectbox("Selecione usuários que estão empregados a", options=["Mais de um ano", "Mais de 3 anos", "Mais de 5 anos"], index=None)

    # Aplicar os filtros no DataFrame - esse é o método que aplica os filtros
    def apply_filters(df, gender_filter, age_filter, select_family_status, has_child,  yearsEmployed, income_filter):
        filtered_df = df.copy()

        # Filtrar por gênero
        if gender_filter == 'Homem':
            filtered_df = filtered_df[filtered_df['Gender'] == 1]
        elif gender_filter == 'Mulher':
            filtered_df = filtered_df[filtered_df['Gender'] == 0]
        elif gender_filter == 'Todos':
            filtered_df = filtered_df

        # Filtrar por idade
        filtered_df = filtered_df[(filtered_df['Age'] >= age_filter[0]) & (filtered_df['Age'] <= age_filter[1])]

        # Filtrar por renda
        filtered_df = filtered_df[(filtered_df['Total_income'] >= income_filter[0]) & (filtered_df['Total_income'] <= income_filter[1])]

        # Filtrar por family status
        filtered_df = filtered_df[filtered_df["Family_status"] == select_family_status]

        #filtra por desemprego
        if tem_emprego == "Sim":
                filtered_df = filtered_df[filtered_df["Unemployed"]==0]
        elif tem_emprego == "Não":
                filtered_df = filtered_df[filtered_df["Unemployed"]==1]

        

        #filtra por estado civil
      
        #eu apaso uma opração de comparação para filtrar dentro do dataframe
        #só essa linha faz funcionar porque passei o family status no paremtros

        #filtrar se tem filho ou não
        if has_child == "Sim":
            filtered_df = filtered_df[filtered_df["Num_children"] > 0]

        elif has_child == "Nao":
             filtered_df = filtered_df[filtered_df["Num_children"] == 0]   

        #filtrar por tempo empregado
        
        if yearsEmployed == "Mais de um ano":
             filtered_df = filtered_df[filtered_df["Years_employed"] >= 1 ]
           
        elif yearsEmployed == "Mais de 3 anos":
             filtered_df = filtered_df[filtered_df["Years_employed"] >= 3 ]
       
        elif yearsEmployed == "Mais de 5 anos":
            filtered_df = filtered_df[filtered_df["Years_employed"] >= 5 ]

        elif yearsEmployed == "":
            filtered_df = filtered_df[filtered_df["Years_employed"] >= 0 ]
           
        return filtered_df
    

    filtered_df = apply_filters(df, gender_filter, age_filter, select_family_status, has_child, yearsEmployed, income_filter)

    # Colocar o DataFrame filtrado na segunda coluna
    with col2:
        st.write("Dados Filtrados:")
        st.dataframe(filtered_df, height=720)
        ids = filtered_df["ID"]
        #o código acima seleciona a coluna ID

        csv = ids.to_csv(index= True)
        st.download_button(
        label="Baixar CSV com IDs",
        data=csv,
        file_name='ids-hipotese.csv',
        mime='text/csv'
    )

st.divider()

st.title("🚨 Em caso de incosistência dos dados, relembre de clincar na página de elegiveis e fazer um novo filtro 🚨")



    


