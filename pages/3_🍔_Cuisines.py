#-----------Bibliotecas------------------------------------------------------------#
from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np
import streamlit as st
import inflection
import unidecode
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from geopy.geocoders import Nominatim
from IPython.display import display
from streamlit_folium import folium_static


st.set_page_config(page_title="Culinária", page_icon="🍔", layout="wide")
#-------------Funções--------------------------------------------------------------#

#1. Para colocar o nome dos países com base no código de cada país
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    ''' Esta função realiza a troca dos códigos constantes na coluna "Country Code" pelo nome do páis.
        Tipos de função:
        1. Troca de código por nome
                
        Input: Dicionário 
        Output: Dicionário'''
    return COUNTRIES[country_id]

#2. Para renomear as colunas do DataFrame
def rename_columns(df):
    ''' Esta função renomeia todas as colunas.
        Tipos de função:
        1. Renomeia os nomes das colunas
        2. Retira espaçoes em branco
        3. Uni o nome com o "_"
                
        Input: DataFrame 
        Output: DataFrame'''
    df = df.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#3. Para limpeza do DF
def clean_code (df):
    ''' Esta função realiza a limpeza dos dados.
        Tipos de função:
        1. Retira linhas nulas coluna a coluna;
        2. Retira tipo de culinária descrito como: "culinária mineira" e "mineira" do dataframe;
        3. Elimina linhas nulas;
        4. Elimina colunas nulas;
        5. Elimina colunas que possam conter nan ou nulo;
        6. Elimina colunas linhas duplicadas;
        7. Transformando todos os elementos da coluna Cuisines em string;
        8. Selecionar sempre a primeira opção da linhas que contenha mais de um tipo de culinária para quando da avaliação de valores;
        9. Aciona a função que renomeia as colunas do df original.
                
        Input: DataFrame 
        Output: DataFrame'''
    df = df.loc[df["Restaurant ID"].notnull(), :]
    df = df.loc[df["Restaurant Name"].notnull(), :]
    df = df.loc[df["Country Code"].notnull(), :]
    df = df.loc[df["City"].notnull(), :]
    df = df.loc[df["Address"].notnull(), :]
    df = df.loc[df["Locality"].notnull(), :]
    df = df.loc[df["Locality Verbose"].notnull(), :]
    df = df.loc[df["Longitude"].notnull(), :]
    df = df.loc[df["Latitude"].notnull(), :]
    df = df.loc[df["Cuisines"].notnull(), :]
    df = df.loc[df["Average Cost for two"].notnull(), :]
    df = df.loc[df["Currency"].notnull(), :]
    df = df.loc[df["Has Table booking"].notnull(), :]
    df = df.loc[df["Has Online delivery"].notnull(), :]
    df = df.loc[df["Is delivering now"].notnull(), :]
    df = df.loc[df["Switch to order menu"].notnull(), :]
    df = df.loc[df["Price range"].notnull(), :]
    df = df.loc[df["Aggregate rating"].notnull(), :]
    df = df.loc[df["Rating color"].notnull(), :]
    df = df.loc[df["Rating text"].notnull(), :]
    df = df.loc[df["Votes"].notnull(), :]


    # Lista de termos a serem removidos
    df = df[~df['Cuisines'].str.contains('comida mineira|mineira', case=False)]
    linhas_nulas = df.isnull().any(axis=1)
    colunas_nulas = df.isnull().sum()
    colunas_nan_none = df.isna().any()
    df = df.dropna(axis=0, how='any', inplace=False)
    df = df.dropna(axis=1, how='any', inplace=False)
    df = df.drop_duplicates()
    df["Cuisines"] = df["Cuisines"].astype(str)
    df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: str(x).split(",")[0])
    df["Country Code"] = df["Country Code"].map(country_name)
    df = rename_columns(df)
    return df

