import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Dashboard Salários", layout="wide")

# Carregar dados
df = pd.read_csv("dados-imersao-final.csv")

# --- Barra lateral com filtros ---
st.sidebar.header("Filtros")

ano_selecionado = st.sidebar.selectbox("Selecione o ano", df['ano'].unique())
senioridade_selecionada = st.sidebar.multiselect("Selecione a senioridade", df['senioridade'].unique())
empresa_selecionada = st.sidebar.multiselect("Selecione a empresa", df['empresa'].unique())

# --- Aplicar filtros ---
df_filtrado = df[df['ano'] == ano_selecionado]

if senioridade_selecionada:
    df_filtrado = df_filtrado[df_filtrado['senioridade'].isin(senioridade_selecionada)]

if empresa_selecionada:
    df_filtrado = df_filtrado[df_filtrado['empresa'].isin(empresa_selecionada)]

# --- Layout em colunas ---
col1, col2 = st.columns(2)

# Gráfico 1: Top 10 cargos por salário
with col1:
    fig1 = px.bar(
        df_filtrado.head(10),
        x='cargo',
        y='salario',
        title=f'Top 10 Cargos por Salário ({ano_selecionado})'
    )
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Distribuição de salários por senioridade
with col2:
    fig2 = px.box(
        df_filtrado,
        x='senioridade',
        y='salario',
        title='Distribuição de Salários por Senioridade'
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico extra: evolução dos salários ao longo dos anos ---
fig3 = px.line(
    df,
    x='ano',
    y='salario',
    color='cargo',
    title='Evolução Salarial por Cargo'
)
st.plotly_chart(fig3, use_container_width=True)

# --- Métricas rápidas ---
st.subheader("Indicadores")
colA, colB, colC = st.columns(3)
colA.metric("Salário Médio", round(df_filtrado['salario'].mean(), 2))
colB.metric("Salário Máximo", df_filtrado['salario'].max())

colC.metric("Salário Mínimo", df_filtrado['salario'].min())
