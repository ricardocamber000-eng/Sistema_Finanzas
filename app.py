import streamlit as st
import pandas as pd
from datetime import date
import os
import json
import requests
from streamlit_lottie import st_lottie

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- PERSISTENCIA Y ARCHIVOS ---
DB_FILE = "wallet_database.csv"
CONFIG_FILE = "settings.json"

# Inicializar estado del tema
if "theme" not in st.session_state:
    st.session_state.theme = "Oscuro"

# Cargar configuración de meta
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# Cargar animaciones
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_win = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_TOE99i.json")

# --- DICCIONARIOS Y CONSTANTES ---
ICONOS = {
    "Servicios": "💡", "Mercado": "🛒", "Deudas": "💳", 
    "Ocio": "🎬", "Transporte": "🚗", "Depósito": "💰", "Varios": "📦"
}

# --- LÓGICA DE COLORES ---
if st.session_state.theme == "Claro":
    bg_app, bg_glass, text_main, text_sec, accent = "#F0F2F6", "rgba(255, 255, 255, 0.6)", "#1A1C1E", "#5E6368", "#2D0066"
    border_glass, bar_bg, bar_shadow = "rgba(0,0,0,0.05)", "#FFFFFF", "rgba(0,0,0,0.1)"
else:
    bg_app, bg_glass, text_main, text_sec, accent = "#1A0040", "rgba(255, 255, 255, 0.07)", "#FFFFFF", "#AAAAAA", "#D4FF00"
    border_glass, bar_bg, bar_shadow = "rgba(255,255,255,0.1)", "#FFFFFF", "rgba(0,0,0,0.5)"

