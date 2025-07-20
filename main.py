import pandas as pd
import streamlit as st
import requests
from datetime import datetime
import plotly.express as px

# Configurações
st.set_page_config(
    page_title="Dashboard de Clima",
    layout="centered",
    page_icon="🌦️"
)

# Título
st.title("🌤️ Dashboard de Clima em Tempo Real")
st.markdown("---")

# Inputs alinhados
col1, col2 = st.columns([3,1])
cidade = col1.text_input("Digite o nome da cidade:", "Sorocaba")
buscar = col2.button("🔍 Buscar")

# API
api_key = "5259cb144f0e16bd92aba8d18e79198c"
base_url = "https://api.openweathermap.org/data/2.5/weather?"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"

if buscar:
    url = f"{base_url}q={cidade}&appid={api_key}&units=metric&lang=pt_br"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        st.success(f"✅ Dados carregados para {cidade.title()}")
        st.subheader(f"Clima em {cidade.title()} agora:")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("🌡️ Temperatura", f"{data['main']['temp']}°C")
        col_b.metric("🤗 Sensação", f"{data['main']['feels_like']}°C")
        col_c.metric("💧 Umidade", f"{data['main']['humidity']}%")
        
        st.write(f"💨 **Vento:** {data['wind']['speed']} m/s")
        st.write(f"⛅ **Descrição:** {data['weather'][0]['description'].capitalize()}")
        
        # Previsão
        url_f = f"{forecast_url}q={cidade}&appid={api_key}&units=metric&lang=pt_br"
        response_f = requests.get(url_f)
        data_f = response_f.json()
        
        forecast_list = data_f['list']
        temps, times = [], []
        
        for item in forecast_list:
            temps.append(item['main']['temp'])
            times.append(datetime.fromtimestamp(item['dt']))
        
        df = pd.DataFrame({'Data/Hora': times, 'Temperatura (°C)': temps})
        
        fig = px.line(df, x='Data/Hora', y='Temperatura (°C)',
                      title=f'🌡️ Previsão de Temperatura - {cidade.title()}',
                      template='plotly_dark')
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("🚫 Cidade não encontrada. Verifique o nome e tente novamente.")

st.markdown("---")
st.caption("Desenvolvido por Samuel de Moraes Delgado • Dados via OpenWeatherMap • Construído com Streamlit 🚀")
