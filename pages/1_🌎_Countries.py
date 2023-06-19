#-----------Bibliotecas------------------------------------------------------------#
from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title="Países", page_icon="🌎", layout="wide")

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

#4. Para exibição de gráfico com a quantidade restaurantes registrados por país
def country_Restaurant(df):
    ''' Esta função realiza a seleção dos países com maior número de restaurande registrados:
        1. Seleciona as colunas de páis e restaurante e os agrupa;        
        2. Ordena a contagem única por restaurantes;
        3. Cria gráfico com o número de restaurantes por país.

        Input: DataFrame 
        Output: Gráfico'''
    df_country_Restaurant = df.loc[:, ["restaurant_id", "country_code"]].groupby(["country_code"]).nunique().sort_values("restaurant_id", ascending=False).reset_index()
    df_country_Restaurant.columns = ["Países", "Quantidade de restaurantes"]
    fig = px.bar( df_country_Restaurant, x="Países", y="Quantidade de restaurantes", title="Restaurantes registrados")
    fig = fig.update_traces(textposition="inside", text=df_country_Restaurant["Quantidade de restaurantes"])
    fig = fig.update_layout(title_x=0.25)
    return fig

#5. Para exibição de gráfico contendo cidades registradas por país
def City_Restaurant(df):
    ''' Esta função realiza a seleção e contagem de cidades por país:
        1. Seleciona as colunas de cidade e país e os agrupa;        
        2. Ordena a contagem única de cidades;
        3. Cria gráfico com o número de cidades por país.

        Input: DataFrame 
        Output: Gráfico'''
    df_City_Restaurant = df.loc[:, ["city", "country_code"]].groupby(["country_code"]).nunique().sort_values("city", ascending=False).reset_index()
    df_City_Restaurant.columns = ["Países", "Cidades registradas"]
    fig = px.bar(df_City_Restaurant, x="Países", y="Cidades registradas", title="Cidades resgistradas")
    fig = fig.update_traces(textposition="inside", text=df_City_Restaurant["Cidades registradas"])
    fig = fig.update_layout(title_x=0.25)
    return fig

#6. Para exibição de gráfico de média de avaliações por país
def country_votes(df):
    ''' Esta função realiza a seleção e contagem de votos por país:
        1. Seleciona as colunas de votos e país e os agrupa;        
        2. Ordena a contagem única por páis;
        3. Cria gráfico com o número médio de votos por país.

        Input: DataFrame 
        Output: Gráfico'''
    df_country_votes = df.loc[:, ["votes", "country_code" ] ].groupby(["country_code"]).mean().sort_values("votes", ascending=False).reset_index()
    df_country_votes = df_country_votes.round({"votes":2})
    df_country_votes.columns = ["Países", "Média de avaliações"]
    fig = px.bar(df_country_votes, x="Países", y="Média de avaliações", title="Média de avaliações" )
    fig = fig.update_traces(textposition="inside", text=df_country_votes["Média de avaliações"])
    fig = fig.update_layout(title_x=0.25)
    return fig

#7. Para exibição de gráfico contendi preço médio para 2 pessoas por país
def Restaurant_Avg_Cost_for_two(df):
    ''' Esta função realiza a seleção e calcula a média de preço para 2 pessoas por país:
        1. Seleciona as colunas de preço para 2 e país e os agrupa;        
        2. Ordena amédia por média de preço para dois;
        3. Cria gráfico com a média de preço pra 2 por país.

        Input: DataFrame 
        Output: Gráfico'''
    df_Restaurant_Avg_Cost_for_two = df.loc[:, ["average_cost_for_two", "country_code"]].groupby(["country_code"]).mean().sort_values("average_cost_for_two", ascending=False).reset_index()
    df_Restaurant_Avg_Cost_for_two.columns = ["País", "Preço médio pra 2 pessoas"]
    df_Restaurant_Avg_Cost_for_two = df_Restaurant_Avg_Cost_for_two.round({"Preço médio pra 2 pessoas":2})
    fig = px.bar(df_Restaurant_Avg_Cost_for_two, x="País", y="Preço médio pra 2 pessoas", title="Preço médio para 2 por país")
    fig = fig.update_traces(textposition="inside", text=df_Restaurant_Avg_Cost_for_two["Preço médio pra 2 pessoas"])
    fig = fig.update_layout(title_x=0.25)
    return fig

