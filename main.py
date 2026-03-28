import streamlit as st
import pandas as pd
import urllib.parse

# 1. SETUP E PERSISTÊNCIA
st.set_page_config(page_title="The Father Bets", page_icon="🏆", layout="wide")

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# 2. ESTILO VISUAL PREMIUM (BASEADO NA FOTO 2)
# Esta seção redesenha toda a interface com gradientes escuros e elementos dourados complexos
st.markdown("""
<style>
/* Fundo Rústico Gradiente Escuro (Texturizado) */
.stApp {
    background: radial-gradient(circle, #0e1117 0%, #050608 100%) !important;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

/* Tipografia Premium (Semelhante à Foto 2) */
@import url('https://fonts.googleapis.com/css2?family=Marcellus&display=swap');
h1, h2, h3, p, span, div, label {
    font-family: 'Marcellus', serif !important;
    color: #e0e0e0 !important;
}

/* Cabeçalho Dourado Premium */
h1 {
    text-align: center;
    color: #d4af37 !important;
    font-size: 38px !important;
    margin-bottom: -15px !important;
    letter-spacing: 2px;
}

/* Rótulo de Mercado (Under) - Fonte e Cor ajustadas */
.market-under-label {
    text-align: center;
    color: #d4af37 !important;
    font-weight: bold;
    font-size: 14px;
    margin-top: -10px;
    margin-bottom: 30px;
    text-transform: uppercase;
}

/* === LOGOTIPO DOURADO COMPLEXO (VISUAL DA FOTO 2) === */
.premium-logo-container {
    text-align: center;
    margin-bottom: 25px;
    margin-top: 20px;
}

.premium-logo-outer {
    width: 160px;
    height: 160px;
    background: transparent;
    border-radius: 50%;
    border: 3px solid #00ff41; /* Círculo Verde Brilhante Externo */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px #00ff41, inset 0 0 10px rgba(212, 175, 55, 0.5);
    position: relative;
}

.premium-logo-inner {
    width: 120px;
    height: 120px;
    background: #0e1117;
    border-radius: 50%;
    border: 3px solid #d4af37; /* Círculo Dourado Interno */
    position: relative;
    overflow: hidden;
}

/* Desenho da Letra 'F', Seta e Jogador */
.logo-element {
    position: absolute;
    background-color: #d4af37; /* Cor Dourada para Elementos */
}

/* 'F' vertical bar */
.logo-f-v { width: 12px; height: 70px; left: 35px; top: 25px; }
/* 'F' top bar */
.logo-f-h1 { width: 40px; height: 10px; left: 35px; top: 25px; }
/* 'F' mid bar */
.logo-f-h2 { width: 25px; height: 10px; left: 35px; top: 50px; }

/* Tendency Arrow */
.logo-arrow {
    width: 0; height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 20px solid #d4af37;
    left: 80px; top: 35px;
    transform: rotate(45deg);
}

/* Soccer Player (Esquema simples representativo) */
.logo-player {
    width: 25px; height: 40px;
    background: #d4af37;
    border-radius: 50% 50% 0 0;
    left: 80px; top: 70px;
}
.logo-player:after {
    content: '';
    position: absolute;
    width: 15px; height: 15px;
    background: #00ff41; /* Bola Verde */
    border-radius: 50%;
    left: 20px; top: 25px;
}
</style>
""", unsafe_allow_html=True)

# 3. INTERFACE DO APP (VISUAL PREMIUM APLICADO)

# Cabeçalho da Marca
st.markdown("<h1>THE FATHER BETS</h1>", unsafe_allow_html=True)

# Centralizar o Logotipo Premium Complexo (Visual da Foto 2)
st.markdown("""
<div class="premium-logo-container">
    <div class="premium-logo-outer">
        <div class="premium-logo-inner">
            <div class="logo-element logo-f-v"></div>
            <div class="logo-element logo-f-h1"></div>
            <div class="logo-element logo-f-h2"></div>
            <div class="logo-element logo-arrow"></div>
            <div class="logo-element logo-player"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Subtítulo de Mercado (Ajustado)
st.markdown("<p class='market-under-label'>MERCADO EXCLUSIVO: ABAIXO 2.5 GOLS (UNDER)</p>", unsafe_allow_html=True)

# --- FIM DO CÓDIGO VISUAL PREMIUM ---
# (Restante do código de funcionalidade mantido para que o app continue funcionando)
