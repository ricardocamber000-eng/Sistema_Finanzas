# --- HISTORIAL MINIMALISTA ---
st.divider()
st.subheader("Movimientos Recientes")
if not df.empty:
    # Ordenamos por fecha para ver lo más nuevo arriba
    df_display = df.sort_values(by="Fecha", ascending=False).head(10)
    
    for _, row in df_display.iterrows():
        # Definimos color y símbolo según el tipo
        color = "#00ff88" if row['Tipo'] == "Ingreso" else "#ff4b4b"
        simb = "+" if row['Tipo'] == "Ingreso" else "-"
        
        # El bloque de abajo debe tener EXACTAMENTE el mismo nivel de sangría (indentación)
        st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:bold; font-size:1.1em; color:white;">{row['Concepto']}</div>
                        <div style="font-size:0.8em; opacity:0.5; color:white;">{row['Categoría']} • {row['Fecha']}</div>
                    </div>
                    <div style="color:{color}; font-weight:800; font-size:1.2em;">
                        {simb}${row['Monto']:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No hay movimientos registrados aún.")
