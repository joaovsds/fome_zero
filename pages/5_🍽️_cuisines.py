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

st.set_page_config( page_title='Cuisines', page_icon='🍽️', layout ='wide' )

#===================================================#
#     Funções
#===================================================#

def display_cuisine_metrics(cuisines):
    """ Esta função exibe as métricas culinárias
    
         A função calcula as médias de avaliação agregada e custo médio para dois
         para os restaurantes que oferecem uma determinada culinária. Os dados são filtrados com base
         na culinária especificada pelo parâmetro 'cuisines'.
        
        Input:
        - cuisines: Tipo de culinária a ser analisada
        
        Output:
        - Exibição das métricas da culinária
    """
    linhas = df1['cuisines'] == cuisines
    df_aux = (df1.loc[linhas,['aggregate_rating','average_cost_for_two','cuisines','country','currency','city',
                                        'restaurant_id','restaurant_name']]
                .groupby(['country','city','restaurant_id','restaurant_name','average_cost_for_two','currency','cuisines'])
                .mean()
                .sort_values(['aggregate_rating','restaurant_id'],ascending = [False,True])
                .reset_index())

    aux = st.metric(
            label=f'{cuisines}: {df_aux.iloc[0,3]}',
            value=f'{df_aux.iloc[0,7]}/5.0',
            help=f"""
            País: {df_aux.iloc[0,0]}\n
            Cidade: {df_aux.iloc[0,1]}\n
            Média Prato para dois: {df_aux.iloc[0,4]} ({df_aux.iloc[0,5]})
            """,
        )
    return aux

def display_top_restaurants(df1, date_slider):
    """ Esta função exibe uma tabela com os principais restaurantes
    
         A tabela exibe informações dos principais restaurantes com base na avaliação agregada.
         Os restaurantes são classificados em ordem  decrescente de avaliação agregada (selecionado os mesmos com a maiores avaliações)
         e, em caso de empate, são ordenados pelo ID do restaurante em ordem crescente (priorisando os restaurantes mais antigos.
         O número de restaurantes a serem exibidos é determinado pelo parâmetro date_slider.
        
        Input:
        - df1: DataFrame contendo os dados  
        - date_slider: Número de restaurantes a serem exibidos (podendo ser alterado através do filtro da barra lateral)
        
        Output:
        - Exibição da tabela com as informações dos principais restaurantes
    """
    df_aux = (df1.loc[:,['votes','cuisines','country','city','restaurant_id','restaurant_name','average_cost_for_two','aggregate_rating']]
            .groupby(['restaurant_id','restaurant_name','country','city','cuisines','average_cost_for_two','aggregate_rating'])
            .sum()
            .reset_index()
            .sort_values(['aggregate_rating','restaurant_id'],ascending = [False, True])
            .reset_index(drop = True))

    table = st.dataframe(df_aux.head(date_slider))
    return table

def display_top_cuisines(df1,date_slider,title,ascending):
    """ Esta função exibe um gráfico de barras mostrando as principais culinárias com base na média de avaliação
    
         A função calcula a média de avaliação para cada tipo de culinária e exibe as principais culinárias
         em um gráfico de barras. O número de culinárias exibidas é determinado pelo parâmetro date_slider.
         O gráfico de barras mostra a média de avaliação, onde cada barra epresenta uma culinária e a altura
         da barra representa a média de avaliação.
    
    Args:
        df1: O dataframe com os dados.
        date_slider: O número de culinárias a serem exibidas (podendo ser alterado através do filtro da barra lateral).
        title: O título do gráfico.
        ascending: Define a ordem de classificação das culinárias. Se True, as culinárias serão
                          classificadas em ordem crescente de média de avaliação. Se False, as culinárias
                          serão classificadas em ordem decrescente de média de avaliação.
    
    Returns:
        fig: O gráfico de barras.
    """
    df_aux = (df1.loc[:, ['aggregate_rating', 'cuisines']]
              .groupby('cuisines')
              .mean()
              .reset_index()
              .sort_values('aggregate_rating', ascending=ascending)
              .round(2)
              .reset_index(drop=True)
              .head(date_slider))

    fig = go.Figure(data=[go.Bar(
            x=df_aux['cuisines'], y=df_aux['aggregate_rating'],
            width=0.75,
            text=df_aux['aggregate_rating'],
            textposition='auto',
            marker=dict(color='royalblue')
        )])

    fig.update_xaxes(title_text="Tipo de Culinária")
    fig.update_yaxes(title_text="Média de Avalição")
    fig.update_layout(title=dict(text=title,x = 0.5,font=dict(size=18)))   
    fig.update_layout( xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
    fig = st.plotly_chart(fig, use_container_width=True)
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

# criação de filtro de números de restaurantes
date_slider = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    value = 10 ,
    min_value = 0, # inicio do filtro
    max_value = 20, # final do filtro
     )

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
st.title('🍽️ Visão Culinária')
st.markdown('''---''')

st.markdown('### Melhores Restaurantes dos Principais tipos Culinários')

with st.container():
    
    italian, american, arabian, japanese, brazilian = st.columns(5)
    
    with italian:
        display_cuisine_metrics('Italian')
    with american:
        display_cuisine_metrics('American')
    with arabian:
        display_cuisine_metrics('Arabian')
    with japanese:
        display_cuisine_metrics('Japanese')
    with brazilian:
        display_cuisine_metrics('Brazilian')

    st.markdown('''---''')     

    st.markdown(f'## Top {date_slider} Restaurantes')
    
    display_top_restaurants(df1, date_slider)
    
    st.markdown('''---''') 
    
with st.container():
    col1,col2 = st.columns(2)
        
    with col1:
        display_top_cuisines(df1,date_slider,f'Top {date_slider} Melhores Tipos de Culinária',ascending = False)
        
    with col2:
        display_top_cuisines(df1,date_slider,f'Top {date_slider} Piores Tipos de Culinária',ascending = True)
       
