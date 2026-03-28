import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

# 1. SETUP
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# 2. ESTILO DARK FORÇADO (RÚSTICO)
st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"] { background-color: #101216 !important; color: white !important; }
h1, h2, h3, p, span, div, label { color: #e0e0e0 !important; }
.card { background-color: #1a1e24 !important; padding: 20px; border-radius: 15px; border: 1px solid #d4af3733; margin-bottom: 15px; }
.market-label { background-color: #d4af37 !important; color: black !important; padding: 6px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px; }
.stButton > button { width: 100%; border-radius: 10px; border: 1px solid #d4af37 !important; background: transparent !important; color: #d4af37 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. DADOS
data = [
    {"Match": "Banfield vs Gimnasia", "League": "Arg. LPF", "Prob": 88.4, "AvgG": 1.9},
    {"Match": "Ajaccio vs Grenoble", "League": "FRA Ligue 2", "Prob": 82.1, "AvgG": 2.1},
    {"Match": "Operário vs Brusque", "League": "BRA Série B", "Prob": 79.5, "AvgG": 1.8},
    {"Match": "Getafe vs Mallorca", "League": "ESP La Liga", "Prob": 75.2, "AvgG": 2.2}
]
df = pd.DataFrame(data)

# 4. CABEÇALHO COM LOGO
st.markdown("<h1 style='text-align: center; color: #d4af37;'>THE FATHER BETS</h1>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;"><div style="width:120px; height:120px; background:radial-gradient(circle, #d4af37, #101216); border-radius:50%; border:3px solid #00ff41; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 0 15px #00ff41;"><span style="color:#101216; font-size:45px; font-weight:bold;">TFB</span></div></div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ff41; font-weight: bold; margin-top:10px;'>MERCADO EXCLUSIVO: ABAIXO 2.5 GOLS (UNDER)</p>", unsafe_allow_html=True)

# 5. BOTÕES DE INFO
c1, c2 = st.columns(2)
with c1:
    if st.button("📖 Regras"): st.info("Foco em ligas com média < 2.3 gols.")
with c2:
    if st.button("💰 Gestão"): st.success("Use 1% a 3% da banca.")

# 6. DASHBOARD
t1, t2 = st.tabs(["📊 JOGOS", "⭐ SALVOS"])

with t1:
    conf = st.select_slider("Confiança %", options=[50, 60, 65, 70, 75, 80, 85, 90], value=65)
    filt = df[df['Prob'] >= conf]
    for i, r in filt.iterrows():
        st.markdown(f'<div class="card"><div style="display:flex; justify-content:space-between; font-size:11px; color:#888;"><span>{r["League"]}</span><span style="color:#00ff41;">{r["Prob"]}%</span></div><h3 style="margin:10px 0;">{r["Match"]}</h3><div class="market-label">PALPITE: ABAIXO 2.5 GOLS</div></div>', unsafe_allow_html=True)
        with st.expander("🔍 Detalhes"):
            st.write(f"Média de Gols: {r['AvgG']}")
            if st.button(f"Salvar {r['Match']}", key=f"s_{i}"):
                if r['Match'] not in st.session_state.favorites:
                    st.session_state.favorites.append(r['Match'])
                    st.rerun()

with t2:
    if not st.session_state.favorites:
        st.info("Lista vazia.")
    else:
        for f in st.session_state.favorites: st.warning(f"📌 {f} - Abaixo 2.5")
        txt = urllib.parse.quote("🏆 *TFB Palpites:*\n" + "\n".join(st.session_state.favorites))
        st.markdown(f'<a href="https://wa.me/?text={txt}" target="_blank"><div style="background:#25D366; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold;">WhatsApp</div></a>', unsafe_allow_html=True)
        if st.button("Limpar"):
            st.session_state.favorites = []
            st.rerun()
