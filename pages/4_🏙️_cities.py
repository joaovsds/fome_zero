# importando as bibliotecas
import pandas as pd
import inflection
import streamlit as st
import folium
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config( page_title='Cities', page_icon='🏙️', layout ='wide' )

#===================================================#
#     Funções
#===================================================#

def top_city_resisted_restaurant(df1):
    """ Esta função gera um gráfico de barras mostrando as principais cidades com base na quantidade de restaurantes 
    
         O gráfico mostra as 10 principais cidades com base na quantidade de restaurantes registrados na base de dados.
         Cada barra representa uma cidade e mostra o número de restaurantes registrados.
         A cor das barras representa o país ao qual a cidade pertence.
        
        Input: Dataframe
        Output: Exibição do gráfico de barras interativo com as principais cidades
    """
        
    df_aux = (df1.loc[:,['country','restaurant_id','city']]
      .groupby(['country','city'])
      .count()
      .sort_values(["restaurant_id", "city"], ascending=[False, True])
      .reset_index() )

    fig = (px.bar(df_aux.head(10), x = 'city', y = 'restaurant_id', text = 'restaurant_id', 
                             color = 'country', 
                             labels = { 'restaurant_id' : 'Restaurante',
                                         'city' : 'Cidade' ,
                                          'country' : 'País'} ) )
    fig.update_layout(title=dict(text='Top 10 Cidades com mais Restaurantes na Base de Dados', x=0.30, font=dict(size=20)))
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width = True)
    return fig
def plot_top_cities(condition,title):
    """ Esta função gera um gráfico de barras mostrando as principais cidades com base em uma condição de avaliação
    
         A condição  'acima' (para cidades com avaliação acima de 4) ou 'abaixo' (para cidades com avaliação abaixo de 2.5).
         O gráfico mostra as 7 principais cidades com base na contagem de restaurantes que atendem à condição de avaliação.
         Cada barra representa uma cidade e mostra o número de restaurantes que atendem à condição.
         A cor das barras representa o país ao qual a cidade pertence.
        
        Input: condition (str) - Condição de avaliação ('acima' ou 'abaixo')
               title (str) - Título do gráfico
        Output: Exibição do gráfico de barras com as principais cidades
    """
    
    if condition == 'acima':
        linhas = df1['aggregate_rating'] > 4
    elif condition == 'abaixo':
        linhas = df1['aggregate_rating'] < 2.5
    df_aux = (df1.loc[linhas, ['country', 'city', 'restaurant_id']]
              .groupby(['country', 'city'])
              .count()
              .sort_values('restaurant_id', ascending=False)
              .reset_index())

    fig = (px.bar(df_aux.head(7), x='city', y='restaurant_id', text='restaurant_id',
                  color='country',
                  labels={'restaurant_id': 'Restaurantes',
                          'city': 'Cidade',
                          'country': 'País'}))
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    fig.update_layout(title=dict(text=title, font=dict(size=17)))
    st.plotly_chart(fig, use_container_width=True)
    
def plot_top_cities_cuisines(df1):
    """ Esta função exibe um gráfico de barras mostrando as principais cidades com maior diversidade gastronômica
    
         O gráfico de barras exibe as 10 principais cidades com base na quantidade de tipos culinários únicos encontrados em cada uma.
         Cada barra representa uma cidade e mostra o número de tipos culinários presentes nessa cidade.
         A cor das barras representa o país ao qual a cidade pertence.
        
        Input: Dataframe 
        Output: Exibição do gráfico de barras com as principais cidades e diversidades gastronômicas
    """
    
    df_aux = (df1.loc[:,['cuisines','country','city']]
             .groupby(['country','city'])
             .nunique()
             .sort_values('cuisines',ascending = False)
             .reset_index() )

    fig = (px.bar(df_aux.head(10), x = 'city', y = 'cuisines', text = 'cuisines', 
                             color = 'country', 
                             labels = { 'cuisines' : 'Tipos Culinários',
                                         'city' : 'Cidade' ,
                                          'country' : 'País'} ) )
    fig.update_layout(title=dict(text='Top 10 cidades com maiores diversidades gastronômicas', x=0.30,font=dict(size=20)))
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width = True)
    return fig
    
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
        Output: Dataframe com os nomes dos países 
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
        Output: Dataframe com os nomes das cores 
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
# Import dataset
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
default = ['Brazil', 'Australia', 'Canada',
           'England', 'Qatar', 'South Africa'])

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
st.title('🏙️ Visão Cidades')
st.markdown('''---''')

with st.container():    
    top_city_resisted_restaurant(df1)
    
st.markdown('''---''') 
           
with st.container():    
    col1,col2 = st.columns(2)
    
    with col1:
        plot_top_cities('acima','Top 7 cidades com restaurantes de média avaliativa acima de 4')
    
    with col2:
        plot_top_cities('abaixo','Top 7 cidades com restaurantes de média avaliativa abaixo de 2.5')
       
    st.markdown('''---''')
        
with st.container():
    plot_top_cities_cuisines(df1)


