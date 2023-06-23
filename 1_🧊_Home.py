import streamlit as st
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(
    page_title="Home",
    page_icon=":bar_chart:"
)

#===================================================#
#     Funções
#===================================================#

def image_to_base64(image):
    """ Esta função recebe uma imagem como entrada e retorna uma representação base64 da imagem.
         Converte uma imagem para uma string base64. 
         
         Input:
         - image: A imagem a ser convertida.
    
         Output:
         - encoded_image: A imagem convertida em uma string base64.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_image

#===================================================#
#     Barra lateral
#===================================================#

image = Image.open('Logo.png')
image_resized = image.resize((150, 150))  

st.sidebar.markdown(
    f'<p align="center"><img src="data:image/png;base64,{image_to_base64(image_resized)}" alt="Logo" width="150" style="vertical-align: middle"></p>',
    unsafe_allow_html=True
)

st.sidebar.markdown('''---''') 

st.sidebar.markdown('##### Developed by:') 
st.sidebar.markdown('#### Joao Victor - Data Scientist') 

st.sidebar.markdown('''---''') 
#===================================================#
#     layout no streamlit
#===================================================#

st.write("# Fome Zero Growth Dashboard")

st.markdown(
    """
    O Growth Dashboard foi desenvolvido com o propósito de monitorar as métricas dos estabelecimentos gastronômicos em diferentes países e segmentos culinários.
    ### Como utilizar esse Growth Dashboard?
    - Overall:
        - Restaurantes Cadastrados
        - Países Cadastrados
        - Cidade Cadastradas
        - Avaliações Feitas na Plataforma
        - Tipos de Culinárias
        - Mapa da localização dos Restaurantes
        
    - Countries:
        - Restaurantes Registrados por País
        - Cidades Registradas por País
        - Avaliação Média por País
        - Preço Médio de Prato para Dois por País
        
    - Cities:
        - Cidades com mais Restaurantes na Base de Dados
        - Top 7 cidades com restaurantes de média avaliativa acima de 4
        - Top 7 cidades com restaurantes de média avaliativa abaixo de 2.5
        - Top 10 cidades com maiores diversidades gastronômicas
    
    - Cuisines:
        - Melhores Restaurantes dos Principais tipos Culinários
        - Top Restaurantes
        - Top Melhores Tipos de Culinária
        - Top Piores Tipos de Culinária
        
    """)