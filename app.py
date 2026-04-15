import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA (Sin cambios)
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- PARÁMETROS Y DICCIONARIOS (Sin cambios) ---
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

# --- SISTEMA DE SEGURIDAD (Sin cambios) ---
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

# --- CARGA DE DATOS (Sin cambios) ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# --- CÁLCULOS GLOBALES (Sin cambios) ---
total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
balance = total_in - total_out

# --- ESTILOS CSS (MEJORADOS PARA BARRA FLOTANTE BLANCA) ---
st.markdown("""
<style>
    /* Fondo General (Sin cambios) */
    .stApp { background-color: #0E1117 !important; }

    /* Estilizar las TABS para que PAREZCAN una barra de menú flotante */
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; 
        bottom: 20px;          /* Separación del borde inferior */
        left: 20px;            /* Separación del borde izquierdo */
        right: 20px;           /* Separación del borde derecho */
        width: auto;           /* Ancho automático basado en los bordes laterales */
        z-index: 1000;         /* Asegurar que esté sobre todo */
        
        background-color: white !important; /* Color de fondo blanco */
        border: none !important;           /* Eliminar bordes predeterminados */
        border-radius: 20px;               /* Esquinas redondeadas para el efecto flotante */
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); /* Sombra para dar profundidad y efecto flotante */
        
        display: flex; 
        justify-content: space-around; 
        padding: 10px 0;
    }

    /* Estilo de cada pestaña */
    .stTabs [data-baseweb="tab"] {
        color: black !important;      /* Texto negro sobre fondo blanco */
        background: transparent !important; 
        border: none !important; 
        flex-grow: 1; 
        text-align: center;
        transition: color 0.3s ease; /* Transición suave para el color */
    }

    /* Pestaña activa (Dorado sobre blanco) */
    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;    /* Color dorado para la pestaña activa */
        font-weight: bold !important;
    }

    /* Ajustar el margen inferior del contenido principal */
    .main .block-container { 
        padding-bottom: 130px; /* Incrementar ligeramente para asegurar espacio para la barra flotante */
    }

    /* Tarjetas de Historial (Sin cambios) */
    .history-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 12px;
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #C69F40;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN (Sin cambios) ---
tab_home, tab_stats, tab_savings, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🐷 Ahorro", "🛍️ Gastos", "💼 Ingresos"])

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
    progreso_porcentaje = min(max(balance / META_AHORRO, 0.0), 1.0)
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 15px; padding: 20px; border: 1px solid #C69F40;">
        <h3 style="margin-top:0;">Objetivo: Libertad Financiera</h3>
        <p style="color:#888;">Progreso actual basado en tu balance disponible.</p>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span><b>${balance:,.2f}</b> ahorrados</span>
            <span>Meta: <b>${META_AHORRO:,.2f}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progreso_porcentaje)
    faltante = max(META_AHORRO - balance, 0)
    if faltante > 0:
        st.info(f"Te faltan **${faltante:,.2f}** para alcanzar tu meta. ¡Sigue así!")
    else:
        st.balloons()
        st.success("¡Felicidades! Has alcanzado tu meta de ahorro.")

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