# --- INYECCIÓN CSS COMPLETA ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_app} !important; color: {text_main}; }}
    h1, h2, h3, h4, p, span, label {{ color: {text_main} !important; }}
    
    /* Animación de Pulso Neón */
    @keyframes neon-glow {{
        0% {{ box-shadow: 0 0 5px {accent}; border-color: {accent}; }}
        50% {{ box-shadow: 0 0 25px {accent}; border-color: #fff; }}
        100% {{ box-shadow: 0 0 5px {accent}; border-color: {accent}; }}
    }}

    /* Estilo de Tarjetas Glassmorphism */
    .card-resumen, .history-card {{
        background: {bg_glass} !important; 
        backdrop-filter: blur(15px) saturate(160%);
        -webkit-backdrop-filter: blur(15px) saturate(160%);
        border-radius: 25px; padding: 25px;
        border: 1px solid {border_glass}; margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    .history-card {{ border-left: 6px solid {accent} !important; text-align: left; padding: 18px; }}
    .goal-active {{ animation: neon-glow 2s infinite ease-in-out; border: 2px solid {accent} !important; }}

    /* Barra de Navegación Flotante */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background-color: {bar_bg} !important; border-radius: 35px; 
        box-shadow: 0 10px 30px {bar_shadow}; padding: 8px 20px;
        display: flex; justify-content: space-around; border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{ color: #666666 !important; font-size: 0.85em; flex-direction: column; gap: 0px; }}
    .stTabs [aria-selected="true"] {{ color: #C69F40 !important; font-weight: bold; transform: scale(1.1); }}

    /* Botones Neón */
    .stButton > button {{
        border-radius: 40px !important; background-color: {accent} !important; 
        color: #000000 !important; font-weight: 800; border: none !important;
        text-transform: uppercase; letter-spacing: 1px; width: 100%;
    }}
    
    .main .block-container {{ padding-bottom: 160px; }}
</style>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components

def biometric_button():
    # Este JS simula la ceremonia de creación de una Passkey (Huella/FaceID)
    js_code = """
    <script>
    async function registerBiometric() {
        const options = {
            publicKey: {
                challenge: Uint8Array.from("random_challenge", c => c.charCodeAt(0)),
                rp: { name: "R.C Finanzas" },
                user: {
                    id: Uint8Array.from("admin", c => c.charCodeAt(0)),
                    name: "admin@finanzas.pro",
                    displayName: "Admin"
                },
                pubKeyCredParams: [{alg: -7, type: "public-key"}],
                authenticatorSelection: { authenticatorAttachment: "platform" },
                timeout: 60000
            }
        };

        try {
            const credential = await navigator.credentials.create(options);
            window.parent.postMessage({type: 'biometric_success', id: credential.id}, "*");
            alert("¡Huella registrada con éxito!");
        } catch (err) {
            console.error(err);
            alert("Error: El dispositivo no soporta biometría o se canceló.");
        }
    }
    </script>
    <button onclick="registerBiometric()" style="
        background-color: #D4FF00; 
        color: black; 
        border: none; 
        padding: 15px 30px; 
        border-radius: 40px; 
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        text-transform: uppercase;">
        🔗 Vincular Huella Dactilar
    </button>
    """
    components.html(js_code, height=100)
# --- SISTEMA DE SEGURIDAD PREMIUM ---
if "authenticated" not in st.session_state:
    st.markdown(f"""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 4em; margin-bottom:0;">👑</h1>
            <h2 style="letter-spacing: 3px;">R.C FINANZAS <span style="color:{accent};">PRO</span></h2>
            <p style="color:{text_sec};">Terminal de Gestión Patrimonial</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("Login"):
        u = st.text_input("Usuario", placeholder="admin")
        p = st.text_input("Contraseña", type="password", placeholder="••••")
        if st.form_submit_button("DESBLOQUEAR SISTEMA"):
            if u == "admin" and p == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Credenciales Incorrectas")
    st.stop()

# --- CARGA Y PROCESAMIENTO DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
balance = total_in - total_out
goal_reached = balance >= META_AHORRO

# --- NAVEGACIÓN ---
tab_home, tab_config, tab_savings, tab_expenses, tab_income = st.tabs([
    "🏠\nInicio", "⚙️\nConfig", "🐷\nAhorro", "🛍️\nGasto", "💼\nIngreso"
])

with tab_home:
    st.markdown(f"### Hola, Administrador! 👋")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='card-resumen'><small style='color:{text_sec};'>DISPONIBLE</small><h1 style='color:#C69F40; margin: 10px 0;'>${balance:,.2f}</h1></div>", unsafe_allow_html=True)
    with col2:
        pulse = "goal-active" if goal_reached else ""
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen {pulse}'><small style='color:{text_sec};'>META</small><h1 style='color:{accent}; margin: 10px 0;'>{perc}%</h1></div>", unsafe_allow_html=True)

    st.subheader("Últimos Movimientos")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(5).iterrows():
            icono = ICONOS.get(r['Categoría'], "📝") if r['Tipo'] == "Gasto" else "💰"
            color_monto = accent if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>{icono} {r['Detalle']}</b><br><small>{r['Categoría']}</small></div>
                    <div style="color:{color_monto}; font-weight:bold; font-size:1.1em;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_config:
    st.header("Configuración ⚙️")
    theme_choice = st.radio("Tema de la app:", ["Oscuro", "Claro"], horizontal=True, index=0 if st.session_state.theme == "Oscuro" else 1)
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.divider()
    st.subheader("Editar Histórico")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("💾 GUARDAR CAMBIOS"):
        edited_df.to_csv(DB_FILE, index=False)
        st.success("¡Base de datos actualizada!")
        st.rerun()

    with st.expander("🚨 Zona de Peligro"):
        if st.button("REINICIAR TODO EL SISTEMA", type="primary"):
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            st.session_state.clear()
            st.rerun()

with tab_savings:
    st.header("Meta de Ahorro 🐷")
    if goal_reached:
        st.markdown(f"<h2 style='text-align:center; color:{accent};'>¡META LOGRADA! 🏆</h2>", unsafe_allow_html=True)
        if lottie_win: st_lottie(lottie_win, height=200)
        st.balloons()
    
    nueva_meta = st.number_input("Ajustar meta ($)", value=float(META_AHORRO), step=100.0)
    if nueva_meta != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": nueva_meta}, f)
        st.rerun()
    
    progreso = min(max(balance / nueva_meta, 0.0), 1.0) if nueva_meta > 0 else 0
    st.progress(progreso)

with tab_expenses:
    st.header("Nuevo Gasto 🛍️")
    with st.form("f_gasto", clear_on_submit=True):
        c = st.selectbox("Categoría", list(ICONOS.keys()))
        d = st.text_input("Detalle")
        m = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("REGISTRAR GASTO"):
            new_row = pd.DataFrame([[date.today(), "Gasto", c, d, m]], columns=df.columns)
            pd.concat([df, new_row]).to_csv(DB_FILE, index=False)
            st.rerun()

with tab_income:
    st.header("Nuevo Ingreso 💼")
    with st.form("f_ingreso", clear_on_submit=True):
        d = st.text_input("Origen")
        m = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            new_row = pd.DataFrame([[date.today(), "Ingreso", "Depósito", d, m]], columns=df.columns)
            pd.concat([df, new_row]).to_csv(DB_FILE, index=False)
            st.rerun()
