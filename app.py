import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Salários", layout="wide")

# Carregar os dados
df = pd.read_csv("dados-imersao-final.csv")

# --- Filtros na barra lateral ---
st.sidebar.header("Filtros")
ano = st.sidebar.selectbox("Ano", sorted(df['ano'].dropna().unique()))
pais = st.sidebar.multiselect("País (ISO3)", sorted(df['residencia_iso3'].dropna().unique()))
senioridade = st.sidebar.multiselect("Senioridade", sorted(df['senioridade'].dropna().unique()))

# --- Aplicar filtros ---
df_filtrado = df[df['ano'] == ano]

if pais:
    df_filtrado = df_filtrado[df_filtrado['residencia_iso3'].isin(pais)]

if senioridade:
    df_filtrado = df_filtrado[df_filtrado['senioridade'].isin(senioridade)]

# --- Métricas rápidas ---
st.markdown("### Indicadores Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Salário Médio", f"R${df_filtrado['salario'].mean():,.2f}")
col2.metric("Salário Máximo", f"R${df_filtrado['salario'].max():,.2f}")
col3.metric("Salário Mínimo", f"R${df_filtrado['salario'].min():,.2f}")

# --- Gráficos lado a lado ---
st.markdown("### Visualizações")

colA, colB = st.columns(2)

with colA:
    fig1 = px.bar(
        df_filtrado.groupby('cargo')['salario'].mean().sort_values(ascending=False).head(10).reset_index(),
        x='cargo',
        y='salario',
        title='Top 10 Cargos por Salário Médio',
        labels={'cargo': 'Cargo', 'salario': 'Salário Médio'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    fig2 = px.box(
        df_filtrado,
        x='senioridade',
        y='salario',
        title='Distribuição Salarial por Senioridade',
        labels={'senioridade': 'Senioridade', 'salario': 'Salário'}
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico extra: salário médio por país ---
st.markdown("### Salário Médio por País")
fig3 = px.bar(
    df_filtrado.groupby('residencia_iso3')['salario'].mean().reset_index(),
    x='residencia_iso3',
    y='salario',
    title='Salário Médio por País',
    labels={'residencia_iso3': 'País (ISO3)', 'salario': 'Salário Médio'}
)
st.plotly_chart(fig3, use_container_width=True)
