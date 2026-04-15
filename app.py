import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE ACCESO ---
USUARIOS = {"admin": "1234", "roberto": "5555", "invitado": "0000"}

if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center; padding:50px 0;'><h1>👑</h1><h2>R.C FINANZAS</h2><p style='opacity:0.5;'>V1.2 Premium</p></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u = st.text_input("Usuario").lower().strip()
        p = st.text_input("PIN", type="password")
        if st.form_submit_button("ENTRAR"):
            if u in USUARIOS and USUARIOS[u] == p:
                st.session_state.authenticated = True
                st.session_state.user = u
                st.rerun()
            else: 
                st.error("Acceso incorrecto")
    st.stop()

# --- LÓGICA DE DATOS ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- ESTILOS CSS CORREGIDOS ---
st.markdown(f"""
<style>
    .stApp {{
        background-color: #08001A !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(45, 0, 102, 0.4) 0px, transparent 55%), 
            radial-gradient(at 100% 0%, rgba(212, 255, 0, 0.08) 0px, transparent 50%), 
            radial-gradient(at 100% 100%, rgba(94, 0, 211, 0.3) 0px, transparent 55%),
            radial-gradient(at 0% 100%, rgba(0, 212, 255, 0.12) 0px, transparent 50%);
        background-attachment: fixed;
    }}

    .card-resumen, .history-card, [data-testid="stForm"], .meta-container {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(35px) saturate(170%);
        border-radius: 28px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 20px;
    }}

    .history-card {{ border-left: 5px solid #D4FF00 !important; }}

    /* BARRA INFERIOR AJUSTADA */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 480px; z-index: 1000;
        background: rgba(15, 5, 40, 0.95) !important;
        backdrop-filter: blur(20px);
        border-radius: 40px; padding: 0 10px;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 70px; display: flex; align-items: center; justify-content: space-around;
    }}

    .stTabs [data-baseweb="tab"] {{
        font-size: 1.8rem !important;
        color: rgba(255,255,255,0.4) !important;
        background: transparent !important;
        border: none !important;
    }}

    .stTabs [aria-selected="true"] {{ color: #D4FF00 !important; transform: scale(1.1); }}
    
    /* Icono de apagado en rojo */
    .stTabs [data-baseweb="tab"]:last-child {{ color: #FF4B4B !important; }}

    .stTabs [data-baseweb="tab-highlight"] {{ display: none !important; }}
    .main .block-container {{ padding-bottom: 120px; }}
</style>
""", unsafe_allow_html=True)

# --- PROCESAMIENTO DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    # Limpieza crítica para evitar el error de NaT/NaN
    df = df.dropna(subset=['Monto'])
    df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0.0)
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

if not df.empty:
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0

# --- NAVEGACIÓN ---
t_h, t_c, t_s, t_g, t_i, t_quit = st.tabs(["🏠", "⚙️", "🐷", "📊", "💼", "🔘"])

with t_h:
    st.markdown(f"### Hola, {USER_ID.upper()}")
    st.markdown(f"""
        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
            <div class="card-resumen" style="flex: 1; margin-bottom: 0;">
                <small style="opacity:0.6;">DISPONIBLE</small>
                <h2 style="margin:0; color:#D4FF00;">${balance:,.2f}</h2>
            </div>
            <div class="card-resumen" style="flex: 1; margin-bottom: 0;">
                <small style="opacity:0.6;">META</small>
                <h2 style="margin:0;">{min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0}%</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Actividad Reciente")
    if not df.empty:
        # Filtrar solo registros válidos para mostrar
        recents = df[df['Monto'] > 0].sort_values(by="Fecha", ascending=False).head(5)
        for _, r in recents.iterrows():
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><small>{r['Fecha']}</small> • <span style='color:#D4FF00;'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)

with t_s:
    st.header("🎯 Meta de Ahorro")
    faltante = max(META_AHORRO - balance, 0.0)
    prog = min(max(balance / META_AHORRO, 0.0), 1.0) if META_AHORRO > 0 else 0
    st.markdown(f"""
        <div class="meta-container" style="text-align: center;">
            <small style="opacity:0.6;">FALTANTE</small>
            <h1 style="color:#FF4B4B; margin: 5px 0;">${faltante:,.2f}</h1>
        </div>
        <div style="width: 100%; background: rgba(255,255,255,0.07); border-radius: 30px; height: 18px; margin: 20px 0; overflow: hidden;">
            <div style="width: {prog*100}%; background: #D4FF00; height: 100%;"></div>
        </div>
    """, unsafe_allow_html=True)
    m = st.number_input("Ajustar Meta ($)", value=float(META_AHORRO))
    if m != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m}, f)
        st.rerun()

with t_c:
    st.subheader("⚙️ Base de Datos")
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Sincronizar Cambios"):
        ed_df.to_csv(DB_FILE, index=False)
        st.success("Datos guardados")

with t_g:
    st.header("🛍️ Registrar Gasto")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", ["Servicios", "Mercado", "Varios"])
        det = st.text_input("Detalle")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("GUARDAR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("💼 Registrar Ingreso")
    with st.form("fi", clear_on_submit=True):
        det = st.text_input("Origen")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_quit:
    st.session_state.clear()
    st.rerun()
