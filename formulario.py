import streamlit as st

def pedirDatosBiometricos():
    with st.form("formulario_datosBiometricos"):
        peso = st.slider('Peso (kg)', 30, 200)
        altura = st.slider('Altura (cm)', 100, 220)
        nombre = st.text_input("Nombre")
        edad = st.number_input("Edad", min_value=0, max_value=100)
        enviado = st.form_submit_button("Enviar")

        if enviado:
            if altura > 0:
                imc = peso / (altura / 100) ** 2
            else:
                imc = 0
            return {
                "peso": peso,
                "altura": altura,
                "nombre": nombre,
                "edad": edad,
                "imc": imc
            }
        else:
            return None
def pedirPreferenciasAlimentarias():
    with st.form("formulario_preferenciasAlimentarias"):
        vegetariano = st.checkbox("Vegetariano")
        vegano = st.checkbox("Vegano")
        sin_gluten = st.checkbox("Sin Gluten")
        alergias = st.text_input("Alergias (separadas por comas)")
        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "vegetariano": vegetariano,
                "vegano": vegano,
                "sin_gluten": sin_gluten,
                "alergias": [alergia.strip() for alergia in alergias.split(",")]
            }
        else:
            return None
        
def pedirObjetivosNutricionales():
    with st.form("formulario_objetivosNutricionales"):
        objetivo = st.selectbox("Selecciona tu objetivo nutricional", ["Perder peso", "Ganar músculo", "Mantener peso"])
        calorias_diarias = st.number_input("Calorías diarias", min_value=0)
        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "objetivo": objetivo,
                "calorias_diarias": calorias_diarias
            }
        else:
            return None