#8. Definir o dicionário de cores baseado na avaliação média
def get_color(avg_rating):
    ''' Esta função cria condição para definição de cores do popup:
        1. Determina quais valores serão adotados para categorizar;        
        2. Cria as condições de maior ou igual para cada valor adotado e suas respectivas cores;
        3. Função permite utilização para colorir mapas ou demais gráficos em que sejam adotadas as avaliações médias.

        Input: Código phyton 
        Output: Função'''
    if avg_rating >= 4.5:
        return "green"
    elif avg_rating >= 4.0:
        return "lightgreen"
    else:
        return "red"
    
#9. Para criação de mapa com a localização dos restaurantes registrados  
def Country_Aggregate_costfor2_mean(df):
    ''' Esta função deseha mapa a partir da concatenção de df's preço médio para 2 e avaliação média:
        1. Cria os dataframes de preço médio pra 2 e avaliaçõe média;        
        2. Cada dataframe criado foi agrupado por país, restaurante e culinária;
        3. Foram calculadas as médias do agrupamento e ordenados, respectivamente por preço médio pra 2 e avaliaçõe média;
        4. Os dataframes foram concatenados e tiveram suas colunas renomeadas;
        5. Foi criado um dicionário de moedas por país e exibidas as moedas correspondentes em uma nova coluna criada em dataframe auxiliar;
        6. Criação do mapa contendo na página inicial a quantidade de restaurantes por área;
        7. No popup dos restaurantes é apresentada a coloração de acrodo com a função baseada na sua avaliação média e demais informações.

        Input: DataFrame 
        Output: Gráfico'''
    df_Country_Aggregate_costfor2_mean = df.loc[:, ["average_cost_for_two", "country_code", "restaurant_name", "cuisines", "latitude", "longitude"]].groupby(["country_code", "restaurant_name", "cuisines"]).mean().sort_values("average_cost_for_two", ascending=False).reset_index()
    df_Country_Aggregate_costfor2_mean = df_Country_Aggregate_costfor2_mean.round({"average_cost_for_two":1})
    df_Country_Aggregate_rating_mean = df.loc[:, ["aggregate_rating", "country_code", "restaurant_name", "cuisines", "latitude", "longitude"]].groupby(["country_code", "restaurant_name", "cuisines"]).mean().sort_values("aggregate_rating", ascending=False).reset_index()
    df_Country_Aggregate_rating_mean = df_Country_Aggregate_rating_mean.round({"aggregate_rating":1})
    # Concatenar os dataframes e manter latitude e longitude na mesma linha para o mesmo restaurante
    df_concatenado = pd.merge(df_Country_Aggregate_rating_mean, df_Country_Aggregate_costfor2_mean, on=["country_code", "restaurant_name", "cuisines", "latitude", "longitude"], suffixes=("_rating_mean", "_costfor2_mean"), how="outer")
    df_concatenado.columns = ["Pais", "Restaurante", "Culinária", "Avaliação Média", "Latitude", "Longitude",  "Preço"]
    # Mapear código do país para moeda correspondente
    paises = df_concatenado["Pais"].unique()
    codigo_moeda = {
        "India": "INR",
        "Australia": "AUD",
        "Brazil": "BRL",
        "Canada": "CAD",
        "Indonesia": "IDR",
        "New Zeland": "NZD",
        "Philippines": "PHP",
        "Qatar": "QAR",
        "Singapure": "SGD",
        "South Africa": "ZAR",
        "Sri Lanka": "LKR",
        "Turkey": "TRY",
        "United Arab Emirates": "AED",
        "England": "GBP",
        "United States of America": "USD"
    }

    # Verificar se o país tem um código de moeda mapeado, caso contrário, utilizar um código de moeda padrão (por exemplo, "XXX")
    for pais in paises:
        if pais not in codigo_moeda:
            codigo_moeda[pais] = "XXX"  # Código de moeda padrão
    df_aux = df_concatenado.loc[:, ["Pais", "Restaurante", "Culinária", "Latitude", "Longitude", "Avaliação Média", "Preço"]].groupby(["Pais", "Restaurante", "Culinária"]).first().reset_index()
    df_aux["Moeda"] = df_aux["Pais"].map(codigo_moeda)
    # Criação do mapa com agrupamento de marcadores
    map = folium.Map(zoom_start=11)
    marker_cluster = MarkerCluster().add_to(map)

    for index, location_info in df_aux.iterrows():
        color = get_color(location_info["Avaliação Média"])
        folium.Marker(
            [location_info["Latitude"], location_info["Longitude"]],
            popup=f"<b>{location_info['Restaurante']}</b><br><br><br>Culinária: {location_info['Culinária']}<br><br>Preço: {location_info['Preço']} Médio para dois {location_info['Moeda']}<br><br>Avaliação Média: {location_info['Avaliação Média']}/5.0",
            icon=folium.Icon(color=color, icon="home"),
            tooltip=location_info['Restaurante'],
            max_width=1200  # Definir a largura máxima do popup em pixels
        ).add_to(marker_cluster)

    fig = folium_static(map, width=1024, height=600)
    return fig

