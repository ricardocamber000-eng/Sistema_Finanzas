import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS Y ARCHIVOS
DB_FILE = "wallet_database.csv"
LOGO_FILE = "Logo_RC.png"

# 3. INTERFAZ VISUAL (CSS ORIGINAL + MEJORAS)
st.markdown("""
<style>
    /* Fondo General */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
    }

    /* Sidebar Premium */
    [data-testid="stSidebar"] {
        background-color: #07090D !important;
        border-right: 2px solid #C69F40 !important;
    }

    /* Textos en Blanco */
    h1, h2, h3, p, span, label, .stMarkdown, .stSubheader {
        color: #FFFFFF !important;
    }

    /* Tarjetas de Historial */
    .history-card {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        border-left: 6px solid #C69F40 !important; /* Borde dorado */
    }

    /* Saldo Principal */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.15), rgba(0,0,0,0.6)) !important;
        border: 1px solid #C69F40 !important;
        padding: 40px !important;
        border-radius: 30px !important;
        text-align: center;
        margin-bottom: 30px !important;
    }

    /* Botones Dorados */
    .stButton>button {
        background: linear-gradient(135deg, #C69F40 0%, #8A6D2D 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE BASE DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. BARRA LATERAL (SIDEBAR) - LOGICA ORIGINAL
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    seccion = st.selectbox("Menú Principal", ["🏠 Inicio", "📊 Análisis Interactivo"])
    st.write("---")
    
    st.subheader("Nuevo Movimiento")
    registro_tipo = st.radio("Tipo", ["📉 Gasto", "📈 Ingreso"])
    
    with st.form("panel_registro", clear_on_submit=True):
        if "Gasto" in registro_tipo:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
            det = st.text_input("Descripción / Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0, step=0.01)
            tipo_final = "Gasto"
        else:
            cat = "Depósito"
            det = st.text_input("Origen del Dinero")
            mon = st.number_input("Monto ($)", min_value=0.0, step=0.01)
            tipo_final = "Ingreso"
            
        if st.form_submit_button("GUARDAR EN WALLET"):
            if det and mon > 0:
                nuevo_dato = pd.DataFrame([[date.today(), tipo_final, cat, det, mon]], columns=df.columns)
                df = pd.concat([df, nuevo_dato], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                
                # --- ANIMACIONES SEGÚN TIPO ---
                if tipo_final == "Ingreso":
                    st.balloons()
                    st.toast(f"¡Ingreso de ${mon:,.2f} añadido!", icon="💰")
                else:
                    st.toast(f"Gasto de ${mon:,.2f} registrado.", icon="📉")
                
                time.sleep(1)
                st.rerun()
            else:
                st.error("Completa el concepto y monto.")

# 6. CÁLCULOS GLOBALES (Definir antes de las secciones para evitar NameError)
if not df.empty:
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum()
else:
    total_in = 0
    total_out = 0

total_balance = total_in - total_out

# 7. LÓGICA DE VISUALIZACIÓN CENTRAL
if seccion == "🏠 Inicio":
    # --- DISEÑO DE SALDO CENTRAL ---
    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40 !important; font-weight:bold; letter-spacing:4px; margin-bottom:5px;">SALDO DISPONIBLE</p>
        <h1 style="font-size:5em; margin:0; font-weight:800; color:white;">${total_balance:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # ... (resto de tu código de historial)

elif seccion == "📊 Análisis Interactivo":
    st.title("Panel de Control Visual")
    if not df.empty:
        # Aquí ya puedes usar total_in o total_out sin errores
        st.metric("Gastos Totales", f"${total_out:,.2f}") 
        
        gastos_only = df[df["Tipo"] == "Gasto"]
        # ... (resto de tu código de gráficos)
