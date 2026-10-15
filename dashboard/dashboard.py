import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard IoT",
    page_icon="🌡️",
    layout="wide"
)

# Conexão com o banco de dados
DATABASE_URL = "postgresql+psycopg2://postgres:iot12345@localhost:5432/iot_db"
engine = create_engine(DATABASE_URL)

st.title("🌡️ Dashboard de Temperatura — IoT")
st.write("Análise das leituras de temperatura dos dispositivos.")

# Carrega os dados do banco
with engine.connect() as conexao:
    dados = pd.read_sql(
        "SELECT * FROM leituras_temperatura",
        conexao
    )

    media_dispositivo = pd.read_sql(
        "SELECT * FROM avg_temp_por_dispositivo",
        conexao
    )

    leituras_hora = pd.read_sql(
        "SELECT * FROM leituras_por_hora",
        conexao
    )

    temperaturas_dia = pd.read_sql(
        "SELECT * FROM temp_max_min_por_dia ORDER BY data",
        conexao
    )

# Indicadores principais
col1, col2, col3 = st.columns(3)

col1.metric("Total de leituras", f"{len(dados):,}".replace(",", "."))
col2.metric(
    "Temperatura média",
    f"{dados['temperatura'].mean():.2f} °C"
)
col3.metric(
    "Dispositivos/locais",
    str(dados["dispositivo_id"].nunique())
)

st.divider()

# Gráfico 1: temperatura média por dispositivo/local
st.subheader("1. Temperatura média por dispositivo/local")

fig1 = px.bar(
    media_dispositivo,
    x="dispositivo_id",
    y="temperatura_media",
    labels={
        "dispositivo_id": "Dispositivo/local",
        "temperatura_media": "Temperatura média (°C)"
    },
    title="Temperatura média registrada"
)

st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: quantidade de leituras por hora
st.subheader("2. Distribuição das leituras por hora")

fig2 = px.bar(
    leituras_hora,
    x="hora",
    y="quantidade_leituras",
    labels={
        "hora": "Hora do dia",
        "quantidade_leituras": "Quantidade de leituras"
    },
    title="Leituras registradas em cada hora"
)

st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: temperaturas máxima e mínima por dia
st.subheader("3. Temperaturas máxima e mínima por dia")

fig3 = px.line(
    temperaturas_dia,
    x="data",
    y=["temperatura_maxima", "temperatura_minima"],
    markers=True,
    labels={
        "data": "Data",
        "value": "Temperatura (°C)",
        "variable": "Medição"
    },
    title="Variação diária da temperatura"
)

st.plotly_chart(fig3, use_container_width=True)

# Tabela de dados
with st.expander("Consultar registros importados"):
    st.dataframe(dados, use_container_width=True)

engine.dispose()