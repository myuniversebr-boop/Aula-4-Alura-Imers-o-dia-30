import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Salários", layout="wide")

# Carregar os dados
df = pd.read_csv("dados-imersao-final.csv")

# Filtro lateral
st.sidebar.header("Filtros")
ano = st.sidebar.selectbox("Ano", sorted(df['ano'].unique()))

# Aplicar filtro
df_filtrado = df[df['ano'] == ano]

# Métricas simples
st.metric("Salário Médio", f"R${df_filtrado['salario'].mean():,.2f}")

# Gráfico simples
fig = px.bar(
    df_filtrado.groupby('cargo')['salario'].mean().sort_values(ascending=False).head(10).reset_index(),
    x='cargo',
    y='salario',
    title='Top 10 Cargos por Salário Médio'
)
st.plotly_chart(fig, use_container_width=True)
