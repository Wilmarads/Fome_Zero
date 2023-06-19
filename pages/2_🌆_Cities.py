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


st.set_page_config(page_title="Cidades", page_icon="🌆", layout="wide")

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
#4. Para seleção de restaurantes que aceitam reservas

def df_Restaurant_City_Table(df):
    ''' Esta função realiza a seleção de restaurantes com reservas online.
        Tipos de função:
        1. Seleciona as linhas que estão com indicação de aceitação de reservar;
        2. Agrupa as linhas selcionadas por cidade;
        3. Ordena as mesmas linhas pot restaurante e cidade;
        4. Retorna  um df com a quantidade de restaurantes que aceitam reservas;
        5. Aciona o index 0 do df.
        
                
        Input: DataFrame 
        Output: DataFrame'''
    df_Restaurant_City_Table = df.loc[df["has_table_booking"] == 1, ["restaurant_id","city"]].groupby(["city"])                                                .nunique().sort_values(["restaurant_id", "city"], ascending=[False,True]).reset_index()
    df_Restaurant_City_Table = df_Restaurant_City_Table.iloc[0,0]
    return df_Restaurant_City_Table

#5. Para seleção de restaurantes que estão realizando entrega no momento

def df_Restaurant_City_Delivery_now(df):
    ''' Esta função realiza a seleção de restauranes que estão realizando entregas no momento.
        Tipos de função:
        1. Seleciona as linhas que estão com indicação de realização de entrega no momento;
        2. Agrupa as linhas selcionadas por cidade;
        3. Ordena as mesmas linhas pot restaurante e cidade;
        4. Retorna  um df com a quantidade de restaurantes que realiza enregas no momento;
        5. Aciona o index 0 do df.
        
                
        Input: DataFrame 
        Output: DataFrame'''
    df_Restaurant_City_Delivery_now = df.loc[df["is_delivering_now"] == 1, ["restaurant_id","city"]].groupby(["city"]).nunique().sort_values(["restaurant_id", "city"], ascending=[False,True]).reset_index()
    df_Restaurant_City_Delivery_now = df_Restaurant_City_Delivery_now.iloc[0,0]
    return df_Restaurant_City_Delivery_now
        
#6. Para seleção de restaurantes com pedidos online

def df_Restaurant_City_Delivery_online(df):
    ''' Esta função realiza a seleção de restauranes que aceitam pedidos online.
        Tipos de função:
        1. Seleciona as linhas que estão com indicação de realização de pedidos online;
        2. Agrupa as linhas selcionadas por cidade;
        3. Ordena as mesmas linhas pot restaurante e cidade;
        4. Retorna  um df com a quantidade de restaurantes que realiza pedidos online;
        5. Aciona o index 0 do df.
        
                
        Input: DataFrame 
        Output: DataFrame'''
    df_Restaurant_City_Delivery_online = df.loc[df["has_online_delivery"] == 1, ["restaurant_id","city"]].groupby(["city"]).nunique().sort_values(["restaurant_id", "city"], ascending=[False,True]).reset_index()
    df_Restaurant_City_Delivery_online = df_Restaurant_City_Delivery_online.iloc[0,0]
    return df_Restaurant_City_Delivery_online

#7. Cria gráfico de top 10 de cidades com maior quantidade de restaurantes registrados
def df_City_Restaurant(df):
    ''' Esta função realiza a seleção das cidades com maior quantidade de restaurantes registrados em sua base.
    Tipos de função:
    1. Seleciona as colunas de restaurante, país e cidade;
    2. Agrupa as colunas selecionadas e realiza contagem por restaurante;
    3. Ordena as linhas  do agrupamento por restaurante e cidade;
    4. Retorna  uma figura com o top 10 de cidades com mais restaurantes na base.   

    Input: DataFrame 
    Output: Gráfico'''
    df_City_Restaurant = df.loc[:, ["restaurant_id", "country_code","city"]].groupby(["country_code", "city"]).nunique().sort_values(["restaurant_id", "city"], ascending=[False,True]).reset_index()
    df_City_Restaurant.columns=["País", "Cidade", "Qtd de restaurantes"]
    df_City_Restaurant["Pais"] = df_City_Restaurant["País"].apply(unidecode.unidecode)
    df_City_Restaurant = df_City_Restaurant.sort_values(["Qtd de restaurantes", "País"], ascending=[False, True])
    fig = px.bar(
    df_City_Restaurant[:10],
    x="Cidade",
    y="Qtd de restaurantes",
    color="Pais",
    title="Cidades com maior quantidade de restaurantes registrados",
    )
    fig = fig.update_traces(textposition="inside", text=df_City_Restaurant["Qtd de restaurantes"])
    fig = fig.update_layout(title_x=0.25)
    return fig

