import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- SISTEMA DE SEGURIDAD ---
def check_password():
    """Maneja el estado de la sesión y muestra el login si no está autenticado."""
    if "authenticated" not in st.session_state:
        st.markdown("<h2 style='text-align:center;'>👑 R.C Finanzas</h2>", unsafe_allow_html=True)
        with st.form("Login"):
            st.markdown("### Control de Acceso")
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Ingresar"):
                # CONFIGURA AQUÍ TU USUARIO Y CLAVE
                if user == "admin" and password == "1234":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        return False
    return True

# Si no pasa el login, se detiene la ejecución
if not check_password():
    st.stop()

# --- BARRA LATERAL (Logout) ---
with st.sidebar:
    st.title("Opciones")
    if st.button("Cerrar Sesión"):
        del st.session_state["authenticated"]
        st.rerun()

# 2. PARÁMETROS Y DATOS
DB_FILE = "wallet_database.csv"

if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 3. ESTILOS CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117 !important; }
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #07090D; border-top: 2px solid #C69F40;
        display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000;
    }
    .stTabs [data-baseweb="tab"] { color: #888 !important; flex-grow: 1; text-align: center; }
    .stTabs [aria-selected="true"] { color: #C69F40 !important; font-weight: bold !important; }
    .main .block-container { padding-bottom: 120px; }
    .history-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 16px;
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #C69F40;
    }
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.15), rgba(0,0,0,0.8));
        border: 1px solid #C69F40; padding: 30px; border-radius: 25px;
        text-align: center; margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 4. NAVEGACIÓN
tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🛍️ Gastos", "💼 Ingresos"])

# --- TAB 1: INICIO ---
with tab_home:
    st.markdown("<h2 style='text-align:center;'>RESUMEN GENERAL</h2>", unsafe_allow_html=True)
    
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    balance = total_in - total_out

    # Métricas superiores
    c1, c2 = st.columns(2)
    c1.metric("Total Ingresos", f"${total_in:,.0f}")
    c2.metric("Total Gastos", f"${total_out:,.0f}", delta=f"-{total_out:,.0f}", delta_color="inverse")

    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40; font-weight:bold; letter-spacing:2px; margin-bottom:0;">SALDO DISPONIBLE</p>
        <h1 style="font-size:3.5em; margin:0; color:white;">${balance:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Últimos Movimientos")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(10).iterrows():
            color = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>{r['Detalle']}</b><br><small>{r['Fecha']} • {r['Categoría']}</small></div>
                    <div style="color:{color}; font-size:1.1em; font-weight:bold;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: ANÁLISIS ---
with tab_stats:
    st.header("Análisis de Gastos")
    if not df.empty:
        # Filtro de Mes
        df['Mes-Año'] = pd.to_datetime(df['Fecha']).dt.strftime('%m-%Y')
        mes_seleccionado = st.selectbox("Selecciona un mes para analizar:", df['Mes-Año'].unique())
        
        df_mes = df[df['Mes-Año'] == mes_seleccionado]
        df_gastos = df_mes[df_mes["Tipo"] == "Gasto"]

        if not df_gastos.empty:
            fig = px.pie(df_gastos, values='Monto', names='Categoría', hole=0.6,
                         title=f"Distribución de Gastos ({mes_seleccionado})",
                         color_discrete_sequence=px.colors.sequential.Gold)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Resumen de mesa
            st.write(f"**Total gastado en este periodo:** ${df_gastos['Monto'].sum():,.2f}")
        else:
            st.warning("No hay gastos registrados en este mes.")
    else:
        st.info("Ingresa algunos datos para ver el análisis.")

# --- TAB 3: GASTOS ---
with tab_expenses:
    st.header("Nuevo Gasto 🛍️")
    with st.form("form_gasto", clear_on_submit=True):
        cat = st.selectbox("Categoría", ["Servicios", "Mercado", "Deudas", "Ocio", "Transporte", "Varios"])
        det = st.text_input("Descripción")
        mon = st.number_input("Monto ($)", min_value=0.01, step=1.0)
        fec = st.date_input("Fecha", value=date.today())
        
        if st.form_submit_button("GUARDAR GASTO"):
            new_data = pd.DataFrame([[fec, "Gasto", cat, det, mon]], columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Gasto registrado correctamente")
            st.rerun()

# --- TAB 4: INGRESOS ---
with tab_income:
    st.header("Nuevo Ingreso 💼")
    with st.form("form_ingreso", clear_on_submit=True):
        det = st.text_input("Origen/Detalle")
        mon = st.number_input("Monto ($)", min_value=0.01, step=1.0)
        fec = st.date_input("Fecha", value=date.today())
        
        if st.form_submit_button("AÑADIR INGRESO"):
            new_data = pd.DataFrame([[fec, "Ingreso", "Depósito", det, mon]], columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Ingreso añadido")
            st.rerun()
