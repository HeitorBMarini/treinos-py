import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# URL direta para o arquivo .xlsx
xlsx_url = "https://docs.google.com/spreadsheets/d/1xwJHd322Znz0pwqK6CGNBZl4-EGAx837OL8IDPp7TbI/pub?output=xlsx"

# Fazer download do arquivo .xlsx e ler com pandas
response = requests.get(xlsx_url)
df = pd.read_excel(BytesIO(response.content))

# Convertendo a coluna de data para o formato datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Criar a barra lateral com logo e filtro de atletas
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Logo-google-g.png/1200px-Logo-google-g.png", width=100)
st.sidebar.title("Navegação")

# Seleção de atleta
atletas = df['Nome do atleta'].dropna().unique()  # Pegar todos os nomes de atletas únicos, ignorando NaNs
atleta_selecionado = st.sidebar.selectbox("Selecione o Atleta", atletas)

# Filtrar os dados com base no nome do atleta selecionado
df_filtrado = df[df['Nome do atleta'] == atleta_selecionado]

# Filtro de data
data_inicio = st.sidebar.date_input("Data de Início", df_filtrado['Timestamp'].min())
data_fim = st.sidebar.date_input("Data de Fim", df_filtrado['Timestamp'].max())

# Filtrar os dados com base no intervalo de datas
df_filtrado = df_filtrado[(df_filtrado['Timestamp'] >= pd.to_datetime(data_inicio)) & (df_filtrado['Timestamp'] <= pd.to_datetime(data_fim))]

# Título da aplicação
st.title(f"Dashboard de {atleta_selecionado}")

# Dividir em quatro seções: duas colunas em cima e duas embaixo
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Gráficos na primeira linha
with col1:
    st.write(f"Gráfico de Fadiga para {atleta_selecionado}:")
    st.bar_chart(df_filtrado['Fadiga'])

with col2:
    st.write(f"Gráfico de Sono para {atleta_selecionado}:")
    st.bar_chart(df_filtrado['TáSono'])

# Gráficos na segunda linha
with col3:
    st.write(f"Gráfico de Estresse para {atleta_selecionado}:")
    st.bar_chart(df_filtrado['Estresse'])

with col4:
    st.write(f"Gráfico de Dor Muscular para {atleta_selecionado}:")
    st.bar_chart(df_filtrado['Dor Muscular'])

# Gráficos de Pizza
st.subheader(f"Distribuição de Prontidão e Taxa de Recuperação para {atleta_selecionado}")

col5, col6 = st.columns(2)

with col5:
    st.write(f"Prontidão (o quanto eu me sinto preparada para o treino):")
    prontidao_counts = df_filtrado['Prontidão (o quanto eu me sinto preparada para o treino)'].value_counts()
    st.write(prontidao_counts)
    st.pyplot(prontidao_counts.plot.pie(autopct='%1.1f%%', figsize=(5, 5), title="Prontidão").figure)

with col6:
    st.write(f"Qual sua taxa de recuperação?:")
    recuperacao_counts = df_filtrado['Qual sua taxa de recuperação?'].value_counts()
    st.write(recuperacao_counts)
    st.pyplot(recuperacao_counts.plot.pie(autopct='%1.1f%%', figsize=(5, 5), title="Taxa de Recuperação").figure)

# Gráfico de Barras para Locais de Dor
st.subheader(f"Locais de Dor para {atleta_selecionado}")
locais_dor_counts = df_filtrado['Locais de dor'].value_counts()
st.bar_chart(locais_dor_counts)
