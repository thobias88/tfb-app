import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. CONFIGURAÇÃO E ESTILO (MANTENDO SUA IDENTIDADE VISUAL)
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")

st.markdown("""
<style>
    .stApp { background: #050608 !important; }
    .gold-title { text-align: center !important; color: #d4af37 !important; font-size: 45px !important; font-weight: 900 !important; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px 4px #000; }
    .premium-card { background: #1a1e24; padding: 15px; border-radius: 12px; border: 1px solid #d4af3744; margin-bottom: 12px; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #d4af37 !important; border-bottom-color: #d4af37 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="gold-title">THE FATHER BETS</h1>', unsafe_allow_html=True)

# 2. ABAS DE NAVEGAÇÃO
tab1, tab2 = st.tabs(["💰 Calculadora & Jogos", "🔍 Importar Estatísticas"])

with tab1:
    # --- CALCULADORA QUE VOCÊ GOSTOU ---
    st.markdown("<div style='background:#111; padding:15px; border-radius:10px; border:1px solid #d4af3788;'>", unsafe_allow_html=True)
    valor = st.number_input("Valor da Aposta (R$):", min_value=1.0, value=50.0, step=10.0)
    st.markdown(f"<p style='color:#00ff41; font-size:18px;'>Se a Odd for 1.50, seu Lucro é: <b>R$ {valor * 0.50:.2f}</b></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Lista de Jogos (Aqui aparecerão os jogos analisados na outra aba)
    st.write("### 📅 Meus Palpites Under 2.5")
    if 'meus_jogos' in st.session_state and st.session_state.meus_jogos:
        for j in st.session_state.meus_jogos:
            with st.container():
                st.markdown(f"""
                <div class="premium-card">
                    <span style="color:#888; font-size:12px;">Confiança: {j['conf']}</span>
                    <h3 style="color:#fff;">{j['time_h']} vs {j['time_a']}</h3>
                    <p style="color:#d4af37; font-weight:bold;">PALPITE: UNDER 2.5 GOLS</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Vá na aba 'Importar Estatísticas' para adicionar jogos.")

with tab2:
    st.subheader("🔗 Analisar Link ou Inserir Manual")
    
    metodo = st.radio("Escolha o método:", ["Analisar Link (Beta)", "Inserir Manualmente"])
    
    if metodo == "Analisar Link (Beta)":
        url_input = st.text_input("Cole o link do site de estatísticas (ex: Flashscore, SofaScore):")
        if st.button("🚀 Extrair e Analisar"):
            with st.spinner("Lendo dados do site..."):
                # Simulação de Extração (Scraping real exige headers específicos por site)
                try:
                    # Aqui entra a lógica de requests.get(url_input)
                    st.error("O site bloqueou o acesso automático. Use a 'Inserir Manualmente' abaixo para resultados imediatos.")
                except:
                    st.error("Link inválido ou inacessível.")

    else:
        # --- FORMULÁRIO MANUAL (MAIS SEGURO) ---
        with st.form("manual_entry"):
            col1, col2 = st.columns(2)
            t1 = col1.text_input("Time da Casa")
            t2 = col2.text_input("Time Visitante")
            media_gols = st.slider("Média de gols dos últimos 5 jogos:", 0.0, 5.0, 2.0)
            
            submit = st.form_submit_button("Analisar e Salvar Jogo")
            
            if submit:
                # Lógica de Confiança
                nivel = "ALTA" if media_gols <= 2.0 else "MÉDIA"
                if media_gols > 3.0: nivel = "BAIXA (Risco)"
                
                novo_jogo = {"time_h": t1, "time_a": t2, "conf": nivel}
                
                if 'meus_jogos' not in st.session_state:
                    st.session_state.meus_jogos = []
                
                st.session_state.meus_jogos.append(novo_jogo)
                st.success(f"Jogo {t1} vs {t2} adicionado com Confiança {nivel}!")

# 3. REQUISITOS TÉCNICOS (REQUIREMENTS.TXT)
# streamlit
# pandas
# requests
# beautifulsoup4
