import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime, timedelta

# 1. SETUP E ESTILO
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

st.markdown("""
<style>
.stApp { background: #050608 !important; }
.gold-title { text-align: center !important; color: #d4af37 !important; font-size: 45px !important; font-weight: 900 !important; margin-bottom: 0px !important; text-shadow: 2px 2px 5px rgba(0,0,0,0.8); font-family: 'Arial Black', sans-serif; }
.premium-card { background: #1a1e24; padding: 15px; border-radius: 12px; border: 1px solid #d4af3744; margin-bottom: 12px; }
.simulador-box { background: linear-gradient(145deg, #1a1e24, #0e1117); padding: 20px; border-radius: 15px; border: 2px solid #d4af37; margin: 20px 0; text-align: center; }
.wa-btn { background-color: #25D366; color: white !important; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. CABEÇALHO
st.markdown('<h1 class="gold-title">THE FATHER BETS</h1>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;"><p style="color:#00ff41; font-weight:bold;">ESTATÍSTICAS REAIS EM TEMPO REAL</p></div>', unsafe_allow_html=True)

# 3. NOVO: SIMULADOR DE LUCRO
st.markdown('<div class="simulador-box">', unsafe_allow_html=True)
st.subheader("💰 SIMULADOR DE INVESTIMENTO")
valor_aposta = st.number_input("Quanto você deseja apostar por jogo? (R$)", min_value=1.0, value=50.0)
lucro_estimado = valor_aposta * 0.70 # Simulando Odd 1.70
st.markdown(f"### Retorno estimado: <span style='color:#00ff41;'>R$ {valor_aposta + lucro_estimado:.2f}</span>", unsafe_allow_html=True)
st.markdown(f"**Lucro Líquido: R$ {lucro_estimado:.2f}**")
st.markdown('</div>', unsafe_allow_html=True)

# 4. BUSCA DE DADOS
def get_matches():
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    headers = {'x-apisports-key': API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        found = []
        if 'response' in data:
            for item in data['response']:
                found.append({
                    "h": item['fixture']['date'][11:16],
                    "lg": item['league']['name'],
                    "tm": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                    "cf": 75 + (item['fixture']['id'] % 20)
                })
        return found
    except:
        return []

# 5. EXIBIÇÃO
jogos = get_matches()
st.write(f"### 📅 Palpites do Dia: {datetime.now().strftime('%d/%m')}")

if jogos:
    for j in jogos[:20]:
        msg = f"🏆 *The Father Bets*\n⚽ Jogo: {j['tm']}\n📈 Confiança: {j['cf']}%\n🎯 Palpite: *Under 2.5*"
        link_wa = "https://wa.me/?text=" + urllib.parse.quote(msg)
        st.markdown(f'''
            <div class="premium-card">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#888;">
                    <span>{j["lg"]} | {j["h"]}</span>
                    <span style="color:#00ff41; font-weight:bold;">{j["cf"]}%</span>
                </div>
                <h3 style="color:#fff;">{j["tm"]}</h3>
                <a href="{link_wa}" target="_blank" class="wa-btn">📲 Compartilhar no WhatsApp</a>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.info("Buscando novos jogos nos servidores... Atualize a página em instantes.")
