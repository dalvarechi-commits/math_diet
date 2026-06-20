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
    # 3. Crear los sliders dinámicamente
        for cat in sorted(categorias):
    # Creamos un contenedor colapsable por cada categoría (ej: "Frutas", "Carnes")
           with st.expander(f"📂 {cat}"):
           
            for id_bedca, info in st.session_state.alimentos.items():
                 if info["categoria"] == cat:
                
                    # Creamos el slider para el alimento específico
                    nueva_valoracion = st.slider(
                    label=f"{info['nombre_bedca']}",
                    min_value=1,
                    max_value=5,
                    value=3,          # Valor por defecto solicitado
                    step=1,           # Incrementos de 1 en 1
                    key=f"slider_{id_bedca}" # Clave única obligatoria para Streamlit
                    )
                    # Asignamos el valor en tiempo real directamente al objeto
                    st.session_state.alimentos[id_bedca]["valoracion_usuario"] = nueva_valoracion
                    gustos[id_bedca] = nueva_valoracion
                    
                
                
        enviado = st.form_submit_button("Enviar Gustos")
        if enviado:
            return gustos
        else:
            return None
        

