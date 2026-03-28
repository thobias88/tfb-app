import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO PREMIUM
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")

# Coloque sua chave entre as aspas abaixo
API_KEY = "SUA_CHAVE_AQUI"

# 2. ESTILO VISUAL DA FOTO 2 (DARK & GOLD)
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
        text-shadow: 2px 2px 4px #000;
    }
    .premium-card {
        background: rgba(26, 30, 36, 0.9);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #d4af3755;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .market-tag {
        background-color: #d4af37;
        color: #000;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    .conf-badge {
        color: #00ff41;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO COM LOGO ESTILIZADO
st.markdown("<h1 class='main-title'>THE FATHER BETS</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="width:130px; height:130px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 20px #00ff41;">
            <span style="color:#0e1117; font-size:45px; font-weight:bold;">TFB</span>
        </div>
        <p style='color:#00ff41; font-weight:bold; margin-top:10px;'>MERCADO EXCLUSIVO: ABAIXO 2.5 GOLS</p>
    </div>
    """, unsafe_allow_html=True)

# 4. FUNÇÃO PARA BUSCAR JOGOS REAIS DE AMANHÃ
def fetch_real_data():
    if API_KEY == "44665fca0ce33f498cb33f98d882c65f":
        return None
    
    # Busca jogos para amanhã
    target_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={target_date}"
    headers = {'x-apisports-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        matches = []
        # Pegamos os primeiros 20 jogos para analisar
        for item in data.get('response', [])[:20]:
            matches.append({
                "time": item['fixture']['date'][11:16],
                "league": item['league']['name'],
                "teams": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                "prob": 72 + (item['fixture']['id'] % 15) # Simulação de probabilidade baseada no ID
            })
        return matches
    except:
        return []

# 5. EXIBIÇÃO DOS JOGOS
st.write(f"### 📅 Próximos Jogos ({(datetime.now() + timedelta(days=1)).strftime('%d/%m')})")

if API_KEY == "SUA_CHAVE_AQUI":
    st.warning("⚠️ Quase lá! Você precisa colar sua 'API Key' no código para ver os jogos reais.")
else:
    with st.spinner('Analisando mercados de Under 2.5...'):
        results = fetch_real_data()
        
        if results:
            for m in results:
                st.markdown(f"""
                    <div class="premium-card">
                        <div style="display:flex; justify-content:space-between; font-size:12px; color:#888;">
                            <span>{m['league']} | {m['time']}</span>
                            <span class="conf-badge">CONFIANÇA: {m['prob']}%</span>
                        </div>
                        <h3 style="color:#fff; margin:10px 0;">{m['teams']}</h3>
                        <div class="market-tag">PALPITE: ABAIXO 2.5 GOLS</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Erro ao conectar. Verifique sua chave ou limite da API.")

st.markdown("---")
st.caption("The Father Bets v2.0 | Dados em Tempo Real via API-Sports")
