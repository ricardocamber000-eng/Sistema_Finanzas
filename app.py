import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE ACCESO (V1.2) ---
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

# --- LÓGICA DE DATOS PERSISTENTES POR USUARIO ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- ESTILOS CSS (AJUSTE DE BARRA DE MENÚ) ---
st.markdown(f"""
<style>
    /* 1. Ajuste del contenedor de la barra */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; 
        bottom: 20px; 
        left: 50%; 
        transform: translateX(-50%);
        width: 95%; 
        max-width: 500px; 
        z-index: 1000;
        background: rgba(15, 5, 40, 0.9) !important; 
        backdrop-filter: blur(20px);
        border-radius: 50px; 
        
        /* Centrado y espacio */
        display: flex; 
        justify-content: space-around; 
        align-items: center;
        height: 75px; /* Altura fija para que los iconos respiren */
        padding: 0 15px;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}

    /* 2. Ajuste de los Iconos individuales */
    .stTabs [data-baseweb="tab"] {{
        font-size: 2.2rem !important; /* Aumentamos el tamaño para llenar la barra */
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        flex-grow: 1; /* Hace que cada botón ocupe el mismo espacio */
        display: flex;
        justify-content: center;
    }}

    /* 3. Efecto al estar seleccionado */
    .stTabs [aria-selected="true"] {{
        transform: scale(1.2);
        transition: transform 0.3s ease;
    }}

    /* Ocultar la línea roja/brillante que Streamlit pone por defecto */
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    /* Margen inferior para que el contenido no quede detrás de la barra */
    .main .block-container {{
        padding-bottom: 120px;
    }}
</style>
""", unsafe_allow_html=True)
# --- SECCIÓN METAS DE AHORRO (DISEÑO FLEX) ---
with t_s:
    st.header("🎯 Mi Meta de Ahorro")
    
    faltante = max(META_AHORRO - balance, 0.0)
    prog = min(max(balance / META_AHORRO, 0.0), 1.0) if META_AHORRO > 0 else 0
    porcentaje = int(prog * 100)

    if faltante > 0:
        st.markdown(f"""
            <div class="meta-container" style="text-align: center;">
                <small style="opacity:0.6; letter-spacing: 1px;">TE FALTAN PARA TU OBJETIVO</small>
                <h1 style="color:#FF4B4B; margin: 10px 0;">${faltante:,.2f}</h1>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="meta-container" style="text-align: center; border: 1px solid #D4FF00;">
                <h2 style="color:#D4FF00; margin: 0;">✨ ¡META ALCANZADA!</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">Has superado tu objetivo de ahorro.</p>
            </div>
        """, unsafe_allow_html=True)

    new_meta = st.number_input("Ajustar mi objetivo total ($)", value=float(META_AHORRO), step=100.0)
    if new_meta != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: 
            json.dump({"meta_ahorro": new_meta}, f)
        st.rerun()

    st.markdown(f"""
        <div style="margin-top: 25px; padding: 10px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-weight:800; color:#D4FF00; font-size: 1.1rem;">{porcentaje}%</span>
                <span style="opacity:0.6;">Goal: ${META_AHORRO:,.0f}</span>
            </div>
            <div style="width: 100%; background: rgba(255,255,255,0.07); border-radius: 30px; height: 26px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden;">
                <div style="width: {prog*100}%; 
                            background: linear-gradient(90deg, #D4FF00, #A6FF00); 
                            height: 100%; 
                            box-shadow: 0 0 25px rgba(212, 255, 0, 0.4);
                            transition: width 0.8s ease-in-out;">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if faltante > 0:
        st.info(f"💡 Tip: Si ahorras $50 semanales adicionales, alcanzarás tu meta en {int(faltante/50) + 1} semanas.")

with t_c:
    st.subheader("Configuración")
    if st.button("Cerrar Sesión"):
        del st.session_state.authenticated
        st.rerun()
    st.divider()
    st.markdown("#### Gestión de Datos")
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios"):
        ed_df.to_csv(DB_FILE, index=False)
        st.success("Base de datos actualizada")

with t_g:
    st.header("Registrar Gasto")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", ["Servicios", "Mercado", "Deudas", "Ocio", "Varios"])
        det = st.text_input("Descripción")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("REGISTRAR"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("Registrar Ingreso")
    options = df[df["Tipo"] == "Ingreso"]["Detalle"].unique().tolist() if not df.empty else []
    with st.form("fi", clear_on_submit=True):
        det_select = st.selectbox("Origen del Dinero", options=options, index=None, placeholder="Selecciona un origen frecuente...")
        det_new = st.text_input("O escribe uno nuevo")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            final_det = det_select if det_select else det_new
            if final_det and mon > 0:
                # CORRECCIÓN: Se cerró correctamente el paréntesis de pd.DataFrame
                new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", final_det, mon]], columns=df.columns)
                pd.concat([df, new]).to_csv(DB_FILE, index=False)
                st.rerun()
