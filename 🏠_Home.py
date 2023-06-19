import streamlit as st
import pandas as pd
from PIL import Image
import emoji

st.set_page_config(
    page_title="Home",
    page_icon="🏠"
)


# ==========================================================================================================
# Barra Lateral
# ==========================================================================================================

image = Image.open( "logo.png" )
st.sidebar.image( image, width=300 )

st.sidebar.markdown( '# Fome Zero Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( 'Dados Tratados' )
zomato_df = pd.read_csv("dataset/zomato.csv")

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(zomato_df) 

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='zomato.csv',
    mime='text/csv',
)





# ==========================================================================================================
# Página Home - Orientações
# ==========================================================================================================

st.header ("🏠" "Fome Zero Company Growth Dashboard")
st.markdown(
    '''
    Growth Dashboard foi construído para acompanhar as métricas de crescimento realcionadas aos restaurantes e culinárias oferecidas nos países em que a Fome Zero Company está atuando.
    ### Como utilizar esse Growth Dashboard?
    - Visão Cidades:
        - Visão gerencial: Métricas gerais de comportamento.
        - Visão tática: Indicadores relevantes por cidades.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Países:
        - Visão gerencial: Métricas gerais de comportamento.
    - Visão Culinária: 
        - Visão gerencial: Métricas gerais de comportamento.
    ### Ask for Help
    - Time de Data Science no Discord
        - @Wilmara Alves#8837
    ''')
