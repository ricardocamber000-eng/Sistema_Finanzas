import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(
    page_title="R.C Finanzas", 
    page_icon="👑", 
    layout="centered"
)

# 2. RUTAS DE ARCHIVOS (Asegúrate de que estén en tu GitHub)
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"

# 3. ESTILO CSS: PERSONALIZACIÓN DE LUJO
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    button[data-testid="sidebar-toggle"] svg {{
        fill: #C69F40 !important;
        width: 40px;
        height: 40px;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.98);
        border-right: 2px solid #C69F40;
    }}
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px 20px;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 40px;
    }}
    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #001f3f);
        color: white !important;
        border-radius: 15px;
        font-weight: bold;
    }}
    h1, h2, h3, p, label, span {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. GESTIÓN DE DATOS
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum()
saldo = total_in - total_out

# --- 5. SIDEBAR ---
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.write("---")
    
    t1, t2 = st.tabs(["📉 Gasto", "📈 Ingreso"])
    with t1:
        cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Placeres"])
        with st.form("f_gasto"):
            det = st.text_input("Detalle")
            mon = st.number_input("Monto", min_value=0.0)
            if st.form_submit_button("REGISTRAR"):
                new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
    with t2:
        with st.form("f_ingreso"):
            det_i = st.text_input("Origen")
            mon_i = st.number_input("Monto ", min_value=0.0)
            if st.form_submit_button("AÑADIR"):
                new = pd.DataFrame([[date.today(), "Ingreso", "Fondo", det_i, mon_i]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# --- 6. FRONT PRINCIPAL ---
st.markdown("<h3 style='text-align: center; opacity: 0.5; letter-spacing: 5px;'>R.C FINANZAS</h3>", unsafe_allow_html=True)

st.markdown(f"""
<div class="main-balance">
<p style="margin:0; letter-spacing: 3px; color: #C69F40 !important; font-weight: bold;">SALDO DISPONIBLE</p>
<h1 style="margin:0; font-size:4em;">${saldo:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

st.subheader("Historial Reciente")
if not df.empty:
    df_sorted = df.sort_values(by="Fecha", ascending=False).head(15)
    for _, row in df_sorted.iterrows():
        color = "#00ff88" if row['Tipo'] == "Ingreso" else "#ff4b4b"
        st.markdown(f"""
<div class="history-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="font-weight:bold;">{row['Detalle']}</div>
<div style="font-size:0.8em; opacity:0.6;">{row['Categoría']} • {row['Fecha']}</div>
</div>
<div style="color:{color}; font-weight:bold; font-size:1.2em;">
{" " if row['Tipo'] == "Ingreso" else "-"}${row['Monto']:,.2f}
</div>
</div>
</div>
""", unsafe_allow_html=True)
else:
    st.info("Usa el menú lateral dorado para registrar movimientos.")
