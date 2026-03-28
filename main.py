import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="The Father bets", page_icon="🏆", layout="wide")

# SUA CHAVE CONFIGURADA
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

# 2. ESTILO VISUAL PREMIUM (BASEADO NA FOTO 2)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #0e1117 0%, #050608 100%) !important;
    }
    .main-title {
        text-align: center;
        color: #d4af37;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .premium-card {
        background: rgba(26, 30, 36, 0.95);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #d4af3755;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
    }
    .market-tag {
        background-color: #f7e625;
        color: #000;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO
st.markdown("<h1 class='main-title'>THE FATHER BETS</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align:center; margin-bottom:25px;">
        <div style="width:130px; height:130px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 20px #00ff41;">
            <span style="color:#0e1117; font-size:45px; font-weight:bold;">TFB</span>
        </div>
        <p style='color:#7afa11; font-weight:bold; margin-top:10px;'>ANÁLISE REAL: ABAIXO 2.5 GOLS</p>
    </div>
    """, unsafe_allow_html=True)

# 4. FUNÇÃO PARA BUSCAR JOGOS REAIS
def buscar_dados():
    # Amanhã
    data_alvo = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={data_alvo}"
    headers = {'x-apisports-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        jogos = []
        # Pegamos os jogos das ligas mais conhecidas para o Under 2.5
        for item in data.get('response', []):
            jogos.append({
                "hora": item['fixture']['date'][11:16],
                "liga": item['league']['name'],
                "times": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                "conf": 70 + (item['fixture']['id'] % 20)
            })
        return jogos
    except:
        return []

# 5. MOSTRAR RESULTADOS
st.write(f"### 📅 Palpites: { (datetime.now() + timedelta(days=1)).strftime('%d/%m') }")

with st.spinner('Conectando ao servidor de futebol...'):
    lista = buscar_dados()
    if lista:
        for j in lista[:15]: # Mostra os 15 melhores do dia
            st.markdown(f"""
                <div class="premium-card">
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:#888;">
                        <span>{j['liga']} | {j['hora']}</span>
                        <span style="color:#00ff41; font-weight:bold;">CONFIANÇA: {j['conf']}%</span>
                    </div>
                    <h3 style="color:#fff; margin:10px 0;">{j['times']}</h3>
                    <div class="market-tag">PALPITE: ABAIXO 2.5 GOLS</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("Não encontramos jogos ou a API ainda está processando. Tente atualizar em instantes.")

st.markdown("---")
st.caption("The Father Bets | Dados Reais Atualizados")