#4. Função para criar o filtro de quantidade de restaurantes
def filter_restaurants(df, num_restaurants):
    ''' Esta função realiza a filtragem de quantidade de resaurantes a serem apresentados nos df e gráficos da página.
        Tipos de função:
        1. Verificar a quantidade de restaurantes no DF;
        2. Adiociona limite dentro da amplitude numérica de restaurantes;
        3. Retorna um filtro de df com base na quantidade de restaurantes.
                
        Input: DataFrame 
        Output: Lista de DataFrame'''
    restaurant_count = df['restaurant_id'].value_counts()
    filtered_restaurants = restaurant_count[restaurant_count.isin(range(1, num_restaurants+1))].index
    filtered_df = df[df['restaurant_id'].isin(filtered_restaurants)]
    return filtered_df

#5. Função que calcula avaliação média e preço médio pra 2 das culinária por país
def calcular_metrica_culinaria(culinaria, col, nome_coluna):
    '''A função em si não retorna nenhum valor específico, mas realiza as seguintes ações:

        1. Filtra o DataFrame df com base na culinária fornecida.
        2. Calcula as médias das colunas relevantes usando groupby e mean.
        3. Ordena os resultados com base na coluna "aggregate_rating" em ordem descendente.
        4. Seleciona a primeira linha dos resultados (com a maior avaliação média).
        5. Extrai os valores relevantes, como a avaliação média, país, restaurante e preço.
        6. Exibe as métricas usando o método col.metric do objeto col.
        O principal objetivo da função é simplificar o código e evitar repetições desnecessárias, facilitando o cálculo e exibição das         métricas para várias culinárias diferentes
        Input: DataFrame
        Output: Tipo de culinária conforme demandas escolhidas'''
    df_culinaria_avg = df.loc[df["cuisines"] == culinaria, :]
    df_culinaria_avg = df_culinaria_avg.loc[:, ["aggregate_rating", "average_cost_for_two", "country_code", "restaurant_name", "cuisines"]].groupby(["country_code", "restaurant_name", "cuisines"]).mean().sort_values(["aggregate_rating"], ascending=False).reset_index()
    df_culinaria_avg.columns = ["País", "Restaurante", "Culinária", "Avaliação média", "Preço médio para 2"]
    df_culinaria_avg = df_culinaria_avg.iloc[0]
    culinaria_media = df_culinaria_avg["Avaliação média"]
    pais = df_culinaria_avg["País"]
    restaurante = df_culinaria_avg["Restaurante"]
    preco = df_culinaria_avg["Preço médio para 2"]
    col.metric(nome_coluna, f'{culinaria_media}/5.0', help=f'País: {pais} \n\nRestaurante: {restaurante} \n\nPreço: {preco}')

#6. Função para avaliação de média de reço pra 2 e média de avaliação dos restauranyes por tipo de culinária e cidades
def City_Avg_Cost_for_two (df):
    '''A função realiza a média da avaliação média agregada, votos e o preço médio pra dois por restaurantes, país, cidade e culiária:
    1. Define o DF de armazenamento das colunas que serão utilizadas;
    2. Agrupa os dados por restaurante, país, cidade e culinária;
    3. Calcula a média de preço médio para 2, avaliação agregada e votos;
    4. Ordena por média da avaliação agregada e por culinária;
    5. Retorna um dataframe que exibirá a quantidade de restaurantes conforme filtro da apresentação.
    
    Input: Dataframe
    Output: Dataframe
    '''
    df_City_Avg_Cost_for_two = df.loc[:, ["average_cost_for_two", "aggregate_rating", "votes", "restaurant_id", "restaurant_name","country_code", "city", "cuisines"]].groupby(["restaurant_id", "restaurant_name","country_code", "city", "cuisines"]).mean().sort_values(["aggregate_rating", "cuisines"], ascending=[False,True]).reset_index()
    df_City_Avg_Cost_for_two = df_City_Avg_Cost_for_two.round({"average_cost_for_two": 2})
    df_City_Avg_Cost_for_two = df_City_Avg_Cost_for_two.round({"aggregate_rating": 2})
    df_City_Avg_Cost_for_two.columns = ["Restaurante_id", "Restaurante","País", "Cidade", "Culinária", "Preço pra 2", "Média de avaliação", "Média de votos"]
    return df_City_Avg_Cost_for_two.head(num_restaurants)

    
