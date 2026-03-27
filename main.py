import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA (MOBILE & WEB)
st.set_page_config(
    page_title="The Father Bets (TFB)",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. SISTEMA DE PERSISTÊNCIA (MEMÓRIA DO APP)
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# 3. ESTILIZAÇÃO CUSTOMIZADA (DARK & GOLD PREMIUM)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0b0d10; }
    .main { background-color: #0b0d10; color: #e0e0e0; }
    
    /* Cards de Jogos */
    .card {
        background: linear-gradient(145deg, #161a1f, #1e2329);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #2a2e35;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Botões */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #d4af37;
        background-color: transparent;
        color: #d4af37;
        font-weight: bold;
        transition: 0.4s;
    }
    .stButton > button:hover {
        background-color: #d4af37;
        color: black;
    }
    
    /* Badges de Confiança */
    .badge-high { background-color: #00ff41; color: black; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-med { background-color: #d4af37; color: black; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    
    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. MOTOR DE DADOS (ALGORITMO TFB 30/20/20/15/15)
@st.cache_data
def get_analysis_data():
    # Simulando dados baseados em ligas reais (Argentina, França L2, Série B)
    raw_data = [
        {"Match": "Banfield vs Gimnasia", "League": "Arg. LPF", "H_U25": 82, "A_U25": 78, "AvgG": 1.9, "H2H": 85, "LAvg": 2.1},
        {"Match": "Ajaccio vs Grenoble", "League": "FRA Ligue 2", "H_U25": 75, "A_U25": 80, "AvgG": 2.0, "H2H": 70, "LAvg": 2.2},
        {"Match": "Operário vs Brusque", "League": "BRA Série B", "H_U25": 85, "A_U25": 72, "AvgG": 1.7, "H2H": 60, "LAvg": 2.0},
        {"Match": "Getafe vs Mallorca", "League": "ESP La Liga", "H_U25": 70, "A_U25": 68, "AvgG": 2.2, "H2H": 75, "LAvg": 2.4},
        {"Match": "Lorient vs Pau FC", "League": "FRA Ligue 2", "H_U25": 65, "A_U25": 62, "AvgG": 2.5, "H2H": 80, "LAvg": 2.2},
        {"Match": "Man. City vs Arsenal", "League": "ENG Premier", "H_U25": 40, "A_U25": 35, "AvgG": 3.2, "H2H": 45, "LAvg": 3.1},
    ]
    
    processed = []
    for item in raw_data:
        # Cálculo Inverso de Gols (Menos gols = Mais pontos)
        score_avg_g = max(0, 100 - (item['AvgG'] * 25))
        score_l_avg = max(0, 100 - (item['LAvg'] * 25))
        
        # Algoritmo Final
        prob = (item['H_U25'] * 0.30) + (item['A_U25'] * 0.20) + (score_avg_g * 0.20) + (item['H2H'] * 0.15) + (score_l_avg * 0.15)
        
        item['Prob'] = round(prob, 1)
        item['Trend'] = "Rising ↑" if prob > 70 else "Stable →"
        processed.append(item)
        
    return pd.DataFrame(processed).sort_values(by="Prob", ascending=False)

df = get_analysis_data()

# 5. INTERFACE DO APP
st.markdown("<h1 style='text-align: center; color: #d4af37;'>🏆 THE FATHER BETS</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 DASHBOARD", "⭐ SAVED"])

with tab1:
    # Filtro de Confiança
    min_conf = st.select_slider("Filtro de Confiança %", options=[50, 60, 65, 70, 75, 80, 85, 90], value=65)
    filtered = df[df['Prob'] >= min_conf]

    if filtered.empty:
        st.warning("Nenhum jogo encontrado com esta confiança. Tente baixar o filtro.")
    
    for idx, row in filtered.iterrows():
        is_high = row['Prob'] >= 75
        badge_class = "badge-high" if is_high else "badge-med"
        status = "HIGH" if is_high else "MEDIUM"
        
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #888; font-size: 11px;">{row['League']}</span>
                    <span class="{badge_class}">{status}</span>
                </div>
                <h3 style="margin: 8px 0; font-size: 20px;">{row['Match']}</h3>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #d4af37; font-size: 28px; font-weight: bold;">{row['Prob']}%</span>
                    <span style="color: #00ff41; font-size: 13px;">Trend: {row['Trend']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Análise Detalhada (Breakdown)
            with st.expander("🔍 Detalhes da Análise"):
                col_chart, col_stats = st.columns([2, 1])
                with col_chart:
                    # Gráfico de Barras do Breakdown
                    breakdown_data = pd.DataFrame({
                        'Fator': ['Home', 'Away', 'Avg Gols', 'H2H', 'League'],
                        'Score': [row['H_U25'], row['A_U25'], 80, row['H2H'], 75]
                    })
                    fig = px.bar(breakdown_data, x='Score', y='Fator', orientation='h', 
                                 color='Score', color_continuous_scale='Greens', template='plotly_dark')
                    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=180)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                with col_stats:
                    st.metric("Avg Gols", row['AvgG'])
                    if row['Match'] not in st.session_state.favorites:
                        if st.button("⭐ Salvar", key=f"fav_{idx}"):
                            st.session_state.favorites.append(row['Match'])
                            st.rerun()
                    else:
                        st.info("Salvo ✅")

with tab2:
    st.subheader("⭐ Seus Jogos Salvos")
    if not st.session_state.favorites:
        st.info("Nenhum jogo salvo ainda. Explore o Dashboard!")
    else:
        # Preparação da mensagem WhatsApp
        wa_text = "*TFB - Relatório de Under 2.5*\n\n"
        for i, fav in enumerate(st.session_state.favorites, 1):
            st.write(f"📌 **{fav}**")
            wa_text += f"✅ *{fav}*\n"
        
        wa_text += "\n_Análise via Algoritmo The Father Bets_"
        wa_link = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
        
        st.markdown(f"""
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; margin-top: 20px;">
                    📲 Compartilhar no WhatsApp
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Limpar Favoritos"):
            st.session_state.favorites = []
            st.rerun()

# 6. RODAPÉ FIXO
st.markdown("---")
st.caption("⚠️ Disclaimer: Análise estatística apenas. Aposte com responsabilidade. TFB v1.5")
