import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="WalletPro: Saldo Vivo", page_icon="💰", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0F1218; }
    .main-balance {
        background: linear-gradient(135deg, #007bff, #0056b3);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,123,255,0.3);
    }
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
DB_FILE = "historial_movimientos.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Concepto", "Monto"])

# --- LÓGICA DE SALDO ---
# Calculamos el fondo momentáneo: Ingresos - Gastos
total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
saldo_actual = total_ingresos - total_gastos

# --- VISTA PRINCIPAL ---
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; opacity:0.8; font-size:1.1em;">Fondo Momentáneo</p>
        <h1 style="margin:0; font-size:3em;">${saldo_actual:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# BOTÓN DE INGRESO EXTRA (Historial Bancario)
with st.expander("💵 Sumar Ingreso Extra"):
    with st.form("nuevo_ingreso"):
        monto_in = st.number_input("Monto a sumar ($)", min_value=0.01)
        fuente_in = st.text_input("Origen", placeholder="Ej: Bono, Venta, Pago extra")
        if st.form_submit_button("Confirmar Ingreso"):
            nuevo = pd.DataFrame([[date.today(), "Ingreso", "Extra", fuente_in, monto_in]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Saldo actualizado")
            st.rerun()

st.divider()

# --- SECCIÓN DE GASTOS (Botón de despliegue por categorías) ---
st.subheader("Registrar Gasto")
cat_gasto = st.selectbox("Selecciona Categoría", ["Deudas", "Servicios", "Mercado", "Placeres"])

with st.form("form_gastos"):
    if cat_gasto == "Deudas":
        sub_cat = st.text_input("¿Qué deuda pagas?", placeholder="Ej: Cashea, Préstamo Juan")
    elif cat_gasto == "Servicios":
        sub_cat = st.text_input("Nombre del Servicio", placeholder="Ej: Netflix, Cantv, Luz")
    elif cat_gasto == "Mercado":
        sub_cat = st.text_input("Detalle", value="Compra Mensual")
    else:
        sub_cat = st.text_input("Detalle del Placer", placeholder="Ej: Café, Cine, Cena")

    monto_gasto = st.number_input("Monto pagado ($)", min_value=0.01)
    
    if st.form_submit_button(f"Registrar en {cat_gasto}"):
        nuevo_g = pd.DataFrame([[date.today(), "Gasto", cat_gasto, sub_cat, monto_gasto]], columns=df.columns)
        df = pd.concat([df, nuevo_g], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.toast(f"Gasto en {cat_gasto} descontado", icon="📉")
        st.rerun()

# --- HISTORIAL TIPO MOVIMIENTO BANCARIO ---
st.divider()
st.subheader("Movimientos Recientes")
if not df.empty:
    for i, row in df.sort_values(by="Fecha", ascending=False).head(10).iterrows():
        color = "#28a745" if row['Tipo'] == "Ingreso" else "#dc3545"
        simbolo = "+" if row['Tipo'] == "Ingreso" else "-"
        st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 5px solid {color};">
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#333; font-weight:bold;">{row['Concepto']}</span>
                    <span style="color:{color}; font-weight:bold;">{simbolo} ${row['Monto']:,.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.8em; color:#666;">
                    <span>{row['Categoría']}</span>
                    <span>{row['Fecha']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No hay movimientos registrados.")
        st.info("No hay historial disponible.")
    st.markdown('</div>', unsafe_allow_html=True)
