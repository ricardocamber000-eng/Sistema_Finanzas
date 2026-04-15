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

# 2. RUTAS DE ARCHIVOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"

# 3. ESTILO CSS AVANZADO: FORZAR TEXTURA Y DORADOS
st.markdown(f"""
    <style>
    /* 1. Fondo Global con Textura */
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* 2. Forzar Transparencia para ver el fondo */
    .main .block-container {{
        background-color: rgba(0,0,0,0);
    }}
    
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    /* 3. ICONO DEL SIDEBAR EN DORADO (Selector Robusto) */
    button[kind="headerNoSpacing"] svg, 
    button[data-testid="sidebar-toggle"] svg {{
        fill: #C69F40 !important;
        width: 45px !important;
        height: 45px !important;
    }}
    
    /* 4. Barra Lateral Estilizada */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.95);
        border-right: 2px solid #C69F40;
    }}

    /* 5. Tarjeta de Saldo Principal */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(198, 159, 64, 0.3);
        padding: 50px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }}

    /* 6. Historial Moderno */
    .history-card {{
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 15px 25px;
        margin-bottom: 10px;
        border-left: 4px solid #C69F40;
    }}

    /* 7. Colores de Texto y Botones */
    h1, h2, h3, p, label, span {{
        color: white !important;
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, #C69F40, #8A6D2D);
        color: black !important;
        border: none;
        border-radius: 10px;
        font-weight: 900;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. LÓGICA DE DATOS
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

saldo = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()

# --- 5. SIDEBAR ---
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.write("---")
    
    t1, t2 = st.tabs(["📉 Gasto", "📈 Ingreso"])
    with t1:
        cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
        with st.form("f_gasto"):
            det = st.text_input("Concepto")
            mon = st.number_input("Cantidad ($)", min_value=0.0)
            if st.form_submit_button("REGISTRAR PAGO"):
                new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
    with t2:
        with st.form("f_ingreso"):
            det_i = st.text_input("Origen")
            mon_i = st.number_input("Cantidad ($) ", min_value=0.0)
            if st.form_submit_button("SUMAR CAPITAL"):
                new = pd.DataFrame([[date.today(), "Ingreso", "Fondo", det_i, mon_i]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# --- 6. INTERFAZ PRINCIPAL ---
st.markdown("<br>", unsafe_allow_html=True)

# Saldo con diseño premium
st.markdown(f"""
<div class="main-balance">
    <p style="margin:0; letter-spacing: 3px; color: #C69F40 !important; font-weight: bold; font-size: 1.1em;">SALDO DISPONIBLE</p>
    <h1 style="margin:0; font-size:5em; letter-spacing: -2px;">${saldo:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

# Historial
st.subheader("Movimientos Recientes")
if not df.empty:
    df_sorted = df.sort_values(by="Fecha", ascending=False).head(10)
    for _, row in df_sorted.iterrows():
        is_in = row['Tipo'] == "Ingreso"
        color = "#00ff88" if is_in else "#ff4b4b"
        simbolo = "+" if is_in else "-"
        st.markdown(f"""
<div class="history-card">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-weight:bold; font-size:1.1em;">{row['Detalle']}</div>
            <div style="font-size:0.8em; opacity:0.5;">{row['Categoría']} • {row['Fecha']}</div>
        </div>
        <div style="color:{color}; font-weight:bold; font-size:1.4em;">
            {simbolo}${row['Monto']:,.2f}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
else:
    st.info("Abre el menú lateral dorado para registrar tu primer movimiento.")
</div>
""", unsafe_allow_html=True)
else:
    st.info("Usa el menú lateral dorado para registrar movimientos.")
