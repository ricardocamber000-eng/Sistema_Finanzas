import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- PARÁMETROS Y DICCIONARIOS ---
DB_FILE = "wallet_database.csv"
META_AHORRO = 3000.0
ICONOS = {
    "Servicios": "💡",
    "Mercado": "🛒",
    "Deudas": "💳",
    "Ocio": "🎬",
    "Transporte": "🚗",
    "Depósito": "💰",
    "Varios": "📦"
}

# --- SISTEMA DE SEGURIDAD ---
def check_password():
    if "authenticated" not in st.session_state:
        st.markdown("<h2 style='text-align:center;'>👑 R.C Finanzas</h2>", unsafe_allow_html=True)
        with st.form("Login"):
            st.markdown("### Control de Acceso")
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Ingresar"):
                if user == "admin" and password == "1234":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        return False
    return True

if not check_password():
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

# --- ESTILOS CSS (BARRA BLANCA FLOTANTE PREMIUM) ---
st.markdown("""
<style>
    /* Fondo General */
    .stApp { background-color: #0E1117 !important; }

    /* Barra de Menú Flotante Blanca */
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; 
        bottom: 25px; 
        left: 50%;
        transform: translateX(-50%);
        width: 90%; 
        max-width: 500px;
        z-index: 1000;
        
        background-color: #FFFFFF !important; 
        border-radius: 30px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        padding: 10px 15px;
        display: flex;
        justify-content: space-around;
        border: none !important;
    }

    /* Quitar la línea inferior naranja por defecto de Streamlit */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    /* Estilo de los items del menú */
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: #666666 !important;
        flex-direction: column;
        gap: 0px;
        transition: all 0.3s ease;
    }

    /* Item seleccionado: Letra más grande y color dorado */
    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;
        transform: scale(1.1);
    }

    /* Ajuste para que el contenido no quede debajo de la barra */
    .main .block-container { padding-bottom: 150px; }

    /* Tarjetas de historial */
    .history-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 12px;
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #C69F40;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN CON ICONOS DINÁMICOS ---
# Usamos saltos de línea en el nombre para que el icono quede arriba del texto (en móviles se ve genial)
tab_home, tab_stats, tab_savings, tab_expenses, tab_income = st.tabs([
    "🏠\nInicio", 
    "📊\nStats", 
    "🐷\nAhorro", 
    "🛍️\nGasto", 
    "💼\nIngreso"
])

with tab_home:
    st.markdown("<h2 style='text-align:center;'>MI BILLETERA</h2>", unsafe_allow_html=True)
    color_borde = "#C69F40" if balance >= 0 else "#FF4B4B"
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 30px; 
                border-top: 5px solid {color_borde}; text-align: center; margin-bottom: 25px;">
        <p style="color: #888; margin: 0; font-size: 0.9em; letter-spacing: 2px;">SALDO DISPONIBLE</p>
        <h1 style="margin: 10px 0; font-size: 3.5em; color: white;">${balance:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Actividad Reciente")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():
            icono = ICONOS.get(r['Categoría'], "📝") if r['Tipo'] == "Gasto" else "💰"
            color_monto = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><span style="font-size: 1.2em; margin-right: 10px;">{icono}</span><b>{r['Detalle']}</b><br>
                    <small style="color: #666;">{r['Fecha']} • {r['Categoría']}</small></div>
                    <div style="color:{color_monto}; font-weight:bold;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_stats:
    st.header("Análisis de Finanzas")
    if not df.empty:
        df_temp = df.copy()
        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'])
        df_temp['Mes-Orden'] = df_temp['Fecha'].dt.to_period('M').astype(str)
        st.subheader("Ingresos vs Gastos por Mes")
        df_resumen = df_temp.groupby(['Mes-Orden', 'Tipo'])['Monto'].sum().reset_index()
        fig_barras = px.bar(df_resumen, x='Mes-Orden', y='Monto', color='Tipo', barmode='group',
                            color_discrete_map={'Ingreso': '#00FF9D', 'Gasto': '#FF4B4B'})
        fig_barras.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_barras, use_container_width=True)

with tab_savings:
    st.header("Meta de Ahorro 🐷")
    
    # Progreso
    progreso = min(max(balance / META_AHORRO, 0.0), 1.0)
    porcentaje_texto = int(progreso * 100)
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 25px; border: 1px solid #C69F40; text-align: center;">
        <h2 style="color: #C69F40; margin-bottom: 5px;">{porcentaje_texto}% completado</h2>
        <p style="color: #888;">Meta: <b>${META_AHORRO:,.2f}</b></p>
        <div style="font-size: 4em; margin: 20px 0;">{"💰" if progreso < 1 else "👑"}</div>
        <div style="display: flex; justify-content: space-between; font-size: 0.9em; color: #888;">
            <span>$0</span>
            <span>${balance:,.2f} actual</span>
            <span>${META_AHORRO:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(progreso)
    
    if balance < META_AHORRO:
        faltante = META_AHORRO - balance
        st.info(f"Faltan **${faltante:,.2f}** para tu objetivo. ¡Tú puedes!")
    else:
        st.balloons()
        st.success("¡META LOGRADA! Eres un maestro del ahorro.")

with tab_expenses:
    st.header("Registrar Gasto 🛍️")
    with st.form("form_gasto", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys())[:-2] + ["Varios"])
        det = st.text_input("¿En qué gastaste?")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("GUARDAR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns[:5])
            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.toast(f"Registrado: {det}", icon="✅")
            st.rerun()

with tab_income:
    st.header("Registrar Ingreso 💼")
    with st.form("form_ingreso", clear_on_submit=True):
        det = st.text_input("Origen del ingreso")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("AÑADIR A CARTERA"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns[:5])
            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.toast("¡Dinero añadido!", icon="💰")
            st.rerun()
