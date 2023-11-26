import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

# importando a tabela
valor_import = pd.read_excel('/Users/brunoperrotta/primeiro projeto streamlit/import.xlsx', sheet_name='valor')

# tirando a coluna id, pois não tem utilidade nessa análise
valor_import = valor_import.drop(columns='Id')

# Reorganizando as colunas
vl_melted = valor_import.melt(id_vars=['País'], var_name='Ano', value_name='Valor(US$)')
valor = vl_melted[['Ano', 'País', 'Valor(US$)']]
valor['Ano'] = pd.to_datetime(valor['Ano'], format='%Y')
valor['Ano'] = valor['Ano'].dt.year


# agrupando por ano para ver o valor anual
valor_anual = valor.groupby(['Ano'])['Valor(US$)'].sum().reset_index()
valor_anual['Ano'] = pd.to_datetime(valor_anual['Ano'], format='%Y')
valor_anual['Ano'] = valor_anual['Ano'].dt.year

# Função para obter os top 5 países por ano
def top_countries_by_year(df):
    top_countries = (
        df.groupby('Ano')
        .apply(lambda x: x.nlargest(5, 'Valor(US$)'))
        .reset_index(drop=True)
    )
    return top_countries

# Aplicar a função para obter os top 5 países por ano
top_countries_by_year(valor)
top5 = top_countries_by_year(valor)

# Valor acumulado do 5 maiores de 1970-2022
group5 = top5.groupby(['País'])['Valor(US$)'].sum().sort_values(ascending=False).reset_index()
group5 =  group5.head(5)

st.title('Análise da importação brasileira de vinhos de mesa')

# organizando o dash
row1 = st.columns(2)
row2 = st.columns(2)

# coluna 1
fig_group5_total = px.bar(group5, x="País", y='Valor(US$)',text=group5['Valor(US$)'].apply(lambda x: f'{x:,.0f}'), color_discrete_sequence=px.colors.sequential.RdBu,
                          title='Valor acumulado dos 5 maiores exportadores de vinho para o Brasil entre 1970-2022')
fig_group5_total.update_layout(width=600,  height=460)
fig_group5_total.update_traces(textposition='outside', textfont=dict(color='black'))

with row1[0]:
     st.write(fig_group5_total)

# coluna 2
fig_vl_anual = px.line(valor_anual, x="Ano", y='Valor(US$)', color_discrete_sequence=px.colors.sequential.RdBu,
                       title='Valor anual de vinho importado pelo Brasil' )
fig_vl_anual.update_xaxes(dtick=2)
fig_vl_anual.update_yaxes(dtick=50000000)
fig_vl_anual.update_layout(width=600,  height=460)
with row1[1]:
     st.write(fig_vl_anual)


# coluna 3
'''filtro_ano_top5 = top5[(top5['Ano'] >= 1999) & (top5['Ano'] <= 2022)]

fig_top5 = px.scatter(filtro_ano_top5, x='Ano', y='Valor(US$)',
                 size='Valor(US$)', color='País',
                 hover_name='País', log_x=True, size_max=60, animation_frame='Ano',
                  color_discrete_map={
                     'Chile': 'darkred',      
                     'Argentina': 'lightblue', 
                     'Portugal': 'darkgreen',  
                     'Itália': 'blue',      
                     'França': 'pink'        
                 },
                  range_x=[1999, 2023], range_y=[0, 250000000])

# Personalizar o layout do gráfico
fig_top5.update_layout(
    title='Evolução dos 5 países que mais exportam vinho para o Brasil ao longo do tempo',
    xaxis_title='Ano',
    yaxis_title='Quantidade em Dólares',
    legend_title='Países'
)
fig_top5.update_yaxes(dtick=15000000)
fig_top5.update_layout(width=1200,  height=460)
fig_top5.update_traces(marker=dict(opacity=1))  # Definindo opacidade para 1 (sem transparência)

with row2[0]:
    st.write(fig_top5)
   
st.markdown("Fonte: EMBRAPA")'''

