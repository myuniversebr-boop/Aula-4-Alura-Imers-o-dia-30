import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Dashboard de Salários", layout="wide")

# Carregar os dados
df = pd.read_csv("dados-imersao-final.csv")

# --- Barra lateral com filtros ---
st.sidebar.header("Filtros")

ano = st.sidebar.selectbox("Selecione o ano", sorted(df['ano'].unique()))
empresa = st.sidebar.multiselect("Selecione a empresa", sorted(df['empresa'].dropna().unique()))
pais = st.sidebar.multiselect("Selecione o país (ISO3)", sorted(df['residencia_iso3'].dropna().unique()))
senioridade = st.sidebar.multiselect("Selecione a senioridade", sorted(df['senioridade'].dropna().unique()))

# --- Aplicar filtros ---
df_filtrado = df[df['ano'] == ano]

if empresa:
    df_filtrado = df_filtrado[df_filtrado['empresa'].isin(empresa)]

if pais:
    df_filtrado = df_filtrado[df_filtrado['residencia_iso3'].isin(pais)]

if senioridade:
    df_filtrado = df_filtrado[df_filtrado['senioridade'].isin(senioridade)]

# --- Métricas rápidas ---
st.markdown("### Indicadores Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Salário Médio", f"${df_filtrado['usd'].mean():,.2f}")
col2.metric("Salário Máximo", f"${df_filtrado['usd'].max():,.2f}")
col3.metric("Salário Mínimo", f"${df_filtrado['usd'].min():,.2f}")

# --- Layout dos gráficos ---
st.markdown("### Visualizações")

colA, colB = st.columns(2)

with colA:
    fig1 = px.bar(
        df_filtrado.groupby('cargo')['usd'].mean().sort_values(ascending=False).head(10).reset_index(),
        x='cargo',
        y='usd',
        title='Top 10 Cargos por Salário Médio (USD)',
        labels={'cargo': 'Cargo', 'usd': 'Salário Médio (USD)'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    fig2 = px.box(
        df_filtrado,
        x='senioridade',
        y='usd',
        title='Distribuição Salarial por Senioridade',
        labels={'senioridade': 'Senioridade', 'usd': 'Salário (USD)'}
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico extra: salário médio por país ---
st.markdown("### Salário Médio por País")
fig3 = px.bar(
    df_filtrado.groupby('residencia_iso3')['usd'].mean().reset_index(),
    x='residencia_iso3',
    y='usd',
    title='Salário Médio por País (USD)',
    labels={'residencia_iso3': 'País (ISO3)', 'usd': 'Salário Médio (USD)'}
)
st.plotly_chart(fig3, use_container_width=True)
        title='Top 10 Cargos por Salário

