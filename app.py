import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURACIÓN DE PÁGINA (PWA-Ready) ---
st.set_page_config(
    page_title="Wallet Pro: Finanzas",
    page_icon="💳",  # Icono temporal para PWA
    layout="centered"
)

# --- INYECCIÓN DE CSS (El toque profesional) ---
# Clonamos la estructura modular de tu referencia.
st.markdown(f"""
    <style>
    /* Fondo Negro Profundo para la App */
    .stApp {{ background-color: #0F1218; }}

    /* Títulos Principales en Blanco */
    [data-testid="stHeader"] {{ color: white; font-weight: 700; font-size: 2.2em; }}

    /* Tarjetas Modulares Blancas (Copian tu referencia) */
    .stCard {{
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}

    /* Estilo para st.metric (las tarjetas de arriba) */
    [data-testid="stMetricValue"] {{ font-size: 1.8em; color: #333; }}
    [data-testid="stMetricLabel"] {{ font-size: 0.9em; color: #666; font-weight: 600; text-transform: uppercase; }}

    /* Botón Profesional (Azul Eléctrico) */
    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background-color: #007bff; /* Azul primario */
        color: white;
        font-weight: 700;
        border: none;
    }}
    .stButton>button:hover {{ background-color: #0056b3; }}

    /* st.expander estilizado */
    div[data-testid="stExpander"] {{
        background-color: white;
        border-radius: 12px;
        border: 1px solid #EAEAEA;
        margin-bottom: 25px;
    }}

    </style>
    """, unsafe_allow_html=True)

st.title("WalletPro: Tu Resumen")

# --- LÓGICA DE DATOS ---
DB_FILE = "mis_finanzas.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Fecha", "Concepto", "Categoría", "Monto"])

# --- MÉTRICAS CLAVE (Tarjetas Superiores) ---
# Usamos columnas nativas pero el CSS les da la forma modular.
if not df.empty:
    col_ing, col_gast, col_aho = st.columns(3)
    ingresos_t = df[df["Categoría"] == "Ingresos"]["Monto"].sum()
    gastos_t = df[df["Categoría"].isin(["Deudas", "Servicios"])]["Monto"].sum()
    ahorro_t = df[df["Categoría"] == "Ahorro"]["Monto"].sum()

    # Formateamos los números como dinero
    with col_ing:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.metric("Ingresos Total", f"${ingresos_t:,.2f}", delta_color="normal")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_gast:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.metric("Gastos Total", f"${gastos_t:,.2f}", delta=f"-${gastos_t:,.2f}", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_aho:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.metric("Ahorro Acumulado", f"${ahorro_t:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- FORMULARIO DE REGISTRO (Oculto en Expander) ---
# Útil en móvil para no ocupar pantalla.
with st.expander("➕ Nuevo Gasto / Ingreso", expanded=False):
    with st.form("registro_profesional"):
        c1, c2 = st.columns(2)
        with c1:
            fecha = st.date_input("Fecha", date.today())
            # Conceptos de tu referencia
            concepto = st.text_input("¿En qué se fue el dinero?", placeholder="Ej: Pago de Luz")
        with c2:
            # Usamos emojis para un look más "App"
            categoria = st.selectbox("Categoría", ["💰 Ingresos", "💳 Deudas", "💡 Servicios", "🏦 Ahorro"])
            monto = st.number_input("Monto ($)", min_value=0.01)

        if st.form_submit_button("Guardar Movimiento"):
            # Limpiamos el emoji para la base de datos
            cat_limpia = categoria.split(" ")
            nuevo = pd.DataFrame([[fecha, concepto, cat_limpia, monto]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.toast(f"¡{cat_limpia} guardado con éxito!", icon='💰')
            st.rerun()

# --- SECCIÓN VISUAL Y DE DATOS ---
st.subheader("Análisis de Cuenta")
t_graf, t_hist = st.tabs(["📊 Distribución", "📋 Historial"])

with t_graf:
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    if not df.empty:
        # Gráfico de barras azul sobre fondo blanco
        resumen = df.groupby("Categoría")["Monto"].sum()
        st.bar_chart(resumen, color="#007bff")
    else:
        st.info("Registra tu primer movimiento para ver gráficos.")
    st.markdown('</div>', unsafe_allow_html=True)

with t_hist:
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    if not df.empty:
        # Mostramos los últimos movimientos primero
        st.dataframe(df.sort_values(by="Fecha", ascending=False), use_container_width=True)
    else:
        st.info("No hay historial disponible.")
    st.markdown('</div>', unsafe_allow_html=True)
