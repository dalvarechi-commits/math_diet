from altair import value
import streamlit as st
import formulario

st.header("Bienvenido a Math Diet")
st.write("Esta página te va a ayudar a generar un menú personalizado en función de tus necesidades mediante Teoría de Grafos")
"""
"# Un botón interactivo para probar
datos = formulario.pedirDatosBiometricos()
if datos:
    st.write("Nombre:", datos["nombre"])
    st.write("Peso:", datos["peso"], "kg")
    st.write("Altura:", datos["altura"], "cm")
    st.write("Sexo:", datos["sexo"])
    st.write("Edad:", datos["edad"], "años")
    st.write("IMC:", datos["imc"])
    st.write("TMB:", datos["tmb"], "calorías/día")
    st.write("Energía Total:", datos["energia_total"], "calorías/día")
    st.write("¡Gracias por proporcionar tus datos! Ahora puedes pasar a la siguiente sección para ingresar tus preferencias alimentarias.")
else:    st.write("Por favor, completa el formulario para continuar.")



preferencias = formulario.pedirPreferenciasAlimentarias()
if preferencias:    
    st.write("Alergias alimentarias:")
    for alergia in preferencias["alergias"]:
        st.write("- ", alergia)
    st.write("Vegano:", "Sí" if preferencias["vegano"] else "No")
    st.write("Celiaco:", "Sí" if preferencias["celiaco"] else "No")"""


preferencias_labels = {
        "frutos_secos": "Alergia a los frutos secos — Evita nueces, almendras y avellanas",
        "cacahuetes": "Alergia a los cacahuetes — No comer cacahuetes ni derivados",
        "lactosa": "Intolerancia a la lactosa — Evita leche y lácteos comunes",
        "huevo": "Alergia al huevo — Incluye huevos de gallina y derivados",
        "apio": "Alergia al apio — Evita sopas, caldos y salsas con apio",
        "moluscos": "Alergia a los moluscos — Incluye mejillones, almejas y ostras",
        "pescado": "Alergia al pescado — Evita todo tipo de pescados",
        "crustaceos": "Alergia a los crustáceos — Incluye camarones y langostas",
        "soja": "Alergia a la soja — Evita salsas de soja y productos derivados",
        "mostaza": "Alergia a la mostaza — Incluye mostaza y condimentos similares",
        "sesamo": "Alergia al sésamo — Evita semillas y aceites de sésamo",
        "altramuces": "Alergia a los altramuces — Evita legumbres exóticas",
        "sulfitos": "Alergia al dióxido de azufre y sulfitos — Evita conservantes en bebidas y alimentos",
        "vegano": "Soy vegano — No consumir ningún producto animal",
        "celiaco": "Soy celíaco — Evita gluten y derivados de trigo"
    }



if "datos_completados" not in st.session_state:
    st.session_state.datos_completados = False

if "datos" not in st.session_state:
    st.session_state.datos = None

if "preferencias" not in st.session_state:
    st.session_state.preferencias = None

tab1, tab2 = st.tabs(["Datos Biométricos", "Preferencias Alimentarias"])

with tab1:
    datos = formulario.pedirDatosBiometricos()
    if datos:
        st.session_state.datos_completados = True
        st.session_state.datos = datos
        st.success("✅ Datos biométricos completados")
        st.write("Nombre:", datos["nombre"])
        st.write("Peso:", datos["peso"], "kg")
        st.write("Altura:", datos["altura"], "cm")
        st.write("Sexo:", datos["sexo"])
        st.write("Edad:", datos["edad"], "años")
        st.write("IMC:", datos["imc"])
        st.write("TMB:", datos["tmb"], "calorías/día")
        st.write("Energía Total:", datos["energia_total"], "calorías/día")
        st.write("¡Gracias por proporcionar tus datos! Ahora puedes pasar a la siguiente sección para ingresar tus preferencias alimentarias.")
    else:
        st.write("Por favor, completa el formulario para continuar.")

with tab2:
    if not st.session_state.datos_completados:
        st.error("❌ Debes completar los datos biométricos primero")
    else:
        preferencias = formulario.pedirPreferenciasAlimentarias(preferencias_labels)
        if preferencias:
            st.session_state.preferencias = preferencias
            st.success("✅ Preferencias alimentarias completadas")
            st.write("Alergias alimentarias seleccionadas:")
            for alergia in preferencias["alergias"]:
                st.write("- ", preferencias_labels[alergia])
            st.write("Vegano:", "Sí" if preferencias["vegano"] else "No")
            st.write("Celiaco:", "Sí" if preferencias["celiaco"] else "No")
        elif st.session_state.preferencias:
            st.write("Alergias alimentarias seleccionadas:")
            for alergia in st.session_state.preferencias["alergias"]:
                st.write("- ", alergia)
            st.write("Vegano:", "Sí" if st.session_state.preferencias["vegano"] else "No")
            st.write("Celiaco:", "Sí" if st.session_state.preferencias["celiaco"] else "No")
        else:
            st.write("Completa el formulario de preferencias para ver los resultados.")


