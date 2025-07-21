import pandas as pd
import streamlit as st
import requests
from datetime import datetime
import plotly.express as px
import time

# =================== CONFIGURAÇÕES =====================
st.set_page_config(
    page_title="Dashboard de Clima",
    layout="centered",
    page_icon="🌦️"
)

# =================== HEADER ============================
st.title("🌤️ Dashboard de Clima em Tempo Real")
st.caption("Receba informações climáticas atuais e previsão com gráficos interativos.")
st.markdown("---")

# =================== INPUTS COM LAYOUT =================
col1, col2 = st.columns([4, 1])
cidade = col1.text_input("🌍 Digite o nome da cidade:", "Sorocaba")
unidade = col2.selectbox("🌡️ Unidade", ["°C", "°F"])

st.write(" ")# Adiciona espaçamento
buscar = st.button("🔍 Buscar")


# =================== CONVERSÃO DE UNIDADE ==============
unit_param = "metric" if unidade == "°C" else "imperial"
unit_symbol = "°C" if unidade == "°C" else "°F"

# =================== API CONFIG ========================
api_key = "5259cb144f0e16bd92aba8d18e79198c"
base_url = "https://api.openweathermap.org/data/2.5/weather?"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"

# =================== BUSCA CLIMA =======================
if buscar:
    with st.spinner("🔄 Buscando dados do clima..."):
        time.sleep(0.5)
        url = f"{base_url}q={cidade}&appid={api_key}&units={unit_param}&lang=pt_br"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            st.success(f"✅ Dados carregados para **{cidade.title()}**.")
            st.subheader(f"📍 Clima em {cidade.title()} agora:")

            # ===== CARDS DE DADOS =====
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("🌡️ Temperatura", f"{data['main']['temp']}{unit_symbol}")
            col_b.metric("🤗 Sensação", f"{data['main']['feels_like']}{unit_symbol}")
            col_c.metric("💧 Umidade", f"{data['main']['humidity']}%")

            col_d, col_e = st.columns(2)
            col_d.markdown(f"💨 **Vento:** {data['wind']['speed']} m/s")
            col_e.markdown(f"⛅ **Descrição:** {data['weather'][0]['description'].capitalize()}")

            # ===== PREVISÃO DO TEMPO =====
            st.markdown("---")
            st.subheader(f"📈 Previsão para os próximos dias em {cidade.title()}")

            url_f = f"{forecast_url}q={cidade}&appid={api_key}&units={unit_param}&lang=pt_br"
            response_f = requests.get(url_f)
            data_f = response_f.json()

            forecast_list = data_f['list']
            temps, times, humidity = [], [], []

            for item in forecast_list:
                temps.append(item['main']['temp'])
                humidity.append(item['main']['humidity'])
                times.append(datetime.fromtimestamp(item['dt']))

            df = pd.DataFrame({
                'Data/Hora': times,
                'Temperatura': temps,
                'Umidade (%)': humidity
            })

            fig = px.line(df, x='Data/Hora', y='Temperatura',
                          title=f'🌡️ Previsão de Temperatura - {cidade.title()}',
                          template='plotly_dark',
                          markers=True)

            fig.update_traces(line=dict(width=2), marker=dict(size=4))

            fig.update_layout(
                title_x=0.5,
                font=dict(size=14),
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)

            # ===== UMIDADE OPCIONAL =====
            with st.expander("💧 Visualizar gráfico de umidade"):
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
