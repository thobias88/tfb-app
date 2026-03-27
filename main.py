import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# 2. ESTILO DARK/GOLD
st.markdown("""
    <style>
    .main { background-color: #0b0d10; color: #e0e0e0; }
    .card {
        background: linear-gradient(145deg, #161a1f, #1e2329);
        padding: 20px; border-radius: 15px; border: 1px solid #2a2e35; margin-bottom: 15px;
    }
    .market-label {
        background-color: #d4af37; color: black; padding: 5px; 
        border-radius: 5px; text-align: center; font-weight: bold; font-size: 12px; margin-bottom: 10px;
    }
    .stButton > button { width: 100%; border-radius: 10px; border: 1px solid #d4af37; background: transparent; color: #d4af37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. DADOS REALISTAS
@st.cache_data
def get_data():
    data = [
        {"Match": "Banfield vs Gimnasia", "League": "Arg. LPF", "Prob": 88.4, "AvgG": 1.9, "H_U25": 82, "A_U25": 78, "H2H": 85},
        {"Match": "Ajaccio vs Grenoble", "League": "FRA Ligue 2", "Prob": 82.1, "AvgG": 2.1, "H_U25": 75, "A_U25": 80, "H2H": 70},
        {"Match": "Operário vs Brusque", "League": "BRA Série B", "Prob": 79.5, "AvgG": 1.8, "H_U25": 85, "A_U25": 72, "H2H": 60},
        {"Match": "Getafe vs Mallorca", "League": "ESP La Liga", "Prob": 75.2, "AvgG": 2.2, "H_U25": 70, "A_U25": 68, "H2H": 75},
    ]
    return pd.DataFrame(data)

df = get_data()

# 4. CABEÇALHO E INFOS EXTRAS
st.markdown("<h1 style='text-align: center; color: #d4af37;'>🏆 THE FATHER BETS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ff41; font-weight: bold; margin-bottom: 0;'>MERCADO: ABAIXO 2.5 GOLS (UNDER)</p>", unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📖 Regras do Método"):
        st.info("Focamos em ligas com média inferior a 2.3 gols e times com forte retranca.")
with col_btn2:
    if st.button("💰 Gestão de Banca"):
        st.success("Recomendamos utilizar 1% a 3% da sua banca por entrada.")

tab1, tab2 = st.tabs(["📊 DASHBOARD", "⭐ SALVOS"])

with tab1:
    min_conf = st.select_slider("Filtro de Confiança %", options=[50, 60, 65, 70, 75, 80, 85, 90], value=65)
    filtered = df[df['Prob'] >= min_conf]
    
    for idx, row in filtered.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #888;">
                    <span>{row['League']}</span>
                    <span style="color:#00ff41;">CONFIRMAÇÃO: {row['Prob']}%</span>
                </div>
                <h3 style="margin: 10px 0;">{row['Match']}</h3>
                <div class="market-label">PALPITE: ABAIXO DE 2.5 GOLS</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔍 Análise Técnica"):
                st.write(f"Média de Gols: **{row['AvgG']}**")
                if st.button(f"⭐ Salvar {row['Match']}", key=f"btn_{idx}"):
                    if row['Match'] not in st.session_state.favorites:
                        st.session_state.favorites.append(row['Match'])
                        st.rerun()

with tab2:
    if not st.session_state.favorites:
        st.info("Nenhum palpite salvo.")
    else:
        for fav in st.session_state.favorites:
            st.warning(f"📌 {fav} - Abaixo 2.5")
        
        wa_text = "🏆 *TFB - Meus Palpites Abaixo 2.5:*\n\n" + "\n".join([f"✅ {f}" for f in st.session_state.favorites])
        wa_link = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
        st.markdown(f'<a href="{wa_link}" target="_blank"><div style="background:#25D366; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold;">Enviar para WhatsApp</div></a>', unsafe_allow_html=True)
        if st.button("Limpar"):
            st.session_state.favorites = []
            st.rerun()

st.markdown("---")
st.caption("The Father Bets v1.6 | Analisador de Under 2.5")