#8. Cria gráfico top 10 dos restaurantes melhores avaliados e piores avaliados
def plot_city_restaurant_aggregate(df, rating_threshold):
    ''' Esta função realiza a seleção dos restaurantes melhor e pior valiados com base no critério da avaliação média agregada:
        1. Cria filtro condicional para high, os restaurantes com avalição maior ou igual a 4;        
        2. O mesmo filtro e criado para o low, os restaurantes com avaliação igual ou inferior a 2,5;
        3. Com base no filtro define agrupamento  por país e cidade
        4. Ordena o resultado do agrupamento por reaturante e cidade;
        5. Agrupa as colunas selecionadas e realiza contagem por restaurante;
        6. Cria gráfico que será exibido conforme acionamento para high ou low, respectivamente com os 10 melhores ou os 10 piores.
                      
        Input: DataFrame 
        Output: Gráfico'''
    if rating_threshold == "high":
        filtered_df = df.loc[df["aggregate_rating"] >= 4, ["restaurant_id", "country_code", "city"]]
        title = "Cidades com avaliações maior ou igual a 4"
    elif rating_threshold == "low":
        filtered_df = df.loc[df["aggregate_rating"] <= 2.5, ["restaurant_id", "country_code", "city"]]
        title = "Cidades com avaliações abaixo de 2.5"
    else:
        raise ValueError("Valor inválido para rating_threshold. Deve ser 'high' ou 'low'.")

    aggregated_df = filtered_df.groupby(["country_code", "city"]).nunique().sort_values(["restaurant_id", "city"], ascending=[False, True]).reset_index()
    aggregated_df.columns = ["País", "Cidade", "Qtd de restaurantes"]
    aggregated_df = aggregated_df.sort_values(["Qtd de restaurantes", "País"], ascending=[False, True])

    fig = px.bar(
        aggregated_df[:10],
        x="Cidade",
        y="Qtd de restaurantes",
        color="País",
        title=title,
    )
    fig = fig.update_traces(textposition="inside", text=aggregated_df["Qtd de restaurantes"])
    fig = fig.update_layout(title_x=0.1)

    return fig


#9. Cria gráfico com o top 10 de restaurantes com maior número de culinária distinta 
def df_City_Restaurant_Type_distant(df):
    ''' Esta função realiza a seleção dos restaurantes com maior número de culinárias distintas:
        1. Seleciona as colunas de páis, cidade e culinára  os agrupa;        
        2. Ordena a contagem unica por culinária;
        3. Cria gráfico com top 10.

        Input: DataFrame 
        Output: Gráfico'''
    df_City_Restaurant_Type_distant = df.loc[:,["country_code","city", "cuisines" ]].groupby(["country_code", "city"]).nunique().sort_values(["cuisines"], ascending=False).reset_index()
    df_City_Restaurant_Type_distant.columns = ["País", "Cidade", "Rest. Culinária distintas"]
    fig = px.bar(df_City_Restaurant_Type_distant.head(10), x="Cidade", y="Rest. Culinária distintas", color="País", title="Restaurantes com maior número de culinária distinta")
    fig = fig.update_traces(textposition="inside", text=df_City_Restaurant_Type_distant["Rest. Culinária distintas"])
    fig = fig.update_layout(title_x=0.1)
    return fig


#-------------Importando arquivo---------------------------------------------------#
df_raw = pd.read_csv("dataset/zomato.csv")

df = df_raw.copy()

#------------Limpeza---------------------------------------------------------------#

df = clean_code(df)
  

# ==========================================================================================================
# Barra Lateral
# ==========================================================================================================

st.title('🌆 Visão Cidades')

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
    col1, col2, col3 = st.columns( 3, gap='large')
    
    with col1:
         
        col1.metric( 'Possui mais restaurantes com reservas', df_Restaurant_City_Table(df) )
        
    with col2:
        
        col2.metric("Possui mais restaurantes que fazem entregas", df_Restaurant_City_Delivery_now(df))
        
    with col3:
        
        col3.metric("Possui mais restaurantes com pedidos online", df_Restaurant_City_Delivery_online(df))
        
with st.container():
    st.title( 'Top 10' )
    fig = df_City_Restaurant(df)
    st.plotly_chart(fig, use_container_width=True)

    
with st.container():
    col1, col2, = st.columns( 2, gap='large')
    
    with col1: 
        fig = plot_city_restaurant_aggregate(df, rating_threshold="high")
        st.plotly_chart(fig, use_container_width=True)


    with col2: 
        fig = plot_city_restaurant_aggregate(df, rating_threshold="low")
        st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.subheader( 'Top 10 por culinária' )  
    fig = df_City_Restaurant_Type_distant(df)
    st.plotly_chart( fig, use_container_width=True )


