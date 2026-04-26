import streamlit as st
import formulario
# Título de la página
st.header("Bien venido a Math Diet")

# Texto normal
st.write("Esta página te va a ayudar a generar un menú personalizado en función de tus necesidades mediante Teoría de Grafos")

# Un botón interactivo para probar
if st.button("Empezar"):
    formulario.mostrarFormulario()
 