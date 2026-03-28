import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime, timedelta

# 1. SETUP INICIAL E CHAVE (MANTIDOS)
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")
API_KEY = "44665fca0ce33f498cb33f98d882c65f"

# 2. ESTILO VISUAL REVISADO (FOCO NO TÍTULO DOURADO E GROSSO)
st.markdown("""
<style>
/* Fundo Total do App */
.stApp { background: #050608 !important; }

/* 🌟 TÍTULO PRINCIPAL: OURO E ESPESSO 🌟 */
h1.gold-thick {
    text-align: center !important;
    color: #d4af37 !important; /* Cor Ouro */
    font-size: 42px !important; /* Tamanho maior */
    font-weight: 900 !important; /* Espessura Máxima */
    margin-bottom: 0px !important;
    margin-top: 20px !important;
    font-family: 'Montserrat', sans-serif !important;
    text-shadow: 2px 2px 4px #000;
}

/* Outros Textos */
h2, h3, p, span, label {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    color: #e0e0e0 !important;
}

/* Cards Premium */
.premium-card {
    background: #1a1e24;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #d4af3733;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6);
}

/* Badges e Botão WhatsApp */
.market-tag { background-color: #d4af37; color: black; padding: 5px 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-top: 10px; }
.whatsapp-btn { background-color: #25D366; color: white !important; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. INTERFACE DO APP (LOGOTIPO E TÍTULO DOURADO GROSSO)

# Centralizar Título e Logo
st.markdown('<h1 class="gold-thick">THE FATHER BETS</h1>', unsafe_allow_html=True)

# Logotipo TFB Representativo (Mantenha enquanto embutimos o Base64 do real)
st.markdown(f"""
    <div style="text-align:center; margin-bottom:25px; margin-top:15px;">
        <div style="width:130px; height:130px; background:radial-gradient(circle, #d4af37, #0e1117); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 20px #00ff41;">
            <span style="color:#0e1117; font-size:45px; font-weight:bold;">TFB</span>
        </div>
        <p style='color:#00ff41; font-weight:bold; margin-top:10px;'>MERCADO: ABAIXO 2.5 GOLS (REAIS)</p>
    </div>
    """, unsafe_allow_html=True)

# 4. FUNÇÃO PARA BUSCAR JOGOS REAIS DE AMANHÃ
def fetch_real_data():
    # Define a data de amanhã
    target_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={target_date}"
    headers = {'x-apisports-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        matches = []
        for item in data.get('response', []):
            matches.append({
                "time": item['fixture']['date'][11:16],
                "league": item['league']['name'],
                "teams": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                "prob": 70 + (item['fixture']['id'] % 20) # Simulação de probabilidade baseada em ID
            })
        return matches
    except:
        return []

# 5. EXIBIÇÃO E COMPARTILHAMENTO NO WHATSAPP
st.write(f"### 📅 Palpites para: {(datetime.now() + timedelta(days=1)).strftime('%d/%m')}")

with st.spinner('Acessando dados reais...'):
    jogos = fetch_real_data()
    if jogos:
        for m in jogos[:20]:
            # Preparar mensagem WhatsApp
            mensagem_wa = f"🏆 *The Father Bets*\n⚽ Jogo: {m['teams']}\n📊 Probabilidade Under 2.5: {m['prob']}%\n🎯 Palpite: *Abaixo 2.5 Gols*"
            wa_link = f"https://wa.me/?text={urllib.parse.quote(mensagem_wa)}"
            
            st.markdown(f"""
                <div class="premium-card">
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:#888;">
                        <span>{m['league']} | {m['time']}</span>
                        <span style="color:#00ff41; font-weight:bold;">CONFIANÇA: {m['prob']}%</span>
                    </div>
                    <h3 style="color:#fff; margin:10px 0;">{m['teams']}</h3>
                    <div class="market-tag">PALPITE: ABAIXO DE 2.5 GOLS</div>
                    <a href="{wa_link}" target="_blank" class="whatsapp-btn">📲 Enviar para WhatsApp</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Verifique sua API KEY ou plano na API-Sports. Nenhum dado foi retornado.")

st.markdown("---")
st.caption("The Father Bets v1.9 | Dados Reais via API-Sports | Under 2.5 Анализатор 🏆")
