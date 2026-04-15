import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS Y ARCHIVOS
DB_FILE = "wallet_database.csv"
LOGO_FILE = "Logo_RC.png"

# 3. INTERFAZ VISUAL (CSS DE ALTA ESPECIFICIDAD - ESTILO DE LA IMAGEN)
st.markdown("""
<style>
    /* Fondo General (Negro Mate Profundo) */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        background-image: none !important;
    }

    /* Sidebar con Estilo Premium (como la imagen) */
    [data-testid="stSidebar"] {
        background-color: #07090D !important;
        border-right: 2px solid #C69F40 !important; /* Borde dorado pro */
    }

    /* Forzar textos en blanco nítido */
    h1, h2, h3, p, span, label, .stMarkdown, .stSubheader {
        color: #FFFFFF !important;
    }

    /* --- ESTILO DE TARJETAS (Réplica de la imagen) --- */
    .history-card {
        background: rgba(255, 255, 255, 0.04) !important; /* Efecto cristal sutil */
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        transition: 0.3s !important;
    }
    .history-card:hover {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(198, 159, 64, 0.2) !important;
    }
    
    /* Borde dorado solo en el lado izquierdo para el efecto de la imagen */
    .history-card-gold-edge {
        border-left: 6px solid #C69F40 !important;
    }

    /* Contenedor de Saldo Principal (Brillo Dorado Central) */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.15), rgba(0,0,0,0.6)) !important;
        border: 1px solid #C69F40 !important;
        padding: 40px !important;
        border-radius: 30px !important;
        text-align: center;
        margin-bottom: 30px !important;
        box-shadow: 0 0 20px rgba(198, 159, 64, 0.2) !important;
    }

    /* Botones Dorados R.C */
    .stButton>button {
        background: linear-gradient(135deg, #C69F40 0%, #8A6D2D 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 3.2em !important;
        width: 100% !important;
        letter-spacing: 1px !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(198, 159, 64, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE BASE DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. BARRA LATERAL (SIDEBAR): NAVEGACIÓN Y PARÁMETROS
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    seccion = st.selectbox("Menú Principal", ["🏠 Inicio", "📊 Análisis Interactivo"])
    st.write("---")
    
    # Formulario de Registro (Mantenemos todos los parámetros)
    st.subheader("Nuevo Movimiento")
    registro_tipo = st.radio("Tipo", ["📉 Gasto", "📈 Ingreso"])
    
    with st.form("panel_registro"):
        if "Gasto" in registro_tipo:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
            det = st.text_input("Descripción / Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0, step=0.01)
            tipo_final = "Gasto"
        else:
            cat = "Depósito"
            det = st.text_input("Origen del Dinero")
            mon = st.number_input("Monto ($)", min_value=0.0, step=0.01)
            tipo_final = "Ingreso"
            
        if st.form_submit_button("GUARDAR EN WALLET"):
            nuevo_dato = pd.DataFrame([[date.today(), tipo_final, cat, det, mon]], columns=df.columns)
            df = pd.concat([df, nuevo_dato], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

# 6. LÓGICA DE VISUALIZACIÓN
if seccion == "🏠 Inicio":
    # Cálculo de Saldo
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    balance = total_in - total_out

    # --- DISEÑO DE SALDO CENTRAL (Estilo R.C) ---
    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40 !important; font-weight:bold; letter-spacing:4px; margin-bottom:5px;">SALDO DISPONIBLE</p>
        <h1 style="font-size:5em; margin:0; font-weight:800; color:white;">${balance:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # --- DISEÑO DE HISTORIAL (Estilo de la imagen de referencia) ---
    st.markdown("<h3 style='margin-bottom:20px; color:white;'>Historial Reciente</h3>", unsafe_allow_html=True)
    
    if not df.empty:
        # Ordenamos por fecha descendente
        for i, r in df.sort_values(by="Fecha", ascending=False).head(10).iterrows():
            txt_color = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            simbolo = "+" if r['Tipo'] == "Ingreso" else "-"
            
            # Aplicamos la clase 'history-card-gold-edge' para el borde izquierdo dorado
            st.markdown(f"""
            <div class="history-card history-card-gold-edge">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b style="font-size:1.2em; color:white;">{r['Detalle']}</b><br>
                        <small style="color:#C69F40; opacity:0.8;">{r['Categoría']} • {r['Fecha']}</small>
                    </div>
                    <div style="color:{txt_color}; font-weight:900; font-size:1.5em; text-align:right;">
                        {simbolo}${r['Monto']:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Todavía no has registrado movimientos.")

elif seccion == "📊 Análisis Interactivo":
    # Mantenemos el Análisis Interactivo idéntico, solo hereda el fondo oscuro
    st.title("Panel de Control Visual")
    if not df.empty:
        gastos_only = df[df["Tipo"] == "Gasto"]
        if not gastos_only.empty:
            # Gráfico de Dona
            fig = px.pie(gastos_only, values='Monto', names='Categoría', hole=0.6,
                         color_discrete_sequence=['#C69F40', '#D4AF37', '#B8860B', '#8A6D2D'])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico de barras acumulativo
            st.subheader("Gastos por Categoría")
            fig_bar = px.bar(gastos_only.groupby("Categoría")["Monto"].sum().reset_index(), 
                             x="Categoría", y="Monto", color_discrete_sequence=['#C69F40'])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No hay gastos registrados para analizar.")
    else:
        st.info("Ingresa datos en el panel lateral para ver las gráficas.")
