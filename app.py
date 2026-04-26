import streamlit as st
import formulario

# Título de la página
st.header("Bienvenido a Math Diet")

# Texto normal
st.write("Esta página te va a ayudar a generar un menú personalizado en función de tus necesidades mediante Teoría de Grafos")

# Un botón interactivo para probar
datos = formulario.pedirDatosBiometricos()
if datos:
    st.write("Nombre:", datos["nombre"])
    st.write("Peso:", datos["peso"], "kg")
    st.write("Altura:", datos["altura"], "cm")
    st.write("IMC:", datos["imc"])


