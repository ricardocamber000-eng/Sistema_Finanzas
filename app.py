import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. RECURSOS Y ARCHIVOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"
DB_FILE = "wallet_database.csv"

# 3. CSS MAESTRO (Sin errores de comillas)
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    [data-testid="stSidebar"] {{ 
        background-color: rgba(15, 18, 24, 0.98); 
        border-right: 2px solid #C69F40; 
    }}
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

# 4. CARGA Y GESTIÓN DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. SIDEBAR: NAVEGACIÓN Y REGISTRO
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    seccion = st.selectbox("Navegación", ["🏠 Inicio", "📊 Análisis Interactivo"])
    st.write("---")
    
    tipo_reg = st.radio("Nuevo Movimiento", ["📉 Gasto", "📈 Ingreso"])
    with st.form("form_registro"):
        if "Gasto" in tipo_reg:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0, step=0.01)
            tipo_val = "Gasto"
        else:
            cat = "Depósito"
            det = st.text_input("Origen")
            mon = st.number_input("Monto ($)", min_value=0.0, step=0.01)
            tipo_val = "Ingreso"
            
        if st.form_submit_button("GUARDAR EN WALLET"):
            new_row = pd.DataFrame([[date.today(), tipo_val, cat, det, mon]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

# 6. SECCIONES PRINCIPALES
if seccion == "🏠 Inicio":
    # Lógica de Saldo
    ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    saldo_total = ingresos - gastos

    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40 !important; font-weight:bold; letter-spacing:2px;">SALDO DISPONIBLE</p>
        <h1 style="font-size:3.5em; margin:0;">${saldo_total:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Movimientos Recientes")
    if not df.empty:
        # Mostrar los últimos 8 registros
        for i, r in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():
            simbolo = "+" if r['Tipo'] == "Ingreso" else "-"
            color_txt = "#00ff88" if r['Tipo'] == "Ingreso" else "#ff4b4b"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b style="font-size:1.1em;">{r['Detalle']}</b><br>
                        <small style="opacity:0.6;">{r['Categoría']} • {r['Fecha']}</small>
                    </div>
                    <div style="color:{color_txt}; font-weight:bold; font-size:1.2em;">
                        {simbolo}${r['Monto']:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay registros en la base de datos.")

elif seccion == "📊 Análisis Interactivo":
    st.title("Panel de Control Visual")
    
    if not df.empty:
        tab_pie, tab_line = st.tabs(["Distribución de Gastos", "Evolución de Fondos"])
        
        df_gastos = df[df["Tipo"] == "Gasto"]
        
        with tab_pie:
            if not df_gastos.empty:
                # Paleta manual para evitar AttributeError
                gold_theme = ['#C69F40', '#D4AF37', '#B8860B', '#DAA520', '#8A6D2D']
                
                fig_pie = px.pie(
                    df_gastos, values='Monto', names='Categoría',
                    hole=0.5, title="Gastos por Categoría",
                    color_discrete_sequence=gold_theme
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font_color="white",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.