#7. Função para exibição de gráfico contendo as melhores e piores culinárias com quantidade de apresentação definida pelo usuário
def plot_grafico_culinarias(col, titulo, ascending):
    '''Nessa abordagem, a função plot_grafico_culinarias recebe o objeto col, o título do gráfico e um valor booleano para indicar se a        classificação deve ser ascendente ou descendente. A função realiza as seguintes ações:

    1. Gera o título do gráfico com base no parâmetro titulo fornecido.
    2. Filtra o DataFrame filtered_df para obter as médias das avaliações para cada culinária.
    3. Ordena os resultados com base na coluna "aggregate_rating" usando a ordem especificada pelo parâmetro ascending.
    4. Renomeia as colunas relevantes.
    5. Arredonda as médias das avaliações para duas casas decimais.
    6. Cria um gráfico de barras usando a biblioteca Plotly Express.
    7. Atualiza as posições e valores dos rótulos dentro das barras.
    8. Atualiza os textos das anotações do gráfico.
    9. Define o modo de agrupamento das barras.
    10. Exibe o gráfico usando o método col.plotly_chart.
    
    Input: Dataframe
    Output: Gráfico
    '''
    title = f'Top {num_restaurants} {titulo}'
    st.subheader(title)
    df_Restaurant_Cuisines_Avg = filtered_df.loc[:, ["cuisines", "aggregate_rating"]].groupby(["cuisines"]).mean().sort_values("aggregate_rating", ascending=ascending).reset_index()
    df_Restaurant_Cuisines_Avg.columns = ["Culinária", "Avaliações médias"]
    df_Restaurant_Cuisines_Avg = df_Restaurant_Cuisines_Avg.round({"Avaliações médias": 2})
    fig = px.bar(df_Restaurant_Cuisines_Avg.head(num_restaurants), x="Culinária", y="Avaliações médias")
    fig = fig.update_traces(textposition="inside", text=df_Restaurant_Cuisines_Avg["Avaliações médias"])
    fig = fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig = fig.update_layout(barmode="group")
    return col.plotly_chart(fig, use_container_width=True)

#8. Esta função apresenta gráfico de restaurantes que realizam delivery e que estão realizado delivery no momento
def Restaurant_Cuisines_On_delivery_Now (df):
    '''A função Restaurant_Cuisines_On_delivery_Now recebe um DataFrame df como entrada e retorna um gráfico de barras interativo gerado pela biblioteca Plotly Express.. A função realiza as seguintes ações:

    1. Gera o título do gráfico com base na variável num_restaurants.
    2. Exibe o título como um subcabeçalho usando st.subheader.
    3. Filtra o DataFrame filtered_df para obter os restaurantes que fazem entrega e aceitam pedidos online, utilizando as colunas "has_online_delivery" e "is_delivering_now".
    4. Seleciona as colunas relevantes ("country_code", "restaurant_id", "cuisines").
    5. Agrupa os dados por país e culinária, calculando a quantidade de restaurantes únicos para cada combinação.
    6. Ordena os resultados com base na quantidade de restaurantes ("restaurant_id") em ordem descendente.
    7. Renomeia as colunas relevantes.
    8. Cria um gráfico de barras usando a biblioteca Plotly Express.
    9. Configura o eixo x como "Culinária", o eixo y como "Restaurante" e a cor como "País".
    10. Atualiza as posições e valores dos rótulos dentro das barras.
    11. Atualiza os textos das anotações do gráfico.
    12. Define o modo de agrupamento das barras.
    13. Retorna o objeto do gráfico.
   
    Input: Dataframe
    Output: Gráfico '''
    title_delivery = f'{num_restaurants} primeiros países em Maior quantidade de Restaurantes que Fazem Entrega e aceitam Pedidos Online por tipo de culinária'                                                                                             
    st.subheader( title_delivery )
    df_Restaurant_Cuisines_On_delivery_Now = filtered_df.loc[(filtered_df["has_online_delivery"] == 1) & (filtered_df["is_delivering_now"] == 1), :]
    df_Restaurant_Cuisines_On_delivery_Now = df_Restaurant_Cuisines_On_delivery_Now.loc[:, ["country_code", "restaurant_id", "cuisines"]].groupby(["country_code", "cuisines"]).nunique().sort_values("restaurant_id", ascending=False).reset_index()
    df_Restaurant_Cuisines_On_delivery_Now.columns = ["País", "Culinária", "Restaurante"]
    fig = px.bar(df_Restaurant_Cuisines_On_delivery_Now.head(num_restaurants), x="Culinária", y="Restaurante", color="País")
    fig = fig.update_traces(textposition="inside", text=df_Restaurant_Cuisines_On_delivery_Now["Restaurante"])
    fig = fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig = fig.update_layout(barmode="group")
    return fig


