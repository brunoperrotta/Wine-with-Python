import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

# table import
valor_import = pd.read_excel('https://github.com/brunoperrotta/first-streamlit/raw/49da611a630d53413dcdbd42cc9b32a81e9a5026/import.xlsx', sheet_name='valor', engine='openpyxl')

# droping id column
valor_import = valor_import.drop(columns='Id')

# rerranging the columns
vl_melted = valor_import.melt(id_vars=['País'], var_name='Ano', value_name='Valor(US$)')
valor = vl_melted[['Ano', 'País', 'Valor(US$)']]
valor['Ano'] = pd.to_datetime(valor['Ano'], format='%Y')
valor['Ano'] = valor['Ano'].dt.year


# grouping by year
valor_anual = valor.groupby(['Ano'])['Valor(US$)'].sum().reset_index()
valor_anual['Ano'] = pd.to_datetime(valor_anual['Ano'], format='%Y')
valor_anual['Ano'] = valor_anual['Ano'].dt.year

# function to get top 5 countries per year
def top_countries_by_year(df):
    top_countries = (
        df.groupby('Ano')
        .apply(lambda x: x.nlargest(5, 'Valor(US$)'))
        .reset_index(drop=True)
    )
    return top_countries


top_countries_by_year(valor)
top5 = top_countries_by_year(valor)

# Evolution of the top 5 countries that export the most wine to Brazil over time
group5 = top5.groupby(['País'])['Valor(US$)'].sum().sort_values(ascending=False).reset_index()
group5 =  group5.head(5)

st.title('Analysis of Brazilian Importation of Table Wines')

# organizing the dashboard
row1 = st.columns(2)
row2 = st.columns(2)

# column 1
fig_group5_total = px.bar(group5, x="País", y='Valor(US$)',text=group5['Valor(US$)'].apply(lambda x: f'{x:,.0f}'), color_discrete_sequence=px.colors.sequential.RdBu,
                          title='Accumulated value of the top 5 wine exporters to Brazil between 1970-2022',
                         labels={'País': 'Country', 'Valor(US$)': 'US$'})
fig_group5_total.update_layout(width=600,  height=460)
fig_group5_total.update_traces(textposition='outside', textfont=dict(color='black'))

with row1[0]:
     st.write(fig_group5_total)

# column 2
fig_vl_anual = px.line(valor_anual, x="Ano", y='Valor(US$)', color_discrete_sequence=px.colors.sequential.RdBu,
                       title='Annual value of table wine imported by Brazil',
                      labels={'Ano': 'Year', 'Valor(US$)': 'US$'})
fig_vl_anual.update_xaxes(dtick=2)
fig_vl_anual.update_yaxes(dtick=50000000)
fig_vl_anual.update_layout(width=600,  height=460)
with row1[1]:
     st.write(fig_vl_anual)


# column 3
filtro_ano_top5 = top5[(top5['Ano'] >= 1999) & (top5['Ano'] <= 2022)]

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

#  chart layout
fig_top5.update_layout(
    title='Evolution of the top 5 countries that export the most wine to Brazil over time',
    xaxis_title='Year',
    yaxis_title='US$',
    legend_title='Países'
)
fig_top5.update_yaxes(dtick=15000000)
fig_top5.update_layout(width=1200,  height=460)
fig_top5.update_traces(marker=dict(opacity=1))  # Definindo opacidade para 1 (sem transparência)

with row2[0]:
    st.write(fig_top5)
   
st.markdown("Fonte: EMBRAPA")

