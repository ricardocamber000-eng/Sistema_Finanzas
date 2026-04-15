st.markdown(f"""
<style>
    /* 1. FONDO GLOBAL */
    .stApp {{
        background-color: #0E1117 !important;
        background-image: none !important;
    }}

    /* 2. SIDEBAR (Estilo R.C Finanzas) */
    [data-testid="stSidebar"] {{
        background-color: #07090D !important; /* Más oscuro para contraste */
        border-right: 2px solid #C69F40 !important;
    }}

    /* 3. TEXTOS Y ETIQUETAS */
    h1, h2, h3, p, label, .stMarkdown, span, [data-testid="stWidgetLabel"] p {{
        color: #FFFFFF !important;
    }}

    /* 4. TARJETAS DE HISTORIAL (Efecto cristal) */
    .history-card {{
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid #C69F40 !important;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}

    /* 5. INPUTS Y SELECTORES (Dorado) */
    div[data-baseweb="select"] > div {{
        background-color: #1A1D23 !important;
        color: white !important;
        border: 1px solid #C69F40 !important;
    }}
    
    /* 6. BOTÓN PRINCIPAL */
    .stButton>button {{
        background: linear-gradient(135deg, #C69F40 0%, #8A6D2D 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(198, 159, 64, 0.4);
    }}
</style>
""", unsafe_allow_html=True)
