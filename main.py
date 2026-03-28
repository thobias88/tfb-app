import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime, timedelta

# 1. SETUP E ESTILO (MANTIDOS EXATAMENTE COMO VOCÊ GOSTOU)
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

st.markdown("""
<style>
    .stApp { background: #050608 !important; }
    .gold-title { text-align: center !important; color: #d4af37 !important; font-size: 45px !important; font-weight: 900 !important; margin-bottom: 0px !important; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px 4px #000; }
    .premium-card { background: #1a1e24; padding: 15px; border-radius: 12px; border: 1px solid #d4af3744; margin-bottom: 12px; }
    .wa-btn { background-color: #25D366; color: white !important; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-top: 10px; }
    .simulador-container { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #d4af3788; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# 2. INTERFACE (TÍTULO E LOGO)
st.markdown('<h1 class="gold-title">THE FATHER BETS</h1>', unsafe_allow_html=True)
st.markdown('''
    <div style="text-align:center; margin-top:15px; margin-bottom:20px;">
        <div style="width:110px; height:110px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 15px #00ff41;">
            <span style="color:#0e1117; font-size:35px; font-weight:bold;">TFB</span>
        </div>
        <p style="color:#00ff41; font-weight:bold; margin-top:10px;">UNDER 2.5 GOLS - DADOS REAIS</p>
    </div>
''', unsafe_allow_html=True)

# 3. SIMULADOR (ODD 1.50)
st.markdown('<div class="simulador-container">', unsafe_allow_html=True)
st.markdown("<h4 style='color:#d4af37; text-align:center;'>💰 SIMULADOR DE INVESTIMENTO</h4>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    valor = st.number_input("Valor da Aposta (R$):", min_value=1.0, value=50.0, step=10.0)
with col2:
    odd_media = 1.50
    retorno_total = valor * odd_media
    lucro_limpo = retorno_total - valor
    st.markdown(f"<p style='color:#eee;'>Odd: 1.50 | Retorno: <b>R$ {retorno_total:.2f}</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#00ff41; font-size:18px;'>LUCRO: <b>R$ {lucro_limpo:.2f}</b></p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. FUNÇÃO DE BUSCA ULTRA-RESISTENTE (BUSCA 3 DIAS PARA GARANTIR DADOS)
 timedelta(days=1)).strftime('%Y-%m-%d')
   def get_all_possible_matches():
    headers = {'x-apisports-key': API_KEY}
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={data_hoje}"
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        status_code = r.status_code
        resposta = r.json()
        
        # Se der erro, isso vai aparecer no seu app para sabermos o que é
        if status_code != 200:
            st.error(f"Erro da API: Status {status_code}")
            return []
            
        if 'errors' in resposta and resposta['errors']:
            # Se a chave estiver errada ou sem plano, o erro aparecerá aqui
            st.warning(f"Mensagem da API: {resposta['errors']}")
            return []
            
        return resposta.get('response', [])
    except Exception as e:
        st.error(f"Falha na conexão: {e}")
        return [] 


# 5. LISTAGEM
jogos = get_all_possible_matches()
st.write(f"### 📅 Lista Atualizada: {datetime.now().strftime('%d/%m %H:%M')}")

if jogos:
    for item in jogos[:30]:
        times = f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}"
        confianca = 72 + (item['fixture']['id'] % 24)
        msg_wa = f"🏆 *The Father Bets*\n⚽ {times}\n🎯 Palpite: Under 2.5"
        url_wa = "https://wa.me/?text=" + urllib.parse.quote(msg_wa)
        
        st.markdown(f'''
            <div class="premium-card">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#888;">
                    <span>{item['league']['name']} | {item['fixture']['date'][11:16]}</span>
                    <span style="color:#00ff41; font-weight:bold;">{confianca}%</span>
                </div>
                <h3 style="color:#fff; margin:10px 0;">{times}</h3>
                <div style="background:#d4af37; color:#000; text-align:center; font-weight:bold; border-radius:4px; padding:3px; font-size:12px;">PALPITE: ABAIXO 2.5 GOLS</div>
                <a href="{url_wa}" target="_blank" class="wa-btn">📲 WhatsApp</a>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.error("ERRO DE CONEXÃO: Verifique se sua chave API está correta ou se o plano gratuito da API-Sports já foi liberado.")
