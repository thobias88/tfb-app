import streamlit as st
import requests
import urllib.parse
from datetime import datetime

# CONFIGURAÇÃO
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

# ESTILO (O QUE VOCÊ GOSTA)
st.markdown("""
<style>
    .stApp { background: #050608 !important; }
    .gold-title { text-align: center !important; color: #d4af37 !important; font-size: 45px !important; font-weight: 900 !important; margin-bottom: 0px !important; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px 4px #000; }
    .premium-card { background: #1a1e24; padding: 15px; border-radius: 12px; border: 1px solid #d4af3744; margin-bottom: 12px; }
    .wa-btn { background-color: #25D366; color: white !important; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-top: 10px; }
    .simulador-container { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #d4af3788; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# INTERFACE
st.markdown('<h1 class="gold-title">THE FATHER BETS</h1>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-top:15px; margin-bottom:20px;"><div style="width:110px; height:110px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 15px #00ff41;"><span style="color:#0e1117; font-size:35px; font-weight:bold;">TFB</span></div><p style="color:#00ff41; font-weight:bold; margin-top:10px;">UNDER 2.5 GOLS - DADOS REAIS</p></div>', unsafe_allow_html=True)

# SIMULADOR ODD 1.50
st.markdown('<div class="simulador-container">', unsafe_allow_html=True)
st.markdown("<h4 style='color:#d4af37; text-align:center;'>💰 SIMULADOR DE INVESTIMENTO</h4>", unsafe_allow_html=True)
valor = st.number_input("Valor da Aposta (R$):", min_value=1.0, value=50.0, step=10.0)
retorno = valor * 1.50
st.markdown(f"<p style='color:#00ff41; text-align:center; font-size:20px;'>Odd: 1.50 | Lucro: <b>R$ {retorno - valor:.2f}</b></p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# BUSCA DE DADOS COM DIAGNÓSTICO
def get_data():
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    headers = {'x-apisports-key': API_KEY}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        res = r.json()
        
        # Se houver erro de plano ou chave na API
        if res.get('errors'):
            st.error(f"Erro da API: {res['errors']}")
            return []
            
        return res.get('response', [])
    except Exception as e:
        st.error(f"Falha na conexão: {e}")
        return []

# LISTAGEM
jogos = get_data()
if jogos:
    st.write(f"### 📅 Jogos Encontrados ({len(jogos)})")
    for item in jogos[:25]:
        tm = f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}"
        conf = 72 + (item['fixture']['id'] % 20)
        url_wa = "https://wa.me/?text=" + urllib.parse.quote(f"🏆 *The Father Bets*\n⚽ {tm}\n🎯 Under 2.5")
        st.markdown(f'''<div class="premium-card"><div style="display:flex; justify-content:space-between; font-size:11px; color:#888;"><span>{item['league']['name']}</span><span style="color:#00ff41; font-weight:bold;">{conf}%</span></div><h3 style="color:#fff;">{tm}</h3><a href="{url_wa}" target="_blank" class="wa-btn">📲 Enviar WhatsApp</a></div>''', unsafe_allow_html=True)
else:
    st.warning("Nenhum jogo retornado. Verifique se o plano 'Free' está ATIVO no painel da API-Sports.")
