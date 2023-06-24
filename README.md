# Fome_Zero
This repository contains files and scripts to help the business team make quick decisions from a strategic dashboard of the FomeZero marketplace.
1. Problema de negócio 

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

A Fome Zero acaba de contratar um novo CEO, o senhor Kleiton Guerra, que deseja que você, recém contratado como cientista de dados o ajude a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer utilizando dados. Estes pontos chaves deverão ser apresentados em forma de KPIs estratégicos que proporcionem a tomada de decisões simples, mas não menores importantes.

O CEO gostaria de ver as seguintes métricas de crescimento: A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta clientes a restaurantes. Através desse aplicativo, é possível analisar em qual restaurantes realizar pedido de uma refeição, em qualquer restaurante cadastrado, fornecendo dados como localização, preço médio do prato para duas pessoas, tipo de culinária, se aceita reserva, se faz entregas, etc. 

O Kleiton Guerra ainda não tem visibilidade completa dos KPIs de crescimento da empresa. Você foi contratado como um Cientista de Dados para criar soluções de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter um os principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes. A Fome Zero possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre dois clientes: compradores de comida e restaurantes. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

Visão Países: 
1. Métricas gerais: Restaurantes, Países, Cidades, Avaliações e Culinária registrada na base de dados. 
2. País com maior quantidade de Cidades, Restaurante, Preço de prato para dois, Culinárias distintas e Avaliações registradas. 
3. Distribuição dos restaurantes registrados por país. 
4. Distribuição de cidades registradas por país. 
4. Distribuição das médias de avaliações por país. 
5. Distribuição da média de preço para dois por país.
6. Localização de todos os restaurantes registrados com a informação do nome do restaurante, do tipo de culinária, preço médio para dois, avaliação média e a coloração do localizador de acordo com a média do estabelecimento.

Visão Cidades: 
1. Métricas gerais: Cidade que possui mais restaurantes com reservas, que mais fazem entregas e que mais faz pedidos online. 
2. Cidade com maior quantidade de restaurantes registrados. 
3. Distribuição de cidades com restaurantes com avaliações maiores ou igual a 4. 
4. Distribuição de cidades com restaurantes com avaliações menores ou igual a 2,5. 
4. Distribuição de restaurantes com maior número de culinária distinta. 

Visão Culinária: 
1. Métricas gerais: Culinárias melhor avaliadas por tipo de culinária. 
2. Distribuição de Países contendo cidade, culinária, restaurante, média de avaliação média agregada, média de preço de prato para 2 e média de votos registrados. 
3. Distribuição de melhor e pior culinária avaliada. 
4. Distribuição países em Maior quantidade de Restaurantes que Fazem Entrega e aceitam Pedidos Online por tipo de culinária. 

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibem essas métricas da melhor forma possível para o CEO. 

2. Premissas do negócio

1. Marketplace foi o modelo de negócio assumido. 
3. As 3 principais visões do negócio foram: Visão por países, visão cidades e visão culinária.

3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa: 
1. Visão da distribuição por países 
2. Visão da distribuição por cidades
3. Visão da distribuição por culinária

Cada visão é representada pelo seguinte conjunto de métricas. 

1. Visão da distribuição por países:

a. Número de restaurantes registrados. 
b. Número de países registrados. 
c. Número de cidades registradas. 
d. Número de avaliações registradas. 
e. Número de culinárias registradas. 
f. País com maior número de cidades registradas.
g. País com maior número de restaurantes registrados.
h. País com maior número de preço médio para dois.
i. País com maior número de culinária distinta registrada.
j. País com maior número de avaliações registradas.
k. Distribuição de restaurantes registrados por país.
l. Distribuição de cidades registradas por país.
m. Distribuição de média de avaliações registradas por país.
n. Distribuição de preço médio para dois  por país.
o. Distribuição dos restaurantes no mapa com informações gerais dos restaurantes.




2. Visão da distribuição por cidade
 
a. Possui mais restaurantes com reservas.
b. Possui mais restaurantes que fazem entrega.
c. Possui mais restaurantes que aceitam pedidos online. 
d. Distribuição do top 10 com maior restaurantes registrados por cidade.
d. Distribuição do top 10 com restaurantes com avaliações iguais ou maiores a 4, registrados por cidade. 
e. Distribuição do top 10 com restaurantes com avaliações iguais ou menores a 2,5, registrados por cidade. 
f. Distribuição do top 10 de restaurantes com maior número de culinárias distintas registradas por cidade. 

3. Visão da distribuição por culinária
 
a. 5 culinárias com melhor média de avaliações. 
b. Distribuição de restaurantes por cidade, país, tipo de culinária a partir da média de preço para 2, média de votos e média de avaliação média agregada. 
c. Distribuição das melhores culinárias avaliadas. 
d. Distribuição das piores culinárias avaliadas. 
e. Distribuição de países em Maior quantidade de Restaurantes que Fazem Entrega e aceitam Pedidos Online por tipo de culinária. 

4. Top 3 Insights de dados 

1. A Índia é o país com maior utilização do aplicativo pela visão de registros na base por país, em pelo menos 4 itens avaliados. 
2. Apesar da Índia ser o País com maiores números na base, a maior média de avaliações médias registradas é dos EUA, com praticamente metade das cidades registradas. 
3. A média de avaliações não acompanha a quantidade de restaurantes registrados. 

5. O produto final do projeto 
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através desse link: https://project-currycompany.streamlit.app/ 

6. Conclusão 

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibem essas métricas da melhor forma possível para o CEO. Da visão de países, podemos inferir que pode haver uma subnotificação de avaliações dos restaurantes. 

7. Próximo passos 

1. Reduzir o número de métricas. 
2. Criar novos filtros. 
3. Adicionar novas visões de negócio.

Portfólio….
Desenvolvimento de um Painel Gerencial para Negócio com o Streamlit 
Nesse projeto, os conceitos de Programação em Python, manipulação de dados, pensamento estratégico e lógica de negócio, junto com ferramentas de desenvolvimento web como o Streamlit e Github, foram usados para desenvolver um painel gerencial com as principais métricas de uma empresa marketplace de delivery de comida. O resultado final do projeto foi um painel hospedado em um ambiente Cloud e disponibilizado através de um link web. O painel pode ser acessado por qualquer dispositivo conectado na internet. 

As ferramentas utilizadas foram: 
Python 
Jupyter Lab 
Terminal Streamlit 
Streamlit Cloud
Github 
