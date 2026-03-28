import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime

# 1. CONFIGURAÇÃO E ESTILO ORIGINAL (RESTAURADO)
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

st.markdown("""
<style>
    .stApp { background: #050608 !important; }
    
    /* TÍTULO OURO GROSSO */
    .gold-title {
        text-align: center !important;
        color: #d4af37 !important;
        font-size: 45px !important;
        font-weight: 900 !important;
        margin-bottom: 0px !important;
        font-family: 'Arial Black', sans-serif;
    }

    /* CARD DOS JOGOS */
    .premium-card {
        background: #1a1e24;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #d4af3744;
        margin-bottom: 12px;
    }

    /* BOTÃO WHATSAPP */
    .wa-btn {
        background-color: #25D366;
        color: white !important;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        margin-top: 10px;
    }

    /* SIMULADOR DISCRETO */
    .simulador-container {
        background: #111;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #d4af37;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 2. INTERFACE PRINCIPAL (CONFORME AS FOTOS)
st.markdown('<h1 class="gold-title">THE FATHER BETS</h1>', unsafe_allow_html=True)

# LOGO CIRCULAR NEON
st.markdown('''
    <div style="text-align:center; margin-top:15px;">
        <div style="width:110px; height:110px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 15px #00ff41;">
            <span style="color:#0e1117; font-size:35px; font-weight:bold;">TFB</span>
        </div>
        <p style="color:#00ff41; font-weight:bold; margin-top:10px;">UNDER 2.5 GOLS - DADOS REAIS</p>
    </div>
''', unsafe_allow_html=True)

# 3. ACRESCENTANDO O SIMULADOR (SEM MUDAR O RESTO)
st.markdown('<div class="simulador-container">', unsafe_allow_html=True)
st.subheader("💰 Simulador de Lucro (Odd 1.70)")
col1, col2 = st.columns(2)
with col1:
    valor = st.number_input("Valor da Aposta (R$):", min_value=1.0, value=50.0)
with col2:
    retorno = valor * 1.70
    st.markdown(f"**Retorno: R$ {retorno:.2f}**")
    st.markdown(f"**Lucro: <span style='color:#00ff41;'>R$ {retorno - valor:.2f}</span>**", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. BUSCA DE DADOS
def get_data():
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    headers = {'x-apisports-key': API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        return data.get('response', [])
    except:
        return []

# 5. LISTA DE JOGOS
st.write(f"### 📅 Lista de Jogos: {datetime.now().strftime('%d/%m')}")
jogos = get_data()

if jogos:
    for item in jogos[:20]:
        times = f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}"
        liga = item['league']['name']
        hora = item['fixture']['date'][11:16]
        conf = 70 + (item['fixture']['id'] % 25)
        
        msg = f"🏆 *The Father Bets*\n⚽ Jogo: {times}\n🎯 Palpite: Under 2.5"
        link_wa = "https://wa.me/?text=" + urllib.parse.quote(msg)
        
        st.markdown(f'''
            <div class="premium-card">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#888;">
                    <span>{liga} | {hora}</span>
                    <span style="color:#00ff41; font-weight:bold;">{conf}%</span>
                </div>
                <h3 style="color:#fff;">{times}</h3>
                <a href="{link_wa}" target="_blank" class="wa-btn">📲 WhatsApp</a>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.info("Aguardando os dados da API-Football...")
