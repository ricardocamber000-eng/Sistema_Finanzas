import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. RECURSOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"
DB_FILE = "wallet_database.csv"

# 3. CSS (Escapado con doble llave {{ }} para evitar SyntaxError)
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    .main .block-container {{ background-color: rgba(0,0,0,0); }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.98);
        border-right: 2px solid #C69F40;
    }}
    button[data-testid="sidebar-toggle"] svg {{
        fill: #C69F40 !important;
        width: 42px !important;
    }}
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(198, 159, 64, 0.4);
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 30px;
    }}
    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 10px;
        border-left: 5px solid #C69F40;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #C69F40, #8A6D2D);
        color: black !important;
        border: none;
        font-weight: 900;
        width: 100%;
        border-radius: 10px;
    }}
    h1, h2, h3, p, label, span {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
saldo_actual = total_in - total_out

# 5. SIDEBAR
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        cl, cm, cr = st.columns()
        with cm: st.image(LOGO_FILE, width=150)
            
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important; margin-top:-15px;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.write("---")
    
    tab_g, tab_i = st.tabs(["📉 Gasto", "📈 Ingreso"])
    
    with tab_g:
        cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
        with st.form("form_g"):
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True); df.to_csv(DB_FILE, index=False)
                st.rerun()
                
    with tab_i:
        with st.form("form_i"):
            ori = st.text_input("Origen")
            mon_i = st.number_input("Monto ($) ", min_value=0.0)
            if st.form_submit_button("AÑADIR A SALDO"):
                new = pd.DataFrame([[date.today(), "Ingreso", "Fondo", ori, mon_i]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True); df.to_csv(DB_FILE, index=False)
                st.rerun()

# 6. FRONT PRINCIPAL
st.markdown("<h3 style='text-align:center; opacity:0.4; letter-spacing:6px;'>R.C FINANZAS</h3>", unsafe_allow_html=True)

# Saldo Disponible
st.markdown(f"""
<div class="main-balance">
    <p style="margin:0; color:#C69F40 !important; font-weight:bold; letter-spacing:3px;">SALDO DISPONIBLE</p>
    <h1 style="margin:0; font-size:4.8em; font-weight:800;">${saldo_actual:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

st.subheader("Movimientos Recientes")

# Historial (Reconstruido para evitar errores de f-string)
if not df.empty:
    df_v = df.sort_values(by="Fecha", ascending=False).head(10)
    for i, r in df_v.iterrows():
        es_in = r['Tipo'] == "Ingreso"
        color = "#00ff88" if es_in else "#ff4b4b"
        prefijo = "+" if es_in else "-"
        
        # Usamos una estructura más simple para evitar el SyntaxError
        card_html = f"""
        <div class="history-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:left;">
                    <div style="font-weight:bold; font-size:1.1em; color:white;">{r['Detalle']}</div>
                    <div style="font-size:0.85em; opacity:0.6; color:white;">{r['Categoría']} • {r['Fecha']}</div>
                </div>
                <div style="color:{color}; font-weight:900; font-size:1.4em; text-align:right;">
                    {prefijo}${r['Monto']:,.2f}
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("Sin registros.")
