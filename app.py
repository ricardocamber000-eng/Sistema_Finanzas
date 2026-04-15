import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. RECURSOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"
DB_FILE = "wallet_database.csv"

# 3. CSS (Estilos unificados)
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
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

# 4. CARGA DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. SIDEBAR Y NAVEGACIÓN
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    # MENÚ DE NAVEGACIÓN
    seccion = st.selectbox("Ir a:", ["🏠 Inicio", "📊 Análisis Interactivo"])
    st.write("---")
    
    # REGISTRO DE DATOS
    opcion = st.radio("Nuevo Registro", ["📉 Gasto", "📈 Ingreso"])
    with st.form("registro"):
        if "Gasto" in opcion:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0)
            tipo = "Gasto"
        else:
            cat = "Depósito"
            det = st.text_input("Origen")
            mon = st.number_input("Monto ($)", min_value=0.0)
            tipo = "Ingreso"
            
        if st.form_submit_button("GUARDAR"):
            new_data = pd.DataFrame([[date.today(), tipo, cat, det, mon]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

# 6. LÓGICA DE SECCIONES

if seccion == "🏠 Inicio":
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    saldo = total_in - total_out

    st.markdown(f'<div class="main-balance"><p style="color:#C69F40 !important; font-weight:bold;">SALDO DISPONIBLE</p><h1 style="font-size:3.5em;">${saldo:,.2f}</h1></div>', unsafe_allow_html=True)
    
    st.subheader("Movimientos Recientes")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():
            color = "#00ff88" if r['Tipo'] == "Ingreso" else "#ff4b4b"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between;">
                    <span>{r['Detalle']} <small style="opacity:0.5;">({r['Categoría']})</small></span>
                    <span style="color:{color}; font-weight:bold;">${r['Monto']:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Sin registros.")

elif seccion == "📊 Análisis Interactivo":
    st.title("Panel de Análisis")
    
    if not df.empty:
        # Pestañas internas para diferentes tipos de gráficos
        tab1, tab2 = st.tabs(["Gastos por Categoría", "Histórico de Gastos"])
        
        df_gastos = df[df["Tipo"] == "Gasto"]
        
        with tab1:
            if not df_gastos.empty:
                fig_pie = px.pie(
                    df_gastos, values='Monto', names='Categoría',
                    hole=0.4, title="Distribución de Gastos",
                    color_discrete_sequence=px.colors.sequential.Gold
                )
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("No hay gastos registrados para analizar.")
                
        with tab2:
            if not df_gastos.empty:
                # Agrupamos por fecha para ver evolución
                df_time = df_gastos.groupby("Fecha")["Monto"].sum().reset_index()
                fig_line = px.line(
                    df_time, x="Fecha", y="Monto", 
                    title="Tendencia de Gastos en el Tiempo",
                    line_shape="spline", markers=True
                )
                fig_line.update_traces(line_color='#C69F40')
                fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Agrega datos para generar los gráficos interactivos.")
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No hay datos registrados.")
