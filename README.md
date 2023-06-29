# Problema de Negócio

A empresa Fome Zero é um marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O CEO da empresa foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero. Para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, de modo a mapear a base de restaurantes cadastrados e entender o andamento do negócio por meio das seguintes informações:

## 📋 Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?.
    
## 🌍 Visão Países

1.	Qual a quantidade de restaurantes registrados por país?
2.	Qual a quantidade de cidades registrados por país?
3.	Qual a média de avaliações feitas por país?
4.	Qual a média de preço de um prato para duas pessoas por país?

## 🏨 Visão Cidades

1.	Quais são as cidades com mais restaurantes na base de dados?
2.	Quais são as cidades com restaurantes com média de avaliação acima de 4?
3.	Quais são as cidades com restaurantes com média de avaliação abaixo de 2.5?
4.	Quais são as cidades com mais restaurantes com tipos culinários distintos?

## 🍽️ Visão Culinária

1.	Quais são os melhores restaurantes dos principais tipos culinários?
2.	Quais são os restaurantes com maiores avaliações? 
3.	Quais são os melhores tipos de culinárias?
4.	Quais são os piores tipos de culinárias?

O desafio é responder a essas questões e transformar seus resultados em dashboards que permitam o rápido entendimento do andamento do negócio. Os dados da empresa podem ser obtidos no link do Kaggle abaixo (arquivo zomato.csv):
https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

# Premissas do negócio

1.	O modelo de negócio assumido é um Marketplace.
2.	As 3 principais visões do negócio foram: Visão Países, Visão Cidades e Visão Culinária.
3.	Os preços de um prato para duas pessoas estão nas suas respectivas moedas de cada país.
4.	Qualquer análise que contemple dados financeiros a moeda corrente do país será apresentada junto ao dado.

# Estratégia da solução

1. As análises partiram da resolução das questões propostas pelo CEO segmentadas pelas visões país, cidade e gastronomia;
2. Em termos de ferramental utilizou-se:
    * Jupyter Notebook - Análises prévias e rascunho do script final;
    * Bibliotecas de manipulação de dados - Pandas e Numpy;
    * Bibliotecas de visualização de dados - Matplotlib, Plotly, Folium;
    * Jupyter Lab - Script Python final;
    * Streamlit e Streamlit Cloud- Visualização do dashboard e coloca-lo em produção.

# Top 3 insights de dados

1. O Brasil possui a pior operação: apenas 3 cidades cadastradas, todas figurando no top 5 das cidades piores avaliadas, o que o coloca também como o país de pior nota média de avaliação. É o único da América do Sul;
2. Apenas cerca da metade dos restaurantes que aceitam pedidos online também fazem entregas;
3. Nenhuma das 10 culinárias mais ofertadas encontram-se entre as melhores avaliadas, pelos contrário, 6 delas estão entre as 20 mais caras e piores avaliadas.

# O produto final do projeto

Dashboard online hospedado na Streamlit Cloud o qual pode ser acessado pelo link: https://dashboard-fome-zero.streamlit.app/

# Conclusão

O objetivo do projeto foi criar uma visualização de dados a qual permitisse o acompanhamento das principais características do negócio e de como elas se distribuem geograficamente.

O marketplace Fome Zero tem atuação global com forte presença nos continentes asiático e norte americano apresentando significativa diversidade gastronômica tendo os pratos do norte da Índia como a base de seu cardápio. 

# Próximos Passos

1. Especializar a análise por país gerando métricas de acompanhamento mais local dos negócios de modo a tornar os processos decisórios mais precisos conforme as particularidades geográficas;
2. Padronizar os dados financeiros e de avaliação de modo a tornar a comparação entre restaurantes e países mais justas/precisas na análise;
3. Analisar o custo e/ou benefício de se expandir ou retrair a diversidade gastronômica considerando o preço dos pratos e as avaliações dos restaurantes.
