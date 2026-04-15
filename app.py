import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN INICIAL (Obligatoria como primera instrucción)
# Usamos un emoji de oro para la pestaña del navegador
st.set_page_config(
    page_title="R.C Finanzas | Lujo Financiero", 
    page_icon="👑", 
    layout="centered"
)

# 2. RUTA DE LA IMAGEN DE FONDO (Si falla, el fondo será negro azulado)
BG_IMAGE = "9313.jpg" 

# URL DEL LOGO (Obtén la URL 'Raw' desde tu GitHub como te expliqué arriba)
# Reemplaza el enlace de abajo por tu enlace directo 'Raw' de GitHub
LOGO_IMAGE_URL = "https://github.com/ricardocamber000-eng/Sistema_Finanzas/blob/main/Logo_RC.png"

# 3. ESTILO CSS: INTEGRACIÓN DE ORO, LOGO Y LIMPIEZA TOTAL
st.markdown(f"""
    <style>
    /* Fondo General con la imagen texturizada */
    .stApp {{
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}

    /* ICONO DEL SIDEBAR EN DORADO (Crucial para visibilidad) */
    button[data-testid="sidebar-toggle"] svg {{
        fill: #C69F40 !important; /* Oro más metálico */
        width: 40px;
        height: 40px;
    }}
    
    /* Borde dorado sutil en el Sidebar */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.98);
        border-right: 1px solid #C69F40;
    }}

    /* Tarjeta de Saldo Principal con efecto "Glassmorphism" premium */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 60px 20px;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }}

    /* Tarjetas de Historial con líneas sutiles */
    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding: 22px;
        margin-bottom: 5px;
    }}

    /* Estilo de Botones (Gradiente Azul a Negro con borde sutil) */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #001f3f);
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Forzar textos en blanco y legibilidad */
    h1, h2, h3, p, label, span, .stMarkdown {{
        color: white !important;
    }}
    
    /* Estilo para los inputs */
    .stNumberInput input, .stTextInput input {{
        background-color: rgba(255,255,255,0.08) !important;
        color: white !important;
        border-radius: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. GESTIÓN DE DATOS (CSV Local)
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    # Validamos que el archivo tenga datos antes de calcular
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    else:
        df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculo de Saldo Vivo (Ingresos menos Gastos)
if not df.empty:
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum()
    saldo = total_in - total_out
else:
    saldo = 0.00

# --- 5. SIDEBAR: REGISTRO DE MOVIMIENTOS ---
with st.sidebar:
    # Mostramos el logo y el nombre de la empresa
    st.image(LOGO_IMAGE_URL, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: white !important; letter-spacing: 1px;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.write("---")
    
    tab_gasto, tab_ingreso = st.tabs(["📉 Gasto", "📈 Ingreso"])
    
    with tab_gasto:
        cat_g = st.selectbox("Categoría de Gasto", ["Deudas", "Servicios", "Mercado", "Placeres"])
        with st.form("form_gasto_sidebar"):
            det_g = st.text_input("Detalle", placeholder="Ej: Pago de Netflix")
            mon_g = st.number_input("Monto ($)", min_value=0.01, step=1.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                nuevo = pd.DataFrame([[date.today(), "Gasto", cat_g, det_g, mon_g]], columns=df.columns)
                df = pd.concat([df, nuevo], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
                
    with tab_ingreso:
        with st.form("form_ingreso_sidebar"):
            det_i = st.text_input("Origen del dinero", placeholder="Ej: Sueldo mensual")
            mon_i = st.number_input("Monto a sumar ($)", min_value=0.01, step=1.0)
            if st.form_submit_button("SUMAR FONDOS"):
                nuevo = pd.DataFrame([[date.today(), "Ingreso", "Fondo", det_i, mon_i]], columns=df.columns)
                df = pd.concat([df, nuevo], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# --- 6. FRONT PRINCIPAL: DASHBOARD ---
# Título minimalista y limpio
st.markdown("<h3 style='text-align: center; opacity: 0.5; letter-spacing: 5px; color: white !important;'>R.C FINANZAS</h3>", unsafe_allow_html=True)

# Widget de Saldo (Fondo Momentáneo)
# AJUSTE SOLICITADO: "SALDO DISPONIBLE" en dorado metálico (#C69F40)
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; letter-spacing: 4px; font-size:1em; color: #C69F40 !important; font-weight: 600;">SALDO DISPONIBLE</p>
        <h1 style="margin:0; font-size:4.8em; font-weight:900; color: white !important;">${saldo:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# Historial de Movimientos
st.subheader("Historial Reciente")
if not df.empty:
    # Ordenar por fecha y tomar los últimos 20 registros
    df_sorted = df.sort_values(by="Fecha", ascending=False).head(20)
    
    for _, row in df_sorted.iterrows():
        is_in = row['Tipo'] == "Ingreso"
        c_monto = "#00ff88" if is_in else "#ff4b4b"
        simb = "+" if is_in else "-"
        
        st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; font-size:1.15em; color:white;">{row['Detalle']}</div>
                        <div style="font-size:0.85em; opacity:0.6; color:white;">{row['Categoría']} • {row['Fecha']}</div>
                    </div>
                    <div style="color:{c_monto}; font-weight:800; font-size:1.4em;">
                        {simb}${row['Monto']:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Despliega el menú lateral (icono dorado) para comenzar a registrar movimientos.")
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("El historial está vacío. Despliega el menú lateral (icono dorado) para comenzar.")