#-------------Importando arquivo---------------------------------------------------#
df_raw = pd.read_csv("dataset/zomato.csv")

df = df_raw.copy()

#------------Limpeza---------------------------------------------------------------#

df = clean_code(df)
  

# ==========================================================================================================
# Barra Lateral
# ==========================================================================================================

st.title('🌎 Visão Países')

image = Image.open( "logo.png" )
st.sidebar.image( image, width=300 )

st.sidebar.markdown( '# Fome Zero Company' )

st.sidebar.markdown( """---""" )

st.sidebar.markdown( '# Filtros' )

country_options = st.sidebar.multiselect( 
    'Selecione o país que deseja visualizar o restaurante',
    ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'], 
    default=['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'])



st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Eat wherever you are!' )

# Filtro de país
linhas_selecionadas = df['country_code'].isin( country_options )
df = df.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================# 

with st.container():
    st.title( 'Métricas gerais' )
    col1, col2, col3, col4, col5 = st.columns( 5, gap='large')

    with col1:
        restaurants_register = df.loc[:, 'restaurant_id'].nunique()
        col1.metric( 'Restaurantes Registrados', restaurants_register )

    with col2:
        country_register = df.loc[:, 'country_code'].nunique()
        col2.metric( 'Países Registrados', country_register )

    with col3:
        city_register = df.loc[:, 'city'].nunique()
        col3.metric( 'Cidades Registradas', city_register )

    with col4:
        aggregate_register = df.loc[:, 'votes'].sum()
        col4.metric( 'Avaliações Reistradas', aggregate_register )

    with col5:
        cuisines_register = df.loc[:, 'cuisines'].nunique()
        col5.metric( 'Culinária Resgistradas', cuisines_register )

with st.container():
    st.title( 'País campeão em...' )

    col1, col2, col3, col4, col5 = st.columns( 5, gap='large')

    with col1:
        df_country_city = df.loc[:,["country_code", "city"]].groupby(["country_code"]).nunique().sort_values("city", ascending=False).reset_index()
        col1.metric( 'Cidades registradas',  df_country_city.iloc[0,0] )

    with col2:
        df_country_Restaurant = df.loc[:,["restaurant_id", "country_code"]].groupby(["country_code"]).nunique().sort_values("restaurant_id", ascending=False).reset_index()
        col2.metric( 'Restaurantes registrados', df_country_Restaurant.iloc[0,0] )

    with col3:
        df_country_Restaurant_price = df.loc[:, ["average_cost_for_two","restaurant_id","country_code"]].groupby(["restaurant_id","country_code"]).mean().sort_values("average_cost_for_two", ascending=False).reset_index()
        col3.metric( 'Média de de Preço pra 2', df_country_Restaurant_price.iloc[0,1] )

    with col4:
        df_country_Restaurant_Type_distant = df.loc[:,["country_code", "cuisines" ]].groupby(["country_code"]).nunique().sort_values(["cuisines",], ascending=False).reset_index().head(10)
        df_country_Restaurant_Type_distant.columns = ["Country", "Cuisines"]
        col4.metric( 'Culinára distinta registrada', df_country_Restaurant_Type_distant.iloc[0,0] )

    with col5:
        df_country_votes = df.loc[:, ["votes", "country_code" ] ].groupby(["country_code"]).sum().sort_values("votes", ascending=False).reset_index()
        col5.metric( 'Avaliações resgistradas', df_country_votes.iloc[0,0] ) 

with st.container():
    col1, col2 = st.columns( 2, gap='large')
    
    with col1:
        fig = country_Restaurant(df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = City_Restaurant(df)       
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns( 2, gap='large')

    with col1:
        fig = country_votes(df)
        st.plotly_chart( fig, use_container_width=True )

    with col2:
        fig = Restaurant_Avg_Cost_for_two(df)
        st.plotly_chart( fig, use_container_width=True )

with st.container():
    st.title( 'Localização dos restaurantes' )
    fig = Country_Aggregate_costfor2_mean(df)
   
    




