#Importações de bibliotecas necessárias
import pandas as pd 
import streamlit as st
import requests
from datetime import datetime
import plotly.express as px
import time

# =================== CONFIGURAÇÕES =====================
st.set_page_config(
    page_title="Dashboard de Clima", #Título da aba
    layout="centered", #Centralização do layout
    page_icon="🌦️" #Ícone da aba
)

# =================== HEADER ============================
st.title("🌤️ Dashboard de Clima em Tempo Real") #Título da página
st.caption("Receba informações climáticas atuais e previsão com gráficos interativos.") #Informação adicional embaixo do título
st.markdown("---") #Separador horizontal

# =================== INPUTS COM LAYOUT =================
col1, col2 = st.columns([4, 1]) #Colunas para layout, a primeira mais larga que a segunda
cidade = col1.text_input("🌍 Digite o nome da cidade:", "Sorocaba") #Input da cidade
unidade = col2.selectbox("🌡️ Unidade", ["°C", "°F"]) #Seleção do tipo de medida

buscar = st.button("🔍 Buscar") #Botão de busca


# =================== CONVERSÃO DE UNIDADE ==============
unit_param = "metric" if unidade == "°C" else "imperial"
unit_symbol = "°C" if unidade == "°C" else "°F"

# =================== API CONFIG ========================
api_key = "5259cb144f0e16bd92aba8d18e79198c"
base_url = "https://api.openweathermap.org/data/2.5/weather?"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"

# =================== BUSCA CLIMA =======================
if buscar:
    with st.spinner("🔄 Buscando dados do clima..."): #Carregamento da página por 0.5seg
        time.sleep(0.5)
        url = f"{base_url}q={cidade}&appid={api_key}&units={unit_param}&lang=pt_br" #base URL da API com parâmetros
        response = requests.get(url) #Requisição GET para a API

        if response.status_code == 200: #
            data = response.json() #Dados retornados da API em formato JSON

            st.success(f"✅ Dados carregados para **{cidade.title()}**.") #Mensagem de sucesso
            st.subheader(f"📍 Clima em {cidade.title()} agora:") #Informação adicional

            # ===== CARDS DE DADOS =====
            col_a, col_b, col_c = st.columns(3) #Três colunas para exibir dados
            col_a.metric("🌡️ Temperatura", f"{data['main']['temp']}{unit_symbol}") #Temperatura
            col_b.metric("🤗 Sensação", f"{data['main']['feels_like']}{unit_symbol}") #Sensação Térmica
            col_c.metric("💧 Umidade", f"{data['main']['humidity']}%") #Umidade

            col_d, col_e = st.columns(2) #Duas colunas para exibir dados adicionais
            col_d.markdown(f"💨 **Vento:** {data['wind']['speed']} m/s") #Vento
            col_e.markdown(f"⛅ **Descrição:** {data['weather'][0]['description'].capitalize()}") #Descrição do clima

            # ===== PREVISÃO DO TEMPO =====
            st.markdown("---") #Separador horizontal
            st.subheader(f"📈 Previsão para os próximos dias em {cidade.title()}") #Subtítulo da previsão dos próximos 5 dias

            url_f = f"{forecast_url}q={cidade}&appid={api_key}&units={unit_param}&lang=pt_br" #URL da API para previsão do tempo
            response_f = requests.get(url_f) #Requisição GET para a API de previsão
            data_f = response_f.json() #Dados retornados da API de previsão em formato JSON

            forecast_list = data_f['list'] #Lista de previsões retornadas
            temps, times, humidity = [], [], [] #Listas para armazenar temperatura, hora e umidade

            for item in forecast_list: #Iteração sobre cada item da previsão
                temps.append(item['main']['temp']) #Temperatura
                humidity.append(item['main']['humidity']) #Umidade
                times.append(datetime.fromtimestamp(item['dt'])) #Hora da previsão convertida de timestamp

            df = pd.DataFrame({ #Criação de DataFrame com os dados coletados
                'Data/Hora': times,
                'Temperatura': temps,
                'Umidade (%)': humidity
            })

            fig = px.bar(df, x='Data/Hora', y='Temperatura', #Criação de gráfico de barras
             title=f'🌡️ Previsão de Temperatura - {cidade.title()}', #Título
             template='plotly_dark') #Tema do gráfico

            fig.update_traces(marker=dict(line=dict(width=0), color="#531fb4"))  #Personalização das barras

            fig.update_layout(
                title_x=0.5, #Centralização do título
                font=dict(size=14), #Tamanho da fonte
                plot_bgcolor='#0E1117', #Cor de fundo do gráfico
                paper_bgcolor='#0E1117', #Cor de fundo do papel
                margin=dict(l=20, r=20, t=60, b=20) #Margens do gráfico
            )

            st.plotly_chart(fig, use_container_width=True) #Exibição do gráfico de temperatura

            # ===== UMIDADE OPCIONAL =====
            with st.expander("💧 Visualizar gráfico de umidade"): #Com o botão de expansão aberto
                fig_h = px.line(df, x='Data/Hora', y='Umidade (%)',
                                title=f'💧 Umidade Relativa - {cidade.title()}',
                                template='plotly_dark',
                                markers=True)
                fig_h.update_traces(line=dict(width=2), marker=dict(size=4))
                fig_h.update_layout(
                    title_x=0.5,
                    font=dict(size=14),
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig_h, use_container_width=True)

        else:
            st.error("🚫 Cidade não encontrada. Verifique o nome e tente novamente.")

# =================== FOOTER ============================
st.markdown("---")
st.caption("Desenvolvido por Samuel de Moraes Delgado • Dados via OpenWeatherMap • Construído com Streamlit 🚀")
