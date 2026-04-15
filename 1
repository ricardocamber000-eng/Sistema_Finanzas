import streamlit as st
import pandas as pd
from datetime import date
import os

# CONFIGURACIÓN DE ESTILO PERSONALIZADO
st.set_page_config(page_title="Finanzas Pro", layout="centered")

# Inyectamos CSS para "darle vida"
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        border: none;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stExpander"] {
        border-radius: 10px;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Mi Dashboard Financiero")

# --- LÓGICA DE DATOS ---
DB_FILE = "mis_finanzas.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Fecha", "Concepto", "Categoría", "Monto"])

# --- MÉTRICAS PRINCIPALES (Tarjetas visuales) ---
if not df.empty:
    col_a, col_b, col_c = st.columns(3)
    ingresos_t = df[df["Categoría"] == "Ingresos"]["Monto"].sum()
    gastos_t = df[df["Categoría"].isin(["Deudas", "Servicios"])]["Monto"].sum()
    ahorro_t = df[df["Categoría"] == "Ahorro"]["Monto"].sum()

    col_a.metric("Ingresos", f"${ingresos_t:,.2f}", delta_color="normal")
    col_b.metric("Gastos", f"${gastos_t:,.2f}", delta=f"-{gastos_t:,.2f}", delta_color="inverse")
    col_c.metric("Ahorrado", f"${ahorro_t:,.2f}")

st.divider()

# --- INTERFAZ DE REGISTRO CON EXPANDER ---
with st.expander("➕ Registrar Nuevo Movimiento", expanded=False):
    with st.form("registro_pro"):
        c1, c2 = st.columns(2)
        with c1:
            fecha = st.date_input("Fecha", date.today())
            concepto = st.text_input("¿En qué se fue el dinero?", placeholder="Ej: Pago de luz")
        with c2:
            categoria = st.selectbox("Categoría", ["Ingresos", "Deudas", "Servicios", "Ahorro"])
            monto = st.number_input("Monto ($)", min_value=0.0)
        
        if st.form_submit_button("Guardar Movimiento"):
            nuevo = pd.DataFrame([[fecha, concepto, categoria, monto]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.toast(f"¡{categoria} guardado!", icon='💰')
            st.rerun()

# --- SECCIÓN VISUAL ---
st.subheader("Análisis de Gastos")
t1, t2 = st.tabs(["📊 Gráficos", "📋 Historial"])

with t1:
    if not df.empty:
        # Gráfico circular más limpio
        resumen = df.groupby("Categoría")["Monto"].sum()
        st.plotly_chart # (Si usas Plotly, pero el nativo de Streamlit sirve)
        st.bar_chart(resumen, color="#007bff")
    else:
        st.info("Aún no hay datos para mostrar gráficos.")

with t2:
    st.dataframe(df.sort_values(by="Fecha", ascending=False), use_container_width=True)
