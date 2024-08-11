import streamlit as st
import pandas as pd
#importacoes
#-------------
#page-congig
st.set_page_config("Cartão de crédito", layout = "wide")
#-------------código funcional

df = pd.read_csv("dataset_limpo.csv")
#isso aqui ja é um dataframe

boleansoPositivos = []
boleanosNegativos = []

def verifica_boleanos(df, dadosElegiveis, dadosNaoElegiveis):

        for index, row in df.iterrows():
                if (row['Unemployed'] == 0 and 
                    row['Own_property'] == 1 and 
                    row['Years_employed']> 3 and 
                    row['Education_type'] == 'Higher education' or 'Incomplete higher' and 
                    row['Num_children'] == 0 and
                    220000 >= row['Total_income'] and
                    25 <= row['Age'] <= 40
                    ) :
                       #print(f"{row['ID']}: tem emprego e tem casa e está empregado a mais de 3 anos")
                         dadosElegiveis.append(row)
                else:
                        #print(f"{row['ID']}: sei la")
                        dadosNaoElegiveis.append(row)
#aqui eu salvo os dois retornos da minhas função
        return dadosElegiveis,dadosNaoElegiveis
        

positvo, negativo = verifica_boleanos(df,boleansoPositivos, boleanosNegativos)

#Aqui acaba o tratamento do pyhton e começa o streamlit
#-------------
# Armazenar os resultados na sessão
st.session_state['dadosNegativos'] = negativo
#-------------
st.header("Esses são os clientes que podem receber o cartão:")
st.dataframe(positvo)
#-------------
st.divider()
st.title("Distribuição de gênero")

totalHomens = []
totalMulheres = []
tratado = positvo

def contaGenero(listahomem, listamulher, data):
         
         dataframe = pd.DataFrame(data)
         for index, row in dataframe.iterrows():
                if (row["Gender"] == 1):
                        listahomem.append(row)
                else:
                        listamulher.append(row)

         return listahomem, listamulher
               
homens, mulheres = contaGenero(totalHomens,totalMulheres,tratado)


def calculaPorcentagemDeGenero(dftotal, dfrefrencial):
       
       total = len(dftotal)
       referencial = len(dfrefrencial)

       valorPercentual = (referencial*100)/total

       return round(valorPercentual,2)


col1, col2 = st.columns(2)
with col1:
        st.write("👩🏽‍💼")
        st.write(f"Desses dados existem {len(mulheres)} mulheres que representam {calculaPorcentagemDeGenero(tratado,mulheres)} x% do total de clientes")

with col2:
         st.write("👨🏾‍🔧")
         st.write(f"Desses dados existem {len(homens)} homens que representam {calculaPorcentagemDeGenero(tratado,homens)} x% do total de clientes")
#-------------
st.divider()
st.title("Educação")
#essa visão aqui mmostra uma divisão por tipo de educação
chartDataEducationtype = df["Education_type"]
chart = chartDataEducationtype.value_counts()
st.bar_chart(chart,color=["#ffaa0088"])

#-------------
st.divider()
#Agora aqui é um componente para baixar um csv com os ID`s

st.header("Aqui você pode fazer o download do ID´s de todos os usuários que estão elegiveis para receber um cartão de crédito 👇🏽")
dfTratado = pd.DataFrame(tratado)
ids = dfTratado["ID"]
csv = ids.to_csv(index= False)
#esse é o componente do botão
st.download_button(
    label="Baixar CSV com IDs",
    data=csv,
    file_name='ids.csv',
    mime='text/csv'
)

#-------------
st.divider()







 
