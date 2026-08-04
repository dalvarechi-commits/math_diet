import streamlit as st


def pedirDatosBiometricos(defaults=None):
    """Mostrar formulario de datos biométricos.

    defaults: dict opcional con valores por defecto (p. ej. cargados desde fichero).
    Devuelve dict con los datos si se envía el formulario, o None si no.
    """
    defaults = defaults or {}
    with st.form("formulario_datosBiometricos"):
        email = st.text_input("email", value=defaults.get('email', ''))
        nombre = st.text_input("Nombre", value=defaults.get('nombre', ''))
        peso = st.slider('Peso (kg)', 30, 200, value=int(defaults.get('peso', 70)))
        altura = st.slider('Altura (cm)', 100, 220, value=int(defaults.get('altura', 170)))
        edad = st.number_input("Edad", min_value=0, max_value=100, value=int(defaults.get('edad', 30)))
        sexo_default = defaults.get('sexo', 'Hombre')
        sexo_index = 0 if sexo_default == 'Hombre' else 1
        sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=sexo_index)
        actividad_options = ["Sedentario", "Poca actividad", "Actividad moderada", "Muy activo", "Actividad a nivel profesional"]
        actividad_diaria = st.selectbox(
            "Actividad diaria",
            actividad_options,
            index=(0 if defaults.get('actividad_diaria') is None else actividad_options.index(defaults.get('actividad_diaria')) if defaults.get('actividad_diaria') in actividad_options else 0)
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
                "email": email,
                "nombre": nombre,
                "peso": peso,
                "altura": altura,
                "edad": edad,
                "imc": imc,
                "sexo": sexo,
                "tmb": tmb,
                "energia_total": energia_total,
                "actividad_diaria": actividad_diaria,
            }
        else:
            return None


def pedirPreferenciasAlimentarias(preferencias_labels, defaults=None):
    defaults = defaults or {}
    with st.form("formulario_preferenciasAlimentarias"):
        st.markdown(
            "Selecciona las alergias alimentarias y condiciones dietéticas que se aplican a ti. "
        )

        alergias = st.multiselect(
            "Alergias alimentarias",
            options=list(preferencias_labels.keys()),
            default=defaults.get("alergias", []),
            format_func=lambda value: preferencias_labels[value],
            help="Selecciona una o varias opciones. El formulario guardará las claves internas."
        )

      

        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "alergias": alergias,
               
            }
        else:
            return None


def pedirObjetivosNutricionales(defaults=None):
    defaults = defaults or {}
    opciones = ["Perder peso", "Ganar músculo", "Mantener peso"]
    default_objetivo = defaults.get("objetivo")
    default_index = opciones.index(default_objetivo) if default_objetivo in opciones else 0

    with st.form("formulario_objetivosNutricionales"):
        objetivo = st.selectbox("Selecciona tu objetivo nutricional", opciones, index=default_index)
        enviado = st.form_submit_button("Enviar")

        if enviado:
            return {
                "objetivo": objetivo,
            }
        else:
            return None


def pedirGustos(alimentos, defaults=None):
    defaults = defaults or {}
    
    

    # listado de sliders para cada alimento, con un rango de 1 a 5, y un botón de enviar
    with st.form("formulario_gustos"):
        st.markdown("Valora tu gusto por cada alimento en una escala del 1 al 5, donde 1 es 'No me gusta nada' y 5 es 'Me encanta'.")
        default_gustos = defaults if isinstance(defaults, dict) else {}

        # Organizar por categorías para que la interfaz quede limpia y profesional
        categorias = sorted({info.get("categoria", "Sin categoría") for info in alimentos.values() if info.get("categoria") != "Comidas" and info.get("categoria") != "USUARIO"})

        for cat in categorias:
            with st.expander(f"📂 {cat}"):
                for alimento_key, info in alimentos.items():
                    if info.get("categoria") != cat:
                        continue
                    '''if info.get("categoria") == "Comidas":
                        continue
                    if str(alimento_key).lower() in {"usuario", "user"}:
                        continue
                    if str(info.get("nombre_bedca", "")).lower() in {"usuario", "user"}:
                        continue'''
                    # Obtener el id_bedca del alimento
                    st.write(f"Valoración actual dgrhjdfg: {default_gustos.get(alimento_key)}")
                    st.write(f"Valoración actual info: {info.get('valoracion_usuario', 'No disponible')}")
                    # Primero intenta cargar del defaults del usuario (puede esta bajo alimento_key), luego la valoracion actual, si no, 3
                    default_val = info.get('valoracion_usuario')
                    st.write(f"Valoración actual default_val: {default_val}")
                    if default_val is None:
                        st.write(f"Valoración actual none")
                        default_val = info.get("valoracion_usuario", 3)
                    st.write(("meto valoracion_usuario", default_val))
                    nueva_valoracion = st.slider(
                        label=f"{info.get('nombre_bedca', alimento_key)}",
                        min_value=1,
                        max_value=5,
                        value=int(info.get("valoracion_usuario", 3)),
                        step=1,
                       
                    )
                    # Asignamos el valor en tiempo real directamente al objeto en session_state si existe
                    try:
                        st.session_state.alimentos[alimento_key]["valoracion_usuario"] = nueva_valoracion
                    except Exception:
                        # si no existe session_state.alimentos, actualizamos el dict local
                        alimentos[alimento_key]["valoracion_usuario"] = nueva_valoracion
                    # Guardar con id_bedca como clave para consistencia
                    default_gustos[alimento_key] = nueva_valoracion

        enviado = st.form_submit_button("Enviar Gustos")
        if enviado:
            return default_gustos
        else:
            return None
