import streamlit as st


def pedirDatosBiometricos():
    with st.form("formulario_datosBiometricos"):
        nombre = st.text_input("Nombre")
        peso = st.slider('Peso (kg)', 30, 200)
        altura = st.slider('Altura (cm)', 100, 220)
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
                "nombre": nombre,
                "peso": peso,
                "altura": altura,
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
            "Selecciona las alergias alimentarias y restriccio0nes nutricionales que se aplican a ti. "
           # "Los valores guardados son claves internas para tu menú personalizado."
        )

        alergias = st.multiselect(
            "Alergias y restricciones alimentarias",
            #options=list(preferencias_labels.values()),
            options=list(preferencias_labels.keys()),
            format_func=lambda value: preferencias_labels[value],
            help="Selecciona una o varias opciones. El formulario guardará las claves internas.")


        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "alergias": alergias,
            }
        else:
            return None
        
def pedirObjetivosNutricionales():
    with st.form("formulario_objetivosNutricionales"):
        objetivo = st.selectbox("Selecciona tu objetivo nutricional", ["Perder peso", "Ganar músculo", "Mantener peso"])
        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "objetivo": objetivo,
            }
        else:
            return None
        


def pedirGustos(alimentos):
 # listado de sliders para cada alimento, con un rango de 1 a 5, y un botón de enviar
    with st.form("formulario_gustos"):
        st.markdown("Valora tu gusto por cada alimento en una escala del 1 al 5, donde 1 es 'No me gusta nada' y 5 es 'Me encanta'.")
        gustos = {}
       

       # Organizar por categorías para que la interfaz quede limpia y profesional
       # Extraemos las categorías únicas del JSON
        categorias = set(info["categoria"] for info in st.session_state.alimentos.values())
    def pedirDatosBiometricos(defaults=None):
        """Mostrar formulario de datos biométricos.

        defaults: dict opcional con valores por defecto (p. ej. cargados desde fichero).
        Devuelve dict con los datos si se envía el formulario, o None si no.
        """
        defaults = defaults or {}
        with st.form("formulario_datosBiometricos"):
            peso = st.slider('Peso (kg)', 30, 200, value=int(defaults.get('peso', 70)))
            altura = st.slider('Altura (cm)', 100, 220, value=int(defaults.get('altura', 170)))
            nombre = st.text_input("Nombre", value=defaults.get('nombre', ''))
            edad = st.number_input("Edad", min_value=0, max_value=100, value=int(defaults.get('edad', 30)))
            sexo_default = defaults.get('sexo', 'Hombre')
            sexo_index = 0 if sexo_default == 'Hombre' else 1
            sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=sexo_index)
            actividad_diaria = st.selectbox(
                "Actividad diaria",
                ["Sedentario", "Poca actividad", "Actividad moderada", "Muy activo", "Actividad a nivel profesional"],
                index=(0 if defaults.get('actividad_diaria') is None else ["Sedentario", "Poca actividad", "Actividad moderada", "Muy activo", "Actividad a nivel profesional"].index(defaults.get('actividad_diaria')) if defaults.get('actividad_diaria') in ["Sedentario", "Poca actividad", "Actividad moderada", "Muy activo", "Actividad a nivel profesional"] else 0)
            )
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
                    "energia_total": energia_total,
                    "actividad_diaria": actividad_diaria,
                }
            else:
                return None


