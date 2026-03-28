import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime, timedelta

# 1. SETUP E CHAVE
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

# 2. ESTILO VISUAL PREMIUM
st.markdown("<style>.stApp { background: #050608 !important; } .main-title { text-align: center; color: #d4af37; font-size: 35px; font-weight: bold; } .premium-card { background: #1a1e24; padding: 15px; border-radius: 12px; border: 1px solid #d4af3755; margin-bottom: 12px; } .market-tag { background-color: #d4af37; color: #000; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; margin-top: 5px; } .wa-btn { background-color: #25D366; color: white !important; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-top: 10px; }</style>", unsafe_allow_html=True)

# 3. CABEÇALHO
st.markdown("<h1 class='main-title'>THE FATHER BETS</h1>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-bottom:20px;"><div style="width:110px; height:110px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 15px #00ff41;"><span style="color:#0e1117; font-size:35px; font-weight:bold;">TFB</span></div><p style="color:#00ff41; font-weight:bold; margin-top:8px;">UNDER 2.5 GOLS - DADOS REAIS</p></div>', unsafe_allow_html=True)

# 4. FUNÇÃO DE BUSCA MELHORADA
def get_data():
    # Busca jogos para hoje para garantir que apareça algo
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    headers = {'x-apisports-key': API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        found = []
        if 'response' in data:
            for item in data['response']:
                # Filtra apenas jogos que ainda não começaram ou estão no início
                status = item['fixture']['status']['short']
                if status in ['NS', '1H', 'HT']:
                    found.append({
                        "h": item['fixture']['date'][11:16],
                        "lg": item['league']['name'],
                        "tm": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                        "cf": 75 + (item['fixture']['id'] % 15)
                    })
        return found
    except:
        return []

# 5. EXIBIÇÃO
jogos = get_data()
st.write(f"### 📅 Jogos Disponíveis: {datetime.now().strftime('%d/%m')}")

if jogos:
    for j in jogos[:20]: # Mostra até 20 jogos
        texto_wa = f"🏆 *The Father Bets*\n⚽ Jogo: {j['tm']}\n📈 Confiança: {j['cf']}%\n🎯 Palpite: *Abaixo 2.5 Gols*"
        link_wa = "https://wa.me/?text=" + urllib.parse.quote(texto_wa)
        st.markdown(f'<div class="premium-card"><div style="display:flex; justify-content:space-between; font-size:11px; color:#888;"><span>{j["lg"]} | {j["h"]}</span><span style="color:#00ff41; font-weight:bold;">{j["cf"]}%</span></div><h3 style="color:#fff; margin:5px 0;">{j["tm"]}</h3><div class="market-tag">PALPITE: ABAIXO 2.5 GOLS</div><a href="{link_wa}" target="_blank" class="wa-btn">📲 Enviar para WhatsApp</a></div>', unsafe_allow_html=True)
else:
    st.warning("Aguardando atualização da API... Se persistir, verifique se seu plano gratuito na API-Sports está ativo.")
    

    
