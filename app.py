import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px # Librería para gráficos pro

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. RECURSOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"
DB_FILE = "wallet_database.csv"

# 3. CSS (Centrado y Estilo)
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    .sidebar-header {{ text-align: center; margin-bottom: 20px; }}
    [data-testid="stSidebar"] {{ background-color: rgba(15, 18, 24, 0.98); border-right: 2px solid #C69F40; }}
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(198, 159, 64, 0.4);
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 30px;
    }}
    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #C69F40;
    }}
    h1, h2, h3, p, label, span {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# 4. DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
saldo = total_in - total_out

# 5. SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, width=120)
    st.markdown("<h2 style='color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    opcion = st.radio("Menú de Registro", ["📉 Registrar Gasto", "📈 Añadir Ingreso"])
    
    if "Gasto" in opcion:
        cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
        with st.form("f_g"):
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True); df.to_csv(DB_FILE, index=False)
                st.rerun()
    else:
        with st.form("f_i"):
            ori = st.text_input("Origen")
            mon_i = st.number_input("Monto ($) ", min_value=0.0)
            if st.form_submit_button("AÑADIR INGRESO"):
                new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", ori, mon_i]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True); df.to_csv(DB_FILE, index=False)
                st.rerun()

# 6. CUERPO PRINCIPAL
st.markdown(f"""
<div class="main-balance">
    <p style="margin:0; color:#C69F40 !important; font-weight:bold; letter-spacing:2px;">SALDO ACTUAL</p>
    <h1 style="margin:0; font-size:4em;">${saldo:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN DE GRÁFICOS ---
if not df.empty:
    st.markdown("### 📊 Análisis de Gastos")
    
    # Preparamos datos para el gráfico de torta (solo gastos)
    df_gastos = df[df["Tipo"] == "Gasto"]
    
    if not df_gastos.empty:
        fig = px.pie(
            df_gastos, 
            values='Monto', 
            names='Categoría',
            hole=0.4,
            color_discrete_sequence=['#C69F40', '#8A6D2D', '#5C4A1E', '#3D3114']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Aún no hay gastos para graficar.")

# --- HISTORIAL ---
st.write("---")
st.subheader("Últimos Movimientos")
if not df.empty:
    for i, r in df.sort_values(by="Fecha", ascending=False).head(5).iterrows():
        color = "#00ff88" if r['Tipo'] == "Ingreso" else "#ff4b4b"
        st.markdown(f"""
        <div class="history-card">
            <div style="display:flex; justify-content:space-between;">
                <span><b>{r['Detalle']}</b> ({r['Categoría']})</span>
                <span style="color:{color}; font-weight:bold;">${r['Monto']:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No hay datos registrados.")