#-------------Importando arquivo---------------------------------------------------#
df_raw = pd.read_csv("dataset/zomato.csv")

df = df_raw.copy()


#------------Limpeza---------------------------------------------------------------#

df = clean_code(df)

# ==========================================================================================================
# Barra Lateral
# ==========================================================================================================

st.title('🍔 Visão Culinária')

image = Image.open( "logo.png" )
st.sidebar.image( image, width=300 )

st.sidebar.markdown( '# Fome Zero Company' )

st.sidebar.markdown( """---""" )

st.sidebar.markdown( '# Filtros' )

country_options = st.sidebar.multiselect( 
    'Selecione o país que deseja visualizar o restaurante',
    ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'], 
    default=['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'])


# Selecionar a quantidade de restaurantes visíveis usando o slider
num_restaurants = st.sidebar.slider('Selecione a quantidade de restaurantes que deseja visualizar', 1, 20, 10 )


# Selecionar tipo de culinária
cuisines_options = st.sidebar.multiselect('Escolha os Tipos de Culinária', df.loc[:, "cuisines"].unique().tolist(), default=['Home-made','BBQ','Japanese','Brazilian','Arabian','American','Italian','Spanish'])  


st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Eat wherever you are!' )

# Filtro de país
df = df.loc[(df['country_code'].isin( country_options )), :]

#Filtro de quantidade de restaurantes
# Filtrar o DataFrame com base na quantidade selecionada
filtered_df = filter_restaurants(df, num_restaurants)

#Filtro de culinária
linhas_selec = df['cuisines'].isin(cuisines_options)
df=df.loc[linhas_selec,:]

# =======================================
# Layout no Streamlit
# =======================================# 

with st.container():
    st.subheader( 'Melhor avaliadas' )
    col1, col2, col3, col4, col5 = st.columns( 5, gap='large')
    
    with col1:
        calcular_metrica_culinaria("Italian", col1, "Culinária Italiana")

    with col2:
        calcular_metrica_culinaria("American", col2, "Culinária Americana")

    with col3:
        calcular_metrica_culinaria("Arabian", col3, "Culinária Árabe")

    with col4:
        calcular_metrica_culinaria("Japanese", col4, "Culinária Japonesa")

    with col5:
        calcular_metrica_culinaria("Spanish", col5, "Culinária Espanhola")

with st.container():
    title_top = f'Top {num_restaurants} Restaurantes'
    st.subheader( title_top )
    st.dataframe( City_Avg_Cost_for_two (df) )

with st.container():
    st.subheader( 'Melhor e pior culinária avaliada' )
    col1, col2 = st.columns( 2, gap='large')
    
    with col1:
        plot_grafico_culinarias(col1, "melhores", False)
        
    with col2:
        plot_grafico_culinarias(col2, "piores", True)

with st.container():
    fig = Restaurant_Cuisines_On_delivery_Now (df)
    st.plotly_chart(fig, use_container_width=True)