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

st.set_page_config( page_title='Countries', page_icon='🌍', layout ='wide' )

#===================================================#
#     Funções
#===================================================#

def plot_restaurant_count_by_country(df1):
    """ Esta função gera um gráfico de barras mostrando a quantidade de restaurantes registrados por país

         Cada barra representa um país e mostra o número de restaurantes registrados.
        
        Input: Dataframe
        Output: Exibição do gráfico de barras interativo com a quantidade de restaurantes registrados por país
    """
    df_aux = (df1.loc[:,['restaurant_id','country']]
    .groupby('country')
    .nunique()
    .sort_values('restaurant_id',ascending = False)
    .reset_index())

    fig = go.Figure(data=[go.Bar(
                x=df_aux['country'], y=df_aux['restaurant_id'],
                width=0.75,
                text=df_aux['restaurant_id'],
                textposition='auto',
                marker=dict(color='royalblue')
            )])
    fig.update_layout(title=dict(text="Quantidade de Restaurantes Registrados por País", x=0.25,font=dict(size=20)))  
    fig.update_xaxes(title_text="Países")
    fig.update_yaxes(title_text="Restaurantes")
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width = True)
    return fig

def plot_city_count_by_country(df1):
    """ Esta função gera um gráfico de barras mostrando a quantidade de cidades registradas por país
    
         Cada barra representa um país e mostra o número de cidades registradas.
        
        Input: Dataframe
        Output: Exibição do gráfico de barras com a quantidade de cidades registradas por país
    """
    df_aux = (df1.loc[:,['city','country']]
            .groupby('country')
            .nunique()
            .sort_values('city',ascending = False)
            .reset_index() )

    fig = go.Figure(data=[go.Bar(
                x=df_aux['country'], y=df_aux['city'],width=0.75,
                text=df_aux['city'],
                textposition='auto',
                marker=dict(color='royalblue')
            )])
    fig.update_layout(title=dict(text="Quantidade de Cidades Registrados por País", x=0.25,font=dict(size=20))) 
    fig.update_xaxes(title_text="Países")
    fig.update_yaxes(title_text="Cidades")
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width = True)
    return fig

      
def plot_average_rating_by_country(df1):
    """ Esta função gera um gráfico de barras mostrando a avaliação média por país
    
         Cada barra representa um país e mostra o valor médio da avaliação.
        
        Input: Dataframe
        Output: Exibição do gráfico de barras com a avaliação média por país
    """
    df_aux = (df1.loc[:,['country','aggregate_rating']]
         .groupby('country')
         .mean()
         .sort_values('aggregate_rating',ascending = False)
         .reset_index().round(2) )

    fig = go.Figure(data=[go.Bar(
                x=df_aux['country'], y=df_aux['aggregate_rating'],width=0.75,
                text=df_aux['aggregate_rating'],
                textposition='auto',
                marker=dict(color='royalblue')
            )])
    fig.update_layout(title=dict(text="Avaliação Média por País", x=0.50,font=dict(size=20))) 
    fig.update_xaxes(title_text="Países")
    fig.update_yaxes(title_text="Avaliações")
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width = True)
    return fig


def plot_average_cost_for_two_by_country(df1):
    """ Esta função gera um gráfico de barras mostrando a média de preço de um prato para duas pessoas por país
    
         Cada barra representa um país e mostra o valor médio do preço.
        
        Input: Datafrane
        Output: Exibição do gráfico de barras com a média de preço por país
    """
        
    df_aux = (df1.loc[:,['country','average_cost_for_two']]
       .groupby('country')
       .mean()
       .sort_values('average_cost_for_two',ascending = False)
       .reset_index().round(2) )

    fig = go.Figure(data=[go.Bar(
                x=df_aux['country'], y=df_aux['average_cost_for_two'],width=0.75,
                text=df_aux['average_cost_for_two'],
                textposition='auto',
                marker=dict(color='royalblue')
            )])
    fig.update_layout(title=dict(text="Preço Médio de um Prato para Duas Pessoas por País",  x=0.5,font=dict(size=17))) 
    fig.update_xaxes(title_text="Países")
    fig.update_yaxes(title_text="preço de Prato para Duas Pessoas")
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width = True, width=700, height=300)
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
st.title('🌍 Visão Países')
st.markdown('''---''') 

with st.container():
    plot_restaurant_count_by_country(df1)
    
    st.markdown('''---''') 
    
    plot_city_count_by_country(df1)

st.markdown('''---''')   
    
with st.container():
    col1,col2 = st.columns(2)
    
    with col1:
        plot_average_rating_by_country(df1)
        
    with col2:
        plot_average_cost_for_two_by_country(df1)
