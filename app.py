import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px

# URL direta para o arquivo .xlsx
xlsx_url = "https://docs.google.com/spreadsheets/d/1xwJHd322Znz0pwqK6CGNBZl4-EGAx837OL8IDPp7TbI/pub?output=xlsx"

# Fazer download do arquivo .xlsx e ler com pandas
response = requests.get(xlsx_url)
df = pd.read_excel(BytesIO(response.content))

# Convertendo a coluna de data para o formato datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Criar a barra lateral com logo e filtros
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Logo-google-g.png/1200px-Logo-google-g.png", width=100)
st.sidebar.title("Navegação")

# Seleção opcional de atleta
atleta_selecionado = st.sidebar.selectbox("Selecione o Atleta (Opcional)", options=["Todos"] + df['Nome do atleta'].dropna().unique().tolist())

# Filtro de data (opcional)
data_inicio = st.sidebar.date_input("Data de Início", df['Timestamp'].min())
data_fim = st.sidebar.date_input("Data de Fim", df['Timestamp'].max())

# Aplicar filtro de data, se as datas forem fornecidas
df_filtrado = df.copy()
if data_inicio and data_fim:
    df_filtrado = df_filtrado[(df_filtrado['Timestamp'] >= pd.to_datetime(data_inicio)) & (df_filtrado['Timestamp'] <= pd.to_datetime(data_fim))]

# Título da aplicação
if atleta_selecionado == "Todos":
    st.title("Dashboard Geral dos Atletas")
else:
    st.title(f"Dashboard de {atleta_selecionado}")

# Função para criar gráficos de barras para cada atleta
def criar_graficos_para_atleta(atleta_df, atleta_nome):
    st.subheader(f"Análise das Respostas de {atleta_nome}")
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    
    with col1:
        st.write("Prontidão:")
        fig_prontidao = px.bar(atleta_df, x='Timestamp', y='Prontidão (o quanto eu me sinto preparada para o treino)', 
                               hover_data={'Nome do atleta': True}, title="Prontidão")
        fig_prontidao.update_layout(showlegend=False)
        st.plotly_chart(fig_prontidao)

    with col2:
        st.write("Taxa de Recuperação:")
        fig_recuperacao = px.bar(atleta_df, x='Timestamp', y='Qual sua taxa de recuperação?', 
                                 hover_data={'Nome do atleta': True}, title="Taxa de Recuperação")
        fig_recuperacao.update_layout(showlegend=False)
        st.plotly_chart(fig_recuperacao)

    with col3:
        st.write("Fadiga:")
        fig_fadiga = px.bar(atleta_df, x='Timestamp', y='Fadiga', hover_data={'Nome do atleta': True}, title="Fadiga")
        fig_fadiga.update_layout(showlegend=False)
        st.plotly_chart(fig_fadiga)

    with col4:
        st.write("Sono:")
        fig_sono = px.bar(atleta_df, x='Timestamp', y='TáSono', hover_data={'Nome do atleta': True}, title="Sono")
        fig_sono.update_layout(showlegend=False)
        st.plotly_chart(fig_sono)

    with col5:
        st.write("Estresse:")
        fig_estresse = px.bar(atleta_df, x='Timestamp', y='Estresse', hover_data={'Nome do atleta': True}, title="Estresse")
        fig_estresse.update_layout(showlegend=False)
        st.plotly_chart(fig_estresse)

    with col6:
        st.write("Dor Muscular:")
        fig_dor_muscular = px.bar(atleta_df, x='Timestamp', y='Dor Muscular', hover_data={'Nome do atleta': True}, title="Dor Muscular")
        fig_dor_muscular.update_layout(showlegend=False)
        st.plotly_chart(fig_dor_muscular)

# Função para criar gráficos comparativos para todos os atletas
def criar_graficos_comparativos(df):
    st.subheader("Comparativo entre Todos os Atletas")
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    
    with col1:
        st.write("Prontidão:")
        fig_prontidao = px.bar(df, x='Nome do atleta', y='Prontidão (o quanto eu me sinto preparada para o treino)', 
                               color='Nome do atleta', barmode='group', title="Comparativo de Prontidão")
        st.plotly_chart(fig_prontidao)

    with col2:
        st.write("Taxa de Recuperação:")
        fig_recuperacao = px.bar(df, x='Nome do atleta', y='Qual sua taxa de recuperação?', 
                                 color='Nome do atleta', barmode='group', title="Comparativo de Taxa de Recuperação")
        st.plotly_chart(fig_recuperacao)

    with col3:
        st.write("Fadiga:")
        fig_fadiga = px.bar(df, x='Nome do atleta', y='Fadiga', color='Nome do atleta', barmode='group', title="Comparativo de Fadiga")
        st.plotly_chart(fig_fadiga)

    with col4:
        st.write("Sono:")
        fig_sono = px.bar(df, x='Nome do atleta', y='TáSono', color='Nome do atleta', barmode='group', title="Comparativo de Sono")
        st.plotly_chart(fig_sono)

    with col5:
        st.write("Estresse:")
        fig_estresse = px.bar(df, x='Nome do atleta', y='Estresse', color='Nome do atleta', barmode='group', title="Comparativo de Estresse")
        st.plotly_chart(fig_estresse)

    with col6:
        st.write("Dor Muscular:")
        fig_dor_muscular = px.bar(df, x='Nome do atleta', y='Dor Muscular', color='Nome do atleta', barmode='group', title="Comparativo de Dor Muscular")
        st.plotly_chart(fig_dor_muscular)

# Exibir gráficos
if atleta_selecionado == "Todos":
    criar_graficos_comparativos(df_filtrado)
    for atleta in df_filtrado['Nome do atleta'].dropna().unique():
        atleta_df = df_filtrado[df_filtrado['Nome do atleta'] == atleta]
        criar_graficos_para_atleta(atleta_df, atleta)
else:
    criar_graficos_para_atleta(df_filtrado, atleta_selecionado)
