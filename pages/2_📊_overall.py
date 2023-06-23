# importando as bibliotecas
import pandas as pd
import inflection
import streamlit as st
import folium
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config( page_title="Overall", page_icon=":bar_chart:", layout ='wide' ) 

#===================================================#
#     Funções
#===================================================#

def country_map(df1):
    """ Esta função desenha um mapa com marcadores de restaurantes.
    
         O mapa exibe os restaurantes do dataframe com base em suas coordenadas de latitude e longitude.
         Cada marcador representa um restaurante e exibe informações como nome do restaurante, tipo de culinária,
         custo médio para duas pessoas, avaliação e cor da avaliação.
        
        Input: Dataframe
        Output: Exibição do mapa interativo com marcadores de restaurantes
    """
    # Desenhar o mapa
    df1mapa = df1[['restaurant_name', 'longitude', 'latitude', 'cuisines', 
                   'average_cost_for_two', 'currency', 'aggregate_rating', 'rating_color']].reset_index(drop = True)

    # Criando o mapa
    mapa = folium.Map(zoom_start = 15)

    #Criando os clusters
    mc = MarkerCluster().add_to(mapa)
    
    # Ícone para os marcadores
    icon = 'fa-cutlery'

    # Adicionar os marcadores ao mapa
    for index, location_info in df1mapa.iterrows():
        folium.Marker([location_info['latitude'],       
                       location_info['longitude']],
                       icon = folium.Icon(color=location_info['rating_color'], icon=icon, prefix='fa'),
                       popup = folium.Popup(f"""<h6> <b> {location_info['restaurant_name']} </b> </h6> <br>
                                            Cozinha: {location_info['cuisines']} <br>
                                            Preço médio para dois: {location_info['average_cost_for_two']}({location_info['currency']}) <br>
                                            Avaliação: {location_info['aggregate_rating']} / 5.0 <br> """,
                                            max_width= len(f"{location_info['restaurant_name']}")*20)).add_to(mc)
    folium_static(mapa, width = 1024, height = 600 )
    
def display_metrics(df1):
    """ Esta função exibe métricas de 5 colunas
    
         As métricas exibidas são:
         - Número de restaurantes cadastrados
         - Número de países cadastrados
         - Número de cidades cadastradas
         - Total de avaliações feitas na plataforma
         - Número de tipos de culinárias disponíveis
        
         Input: Dataframe
         Output: Exibição das métricas em 5 colunas
    """
    # Divisão do layout em colunas
    col1,col2,col3,col4,col5 = st.columns(5)
    
    # Métrica: Número de restaurantes cadastrados
    with col1:
        resisted_restaurant = df1.loc[:,'restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados ', resisted_restaurant)
    
    # Métrica: Número de países cadastrados
    with col2:
        resisted_country = df1.loc[:,'country'].nunique()
        col2.metric('Países Cadastrados ', resisted_country)
    
    # Métrica: Número de cidades cadastradas
    with col3:
        resisted_city = df1.loc[:,'city'].nunique()
        col3.metric('Cidade Cadastradas',resisted_city)

    # Métrica: Total de avaliações feitas na plataforma
    with col4:
        resisted_votes = df1.loc[:,'votes'].sum()
        col4.metric('Avaliações Feitas na Plataforma ', resisted_votes)

    # Métrica: Número de tipos de culinárias disponíveis
    with col5:
        cuisines_city = df1.loc[:,'cuisines'].nunique()
        col5.metric('Tipos de Culinárias', cuisines_city)

    
def rename_columns(df):
    """ Esta função realiza modificações nos nomes das colunas do dataframe sendo elas:
    
         Tipos de renomeação:
         
         1. Título: Converte a primeira letra de cada palavra em maiúscula
         2. Snakecase: Converte os espaços em ( _ ) e letras minúsculas
         3. Espaços: Remove os espaços em branco das colunas

         Input: Dataframe
         output: Dataframe com as colunas renomeadas
    """

    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def country_name(df):
    """ Esta função tem a responsabilidade de substituir os códigos pelos nomes dos países correspondentes
        
        Input: Dataframe
        Output: Dataframe com os nomes dos países substituindo os códigos de país
    """
    df['country_code'] = df['country_code'].replace({
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
    }) 
    return df



def color_name(df):
    """ Esta função tem a responsabilidade de substituir os códigos por nomes de cores 
            
        Input: Dataframe
        Output: Dataframe com os códigos de cores substituídos pelos nomes de cores 
    """
    df['rating_color'] = df['rating_color'].replace({
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }) 
    return df


def clean_dataframe(df):
    """ Esta função tem a responsabilidade de limpar o dataframe
    
         Limpezas realizadas:
         
         1. Retorno apenas do primeiro nome dos elementos da coluna 'cuisines'
         2. Remoção de dados nulos
         3. Remoção de dados duplicados
         4. Remoção de linhas com o valor 'Drinks Only' na coluna 'cuisines'
         5. Remoção de linhas com o valor 'Mineira' na coluna 'cuisines'
         6. Renomeação da coluna 'country_code' para 'country'
        
         Input: Dataframe
         Output: Dataframe limpo
    """
    
    # Retorno apenas do primeiro nome dos elementos da coluna 'cuisines'
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)
    
    # Remoção de dados nulo
    df_clean = df.dropna()

    # Remoção os dados duplicados
    df1 = df_clean.drop_duplicates()

    # Remoção de linhas
    linhas_removidas = df['cuisines'] != 'Drinks Only'
    df1 = df1.loc[linhas_removidas,:]

    # Remoção de linhas
    linhas_removidas = df['cuisines'] != 'Mineira'
    df1 = df1.loc[linhas_removidas,:]

    # Renomeação da coluna 'country_code' para 'country'
    df1 = df1.rename(columns={'country_code': 'country'})
    return df1
# -------------------------------- Inicio da Estrutura lógica do código-----------------------------------
# ------------------------
# Importando o  dataset
# ------------------------

df = pd.read_csv('zomato.csv')

# ------------------------
# Limpando dados
# ------------------------
rename_columns(df)
country_name(df)
color_name(df)
df1 = clean_dataframe(df)

#===================================================#
#     Barra lateral
#===================================================#

#Filtro de paises
st.sidebar.markdown('## Filtros')

# Criação do filtro de paises
country_options = st.sidebar.multiselect(
'Selecione os paises que deseja visualizar os Restaurantes:',
['Philippines', 'Brazil', 'Australia', 'United States of America',
   'Canada', 'Singapure', 'United Arab Emirates', 'India',
   'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
   'Sri Lanka', 'Turkey'],
default = ['Philippines', 'Brazil', 'Australia', 'United States of America',
   'Canada', 'Singapure', 'United Arab Emirates', 'India',
   'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
   'Sri Lanka', 'Turkey'])

st.sidebar.markdown('''---''') 

# Aplicação do filtro no dataset
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]


st.sidebar.markdown('##### Developed by:') 
st.sidebar.markdown('#### Joao Victor - Data Scientist')  

st.sidebar.markdown('''---''') 
#===================================================#
#     layout no streamlit
#===================================================#

st.title('Fome Zero')
st.markdown('## O lugar perfeito para encontrar seu restaurante favorito !')
st.markdown('''---''') 

with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
   
    # Chamando a função de exibição de métricas
    display_metrics(df1)
    
    st.markdown('''---''')         
   
    # Chamando a função que exibe o mapa
    country_map(df1)