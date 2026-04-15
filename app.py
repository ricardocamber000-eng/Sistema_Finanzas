import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# --- SISTEMA DE AUTENTICACIÓN ---
def check_password():
    """Retorna True si el usuario ingresó credenciales correctas."""
    def login_form():
        with st.form("Login"):
            st.markdown("<h3 style='text-align:center;'>Control de Acceso</h3>", unsafe_allow_html=True)
            user = st.text_input("Rcarrero")
            password = st.text_input("Balto30", type="password")
            submit = st.form_submit_button("Entrar")
            
            # Credenciales (puedes cambiarlas aquí)
            if submit:
                if user == "admin" and password == "1234":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")

    if "authenticated" not in st.session_state:
        login_form()
        return False
    return True

# Si el usuario no está autenticado, detener la ejecución aquí
if not check_password():
    st.stop()

# --- BOTÓN DE LOGOUT (Opcional) ---
with st.sidebar:
    if st.button("Cerrar Sesión"):
        del st.session_state["authenticated"]
        st.rerun()

# 2. PARÁMETROS
DB_FILE = "wallet_database.csv"

# 3. ESTILOS CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117 !important; }
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #07090D;
        border-top: 2px solid #C69F40;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
        background: transparent !important;
        border: none !important;
        flex-grow: 1;
        text-align: center;
    }
    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;
        font-weight: bold !important;
    }
    .main .block-container { padding-bottom: 100px; }
    .history-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #C69F40;
    }
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.1), rgba(0,0,0,0.6));
        border: 1px solid #C69F40;
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. ESTRUCTURA DE NAVEGACIÓN (TABS INFERIORES)
# Usamos iconos de Streamlit (Emoji o Material Icons)
tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🛍️ Gastos", "💼 Ingresos"])

# --- TAB 1: INICIO ---
with tab_home:
    st.markdown("<h2 style='text-align:center;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    balance = total_in - total_out

    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40; font-weight:bold; letter-spacing:2px;">SALDO DISPONIBLE</p>
        <h1 style="font-size:4em; margin:0; color:white;">${balance:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Historial")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():
            color = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between;">
                    <div><b>{r['Detalle']}</b><br><small>{r['Categoría']}</small></div>
                    <div style="color:{color}; font-size:1.2em; font-weight:bold;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: GRÁFICOS ---
with tab_stats:
    st.header("Análisis Mensual")
    if not df.empty:
        # Aquí puedes replicar tus gráficos de Plotly
        fig = px.pie(df[df["Tipo"]=="Gasto"], values='Monto', names='Categoría', hole=0.5,
                     color_discrete_sequence=['#C69F40', '#8A6D2D', '#555'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos suficientes para graficar.")

# --- TAB 3: COMPRAS (GASTOS) ---
with tab_expenses:
    st.header("Registrar Gasto 🛍️")
    with st.form("form_gasto"):
        cat = st.selectbox("Categoría", ["Servicios", "Mercado", "Deudas", "Varios"])
        det = st.text_input("¿En qué gastaste?")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("REGISTRAR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

# --- TAB 4: CARTERA (INGRESOS) ---
with tab_income:
    st.header("Registrar Ingreso 💼")
    with st.form("form_ingreso"):
        det = st.text_input("Origen del ingreso")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("AÑADIR A CARTERA"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()
