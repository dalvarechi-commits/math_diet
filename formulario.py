import streamlit as st

def pedirDatosBiometricos():
    with st.form("formulario_datosBiometricos"):
        peso = st.slider('Peso (kg)', 30, 200)
        altura = st.slider('Altura (cm)', 100, 220)
        nombre = st.text_input("Nombre")
        edad = st.number_input("Edad", min_value=0, max_value=100)
        sexo = st.selectbox("Sexo", ["Hombre", "Mujer"])
        actividad_diaria = st.selectbox("Actividad diaria", ["Sedentario", "Poca actividad", "Actividad moderada", "Muy activo", "Actividad a nivel profesional"])
        enviado = st.form_submit_button("Enviar")

        if enviado:
            if altura > 0:
                imc = peso / (altura / 100) ** 2
                tmb = 10 * peso + 6.25 * altura - 5 * edad + (5 if sexo == "Hombre" else -161)
                energia_total = 0
                if actividad_diaria == "Sedentario":
                    energia_total = tmb * 1.2
                elif actividad_diaria == "Poca actividad":
                    energia_total = tmb * 1.4
                elif actividad_diaria == "Actividad moderada":
                    energia_total = tmb * 1.55
                elif actividad_diaria == "Muy activo":
                    energia_total = tmb * 1.75
                elif actividad_diaria == "Actividad a nivel profesional":
                    energia_total = tmb * 2.0
            else:
                imc = 0
                tmb = 0
            return {
                "peso": peso,
                "altura": altura,
                "nombre": nombre,
                "edad": edad,
                "imc": imc,
                "sexo": sexo,
                "tmb": tmb,
                "energia_total": energia_total
            }
        else:
            return None
        



def pedirPreferenciasAlimentarias(preferencias_labels):
   

    with st.form("formulario_preferenciasAlimentarias"):
        st.markdown(
            "Selecciona las alergias alimentarias y condiciones dietéticas que se aplican a ti. "
           # "Los valores guardados son claves internas para tu menú personalizado."
        )

        alergias = st.multiselect(
            "Alergias alimentarias",
            #options=list(preferencias_labels.values()),
            options=list(preferencias_labels.keys()),
            format_func=lambda value: preferencias_labels[value],
            help="Selecciona una o varias opciones. El formulario guardará las claves internas.")

        vegano = st.checkbox(preferencias_labels["vegano"])
        celiaco = st.checkbox(preferencias_labels["celiaco"])

        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "alergias": alergias,
                "vegano": vegano,
                "celiaco": celiaco
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