import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- PARÁMETROS Y DICCIONARIOS ---
DB_FILE = "wallet_database.csv"
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

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117 !important; }
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #07090D; border-top: 2px solid #C69F40;
        display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000;
    }
    .main .block-container { padding-bottom: 120px; }
    .history-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 12px;
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #C69F40;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🛍️ Gastos", "💼 Ingresos"])

with tab_home:
    st.markdown("<h2 style='text-align:center;'>MI BILLETERA</h2>", unsafe_allow_html=True)
    
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    balance = total_in - total_out
    
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
                    <div>
                        <span style="font-size: 1.2em; margin-right: 10px;">{icono}</span>
                        <b>{r['Detalle']}</b><br>
                        <small style="color: #666;">{r['Fecha']} • {r['Categoría']}</small>
                    </div>
                    <div style="color:{color_monto}; font-weight:bold;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_stats:
    st.header("Análisis de Finanzas")
    
    if not df.empty:
        # Preparación de datos temporales
        df_temp = df.copy()
        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'])
        df_temp['Mes-Año'] = df_temp['Fecha'].dt.strftime('%m-%Y')
        df_temp['Mes-Orden'] = df_temp['Fecha'].dt.to_period('M').astype(str)

        # 1. GRÁFICO DE BARRAS (COMPARATIVA MENSUAL)
        st.subheader("Ingresos vs Gastos por Mes")
        df_resumen = df_temp.groupby(['Mes-Orden', 'Tipo'])['Monto'].sum().reset_index()
        
        fig_barras = px.bar(
            df_resumen,
            x='Mes-Orden',
            y='Monto',
            color='Tipo',
            barmode='group',
            color_discrete_map={'Ingreso': '#00FF9D', 'Gasto': '#FF4B4B'}
        )
        fig_barras.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_barras, use_container_width=True)

        st.divider()

        # 2. GRÁFICO DE PASTEL (DETALLE POR CATEGORÍA)
        st.subheader("Distribución de Gastos")
        mes_sel = st.selectbox("Filtrar detalle por mes:", df_temp['Mes-Año'].unique())
        
        df_mes = df_temp[(df_temp['Mes-Año'] == mes_sel) & (df_temp['Tipo'] == "Gasto")]
        
        if not df_mes.empty:
            fig_pie = px.pie(df_mes, values='Monto', names='Categoría', hole=0.5,
                             color_discrete_sequence=['#C69F40', '#D4AF37', '#B8860B', '#8A6D2D'])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No hay gastos registrados en el mes seleccionado.")
    else:
        st.info("Aún no hay datos para mostrar el análisis.")

with tab_expenses:
    st.header("Registrar Gasto 🛍️")
    with st.form("form_gasto", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys())[:-2] + ["Varios"])
        det = st.text_input("¿En qué gastaste?")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("GUARDAR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
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
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.toast("¡Dinero añadido!", icon="💰")
            st.rerun()
