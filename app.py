import streamlit as st

import pandas as pd

from datetime import date, timedelta

import os

import plotly.express as px



# 1. CONFIGURACIÓN

st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")



# 2. PARÁMETROS

DB_FILE = "wallet_database.csv"



# 3. ESTILOS CSS (Personalización de la Barra Inferior)

st.markdown("""

<style>

    /* Fondo General */

    .stApp { background-color: #0E1117 !important; }



    /* Estilizar las TABS para que parezcan una barra de menú inferior */

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



    /* Estilo de cada pestaña */

    .stTabs [data-baseweb="tab"] {

        color: #888 !important;

        background: transparent !important;

        border: none !important;

        flex-grow: 1;

        text-align: center;

    }



    /* Pestaña activa (Dorado) */

    .stTabs [aria-selected="true"] {

        color: #C69F40 !important;

        font-weight: bold !important;

    }



    /* Ocultar el margen inferior predeterminado para que no tape el contenido */

    .main .block-container { padding-bottom: 120px; }



    /* Tarjetas de Historial */

    .history-card {

        background: rgba(255, 255, 255, 0.04);

        border: 1px solid rgba(255, 255, 255, 0.05);

        border-radius: 16px;

        padding: 20px;

        margin-bottom: 15px;

        border-left: 6px solid #C69F40;

    }



    /* Balance Central */

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

tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🛍️ Gastos", "💼 Ingresos"])



# --- TAB 1: INICIO ---

with tab_home:

    st.markdown("<h2 style='text-align:center;'>R.C FINANZAS</h2>", unsafe_allow_html=True)

    

    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0

    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0

    balance = total_in - total_out



    # MEJORA: Métricas de resumen rápido

    col1, col2 = st.columns(2)

    col1.metric("Total Ingresos", f"${total_in:,.2f}")

    col2.metric("Total Gastos", f"${total_out:,.2f}", delta=f"-{total_out:,.2f}", delta_color="inverse")



    st.markdown(f"""

    <div class="main-balance">

        <p style="color:#C69F40; font-weight:bold; letter-spacing:2px;">SALDO DISPONIBLE</p>

        <h1 style="font-size:4em; margin:0; color:white;">${balance:,.2f}</h1>

    </div>

    """, unsafe_allow_html=True)



    st.subheader("Historial Reciente")

    if not df.empty:

        # Mostramos los últimos 8 movimientos

        for i, r in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():

            color = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"

            st.markdown(f"""

            <div class="history-card">

                <div style="display:flex; justify-content:space-between;">

                    <div><b>{r['Detalle']}</b><br><small>{r['Categoría']} | {r['Fecha']}</small></div>

                    <div style="color:{color}; font-size:1.2em; font-weight:bold;">${r['Monto']:,.2f}</div>

                </div>

            </div>

            """, unsafe_allow_html=True)



# --- TAB 2: GRÁFICOS ---

with tab_stats:

    st.header("Análisis de Gastos")

    

    if not df.empty and (df["Tipo"] == "Gasto").any():

        # MEJORA: Filtro por periodo

        periodo = st.selectbox("Ver estadísticas de:", ["Histórico Completo", "Últimos 30 días", "Últimos 7 días"])

        

        df_gasto = df[df["Tipo"] == "Gasto"].copy()

        hoy = date.today()

        

        if periodo == "Últimos 30 días":

            df_gasto = df_gasto[df_gasto["Fecha"] >= (hoy - timedelta(days=30))]

        elif periodo == "Últimos 7 días":

            df_gasto = df_gasto[df_gasto["Fecha"] >= (hoy - timedelta(days=7))]



        # Gráfico mejorado

        fig = px.pie(df_gasto, values='Monto', names='Categoría', hole=0.5,

                     title=f"Distribución: {periodo}",

                     color_discrete_sequence=['#C69F40', '#8A6D2D', '#D4AF37', '#555'])

        

        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)

        st.plotly_chart(fig, use_container_width=True)

        

        # Tabla de resumen por categoría

        st.write("Resumen por categoría:")

        st.table(df_gasto.groupby("Categoría")["Monto"].sum().sort_values(ascending=False))

    else:

        st.info("No hay gastos registrados para analizar.")



# --- TAB 3: COMPRAS (GASTOS) ---

with tab_expenses:

    st.header("Registrar Gasto 🛍️")

    with st.form("form_gasto", clear_on_submit=True):

        cat = st.selectbox("Categoría", ["Servicios", "Mercado", "Deudas", "Entretenimiento", "Varios"])

        det = st.text_input("¿En qué gastaste?")

        mon = st.number_input("Monto ($)", min_value=0.0, step=1.0)

        fec = st.date_input("Fecha", date.today())

        

        if st.form_submit_button("REGISTRAR GASTO", use_container_width=True):

            if det and mon > 0:

                new = pd.DataFrame([[fec, "Gasto", cat, det, mon]], columns=df.columns)

                df = pd.concat([df, new], ignore_index=True)

                df.to_csv(DB_FILE, index=False)

                # MEJORA: Feedback táctil/visual

                st.toast(f"Gasto registrado: {det}", icon="💸")

                st.rerun()

            else:

                st.error("Por favor, ingresa un detalle y un monto válido.")



# --- TAB 4: CARTERA (INGRESOS) ---

with tab_income:

    st.header("Registrar Ingreso 💼")

    with st.form("form_ingreso", clear_on_submit=True):

        det = st.text_input("Origen del ingreso (ej. Sueldo, Venta)")

        mon = st.number_input("Monto ($)", min_value=0.0, step=1.0)

        fec = st.date_input("Fecha", date.today())

        

        if st.form_submit_button("AÑADIR A CARTERA", use_container_width=True):

            if det and mon > 0:

                new = pd.DataFrame([[fec, "Ingreso", "Depósito", det, mon]], columns=df.columns)

                df = pd.concat([df, new], ignore_index=True)

                df.to_csv(DB_FILE, index=False)

                # MEJORA: Celebración visual

                st.balloons()

                st.toast("¡Ingreso añadido con éxito!", icon="💰")

                st.rerun()

            else:

                st.error("Datos incompletos.")
