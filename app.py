import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- PERSISTENCIA Y CONFIGURACIÓN ---
DB_FILE = "wallet_database.csv"
CONFIG_FILE = "settings.json"

# Inicializar estado del tema si no existe
if "theme" not in st.session_state:
    st.session_state.theme = "Oscuro"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- DICCIONARIOS ---
ICONOS = {
    "Servicios": "💡", "Mercado": "🛒", "Deudas": "💳", 
    "Ocio": "🎬", "Transporte": "🚗", "Depósito": "💰", "Varios": "📦"
}

# --- SISTEMA DE SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.markdown("<h2 style='text-align:center;'>👑 R.C Finanzas</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Ingresar"):
            if user == "admin" and password == "1234":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Error de acceso")
    st.stop()

# --- CARGA DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# --- CÁLCULOS GLOBALES ---
total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
balance = total_in - total_out

# --- LÓGICA DE TEMAS Y GLASSMORPHISM (PÚRPURA & NEÓN) ---
if st.session_state.theme == "Claro":
    bg_app = "#F0F2F6"
    bg_glass = "rgba(255, 255, 255, 0.6)"
    text_main = "#1A1C1E"
    text_sec = "#5E6368"
    accent_color = "#2D0066" # Púrpura para acentos en modo claro
    border_glass = "rgba(0,0,0,0.05)"
    bar_bg = "#FFFFFF"
    bar_shadow = "rgba(0,0,0,0.1)"
else:
    bg_app = "#1A0040"                    # Púrpura muy profundo (Estilo Planable)
    bg_glass = "rgba(255, 255, 255, 0.07)" # Vidrio translúcido
    text_main = "#FFFFFF"
    text_sec = "#AAAAAA"
    accent_color = "#D4FF00"              # VERDE NEÓN
    border_glass = "rgba(255,255,255,0.1)"
    bar_bg = "#FFFFFF"
    bar_shadow = "rgba(0,0,0,0.5)"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_app} !important; color: {text_main}; }}
    h1, h2, h3, h4, h5, h6, p, span, label {{ color: {text_main} !important; }}
    
    /* Barra Flotante Blanca */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background-color: {bar_bg} !important; border-radius: 35px; 
        box-shadow: 0 10px 30px {bar_shadow}; padding: 8px 20px;
        display: flex; justify-content: space-around; border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{ color: #666666 !important; font-size: 0.85em; flex-direction: column; gap: 0px; }}
    .stTabs [aria-selected="true"] {{ color: #C69F40 !important; font-weight: bold; transform: scale(1.1); }}
    .stTabs [data-baseweb="tab-highlight"] {{ background-color: transparent !important; }}
    
    /* Efecto Glassmorphism */
    .card-resumen, .history-card {{
        background: {bg_glass} !important; 
        backdrop-filter: blur(15px) saturate(150%);
        -webkit-backdrop-filter: blur(15px) saturate(150%);
        border-radius: 25px; padding: 25px;
        border: 1px solid {border_glass}; 
        text-align: center; margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    .history-card {{
        border-radius: 18px; padding: 18px; text-align: left;
        border-left: 6px solid {accent_color} !important;
    }}
    
    .main .block-container {{ padding-bottom: 160px; }}
    
    /* Botones Píldora Neón */
    .stButton > button {{
        border-radius: 40px !important; 
        background-color: {accent_color} !important; 
        color: #000000 !important;
        font-weight: 800 !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1px;
    }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tab_home, tab_edit, tab_savings, tab_expenses, tab_income = st.tabs([
    "🏠\nInicio", "⚙️\nConfig", "🐷\nAhorro", "🛍️\nGasto", "💼\nIngreso"
])

with tab_home:
    st.markdown(f"### Hola, Administrador! 👋")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='card-resumen'>
            <small style='color:{text_sec};'>DISPONIBLE</small>
            <h1 style='color:#C69F40; margin: 10px 0;'>${balance:,.2f}</h1>
        </div>""", unsafe_allow_html=True)
    with col2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"""<div class='card-resumen'>
            <small style='color:{text_sec};'>META</small>
            <h1 style='color:{accent_color}; margin: 10px 0;'>{perc}%</h1>
        </div>""", unsafe_allow_html=True)

    st.subheader("Últimos Movimientos")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(5).iterrows():
            icono = ICONOS.get(r['Categoría'], "📝") if r['Tipo'] == "Gasto" else "💰"
            color_monto = accent_color if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>{icono} {r['Detalle']}</b><br><small>{r['Categoría']}</small></div>
                    <div style="color:{color_monto}; font-weight:bold; font-size:1.1em;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_edit:
    st.header("Configuración ⚙️")
    
    # INTERRUPTOR DE TEMA
    st.subheader("Apariencia")
    theme_choice = st.radio("Tema de la app:", ["Oscuro", "Claro"], horizontal=True, index=0 if st.session_state.theme == "Oscuro" else 1)
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.divider()
    st.subheader("Editar Histórico")
    edited_df = st.data_editor(
        df, num_rows="dynamic", use_container_width=True, hide_index=True,
        column_config={
            "Monto": st.column_config.NumberColumn(format="$%.2f"),
            "Tipo": st.column_config.SelectboxColumn(options=["Ingreso", "Gasto"]),
            "Categoría": st.column_config.SelectboxColumn(options=list(ICONOS.keys())),
            "Fecha": st.column_config.DateColumn()
        }
    )
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
    nueva_meta = st.number_input("Ajustar meta ($)", value=META_AHORRO, step=100.0)
    if nueva_meta != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": nueva_meta}, f)
        st.rerun()
    
    progreso = min(max(balance / nueva_meta, 0.0), 1.0)
    st.markdown(f"""
    <div style="background:{bg_glass}; border-radius:20px; padding:30px; border:1px solid {accent_color}; text-align:center;">
        <h1 style="color:{accent_color}; margin:0;">{int(progreso*100)}%</h1>
        <p style='color:{text_sec};'>Progreso hacia ${nueva_meta:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progreso)

with tab_expenses:
    st.header("Nuevo Gasto 🛍️")
    with st.form("f_gasto", clear_on_submit=True):
        c, d, m = st.selectbox("Categoría", list(ICONOS.keys())), st.text_input("Detalle"), st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("REGISTRAR GASTO"):
            pd.concat([df, pd.DataFrame([[date.today(), "Gasto", c, d, m]], columns=df.columns)]).to_csv(DB_FILE, index=False)
            st.toast(f"Registrado: {d}")
            st.rerun()

with tab_income:
    st.header("Nuevo Ingreso 💼")
    with st.form("f_ingreso", clear_on_submit=True):
        d, m = st.text_input("Origen"), st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            pd.concat([df, pd.DataFrame([[date.today(), "Ingreso", "Depósito", d, m]], columns=df.columns)]).to_csv(DB_FILE, index=False)
            st.toast("¡Dinero añadido!")
            st.rerun()
