# 🌤️ Dashboard de Clima em Tempo Real

Este projeto é um **dashboard interativo de clima** desenvolvido com **Python**, utilizando as bibliotecas **Streamlit**, **Plotly** e **Pandas**. Ele permite consultar o clima atual e visualizar previsões para os próximos dias de qualquer cidade do mundo, com gráficos interativos de temperatura e umidade.

## 🧠 Funcionalidades

- 🔍 Busca de cidade e seleção de unidade de temperatura (°C ou °F)
- 🌡️ Exibição de dados em tempo real:
  - Temperatura atual
  - Sensação térmica
  - Umidade do ar
  - Velocidade do vento
  - Descrição do clima
- 📈 Gráfico de barras com previsão de temperatura para os próximos dias
- 💧 Gráfico de umidade opcional com visualização expandida
- 🚫 Mensagem de erro caso a cidade não seja encontrada

## 🖼️ Demonstração

> Interface moderna e responsiva com Streamlit + Plotly.

![preview](https://via.placeholder.com/800x400?text=Preview+do+Dashboard)

## 📦 Bibliotecas Utilizadas

- `streamlit` – Interface web interativa
- `pandas` – Manipulação de dados
- `requests` – Requisições HTTP para APIs
- `plotly.express` – Gráficos interativos
- `datetime` – Conversão e formatação de datas

## 🔗 API Utilizada

Os dados meteorológicos são fornecidos pela [OpenWeatherMap](https://openweathermap.org/api).

Você precisará de uma chave de API para rodar o projeto. Crie uma conta gratuita no site da OpenWeatherMap e obtenha sua chave.
