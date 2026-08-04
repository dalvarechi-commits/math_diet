from altair import value
import streamlit as st
import formulario
import json
from pathlib import Path
import matplotlib.pyplot as plt
import grafo
import networkx as nx


st.set_page_config(page_title="Math Diet", layout="wide")
alimentos_path_user = Path(__file__).resolve().parent / "datos" / f"alimentos.json"        
alimentos_path_default = Path(__file__).resolve().parent / "datos" / "alimentos.json"

datos_path_user = Path(__file__).resolve().parent / "datos" / f"datosuser.json"


if "user" not in st.session_state:
    st.session_state.user = None

if "alimentos" not in st.session_state:
    # Cargamos el fichero JSON relativo a este archivo (repo_root/datos/alimentos.json)
        
    if "user" in st.session_state:
        alimentos_path_user = Path(__file__).resolve().parent / "datos" / f"alimentos_{st.session_state.get('datos', {}).get('email', 'default')}.json"
        try:
            with alimentos_path_user.open("r", encoding="utf-8") as f:
                st.session_state.alimentos = json.load(f)
                st.write(f"✅ Cargado el fichero de alimentos: {alimentos_path_user}")
        except FileNotFoundError:
            #st.error(f"No se encontró el fichero de alimentos: {alimentos_path_user}. Se cargará el fichero por defecto: {alimentos_path_default}.")
            with alimentos_path_default.open("r", encoding="utf-8") as f:
                st.session_state.alimentos = json.load(f)
                st.write(f"✅ Cargado el fichero de alimentos: {alimentos_path_default}")
            # Simulación por si aún no creas el archivo
        except Exception as e:
            st.error(f"Error cargando {alimentos_path_default}: {e}")
            st.session_state.alimentos = {
                "251111": {"nombre_bedca": "Huevo de gallina entero", "categoria": "Huevos y derivados", "valoracion_usuario": 4.5},
                "295000": {"nombre_bedca": "Merluza fresca", "categoria": "Pescados y derivados", "valoracion_usuario": 4.0}
            }
    else:
        alimentos_path_user = Path(__file__).resolve().parent / "datos" / f"alimentos.json"        
else:   
    try:
        with alimentos_path_user.open("r", encoding="utf-8") as f:
            st.session_state.alimentos = json.load(f)
            st.write(f"✅ Cargado el fichero de alimentos: {alimentos_path_user}")
        
        
    except Exception as e:
        st.error(f"Error cargando {alimentos_path_default}: {e}")
        st.session_state.alimentos = {
            "251111": {"nombre_bedca": "Huevo de gallina entero", "categoria": "Huevos y derivados", "valoracion_usuario": 4.5},
            "295000": {"nombre_bedca": "Merluza fresca", "categoria": "Pescados y derivados", "valoracion_usuario": 4.0}
        }
        


st.header("Bienvenido a Math Diet")
st.write("Esta página te va a ayudar a generar un menú personalizado en función de tus necesidades mediante Teoría de Grafos")


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

if "preferencias_completadas" not in st.session_state:
    st.session_state.preferencias_completadas = False

if "preferencias" not in st.session_state:
    st.session_state.preferencias = None
    
if "objetivo_completado" not in st.session_state:
    st.session_state.objetivo_completado = False


if "objetivos" not in st.session_state:
    st.session_state.objetivos = None


if "gustos" not in st.session_state:
    st.session_state.gustos = None

if "grafo_base" not in st.session_state:
    st.session_state.grafo_base = None
if "grafo_personalizado" not in st.session_state:
    st.session_state.grafo_personalizado = None


def _guardar_datos_usuario():
    datos_usuario = st.session_state.get("datos")
    if not datos_usuario or not datos_usuario.get("email"):
        return
    email = datos_usuario["email"].strip()
    if not email:
        return
    datos_path = Path(__file__).resolve().parent / "datos" / f"datosuser_{email}.json"
    user_data = {
        **datos_usuario,
        "preferencias": st.session_state.get("preferencias"),
        "objetivos": st.session_state.get("objetivos"),
        "gustos": st.session_state.get("gustos"),
    }
    with open(datos_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)


tab1, tab2, tab3, tab4 = st.tabs(["Datos Biométricos", "Alergias y Restricciones", "Objetivos Nutricionales", "Gustos Alimentarios"])

with tab1:
    # permitir cargar datos guardados por email
    cargar_email = st.text_input("Cargar datos por email (si ya existen)")
    if st.button("Cargar datos") and cargar_email.strip():
        datos_path = Path(__file__).resolve().parent / "datos" / f"datosuser_{cargar_email.strip()}.json"
        alimentos_path_user = Path(__file__).resolve().parent / "datos" / f"alimentos_{cargar_email.strip()}.json"
        if datos_path.exists():
            with open(datos_path, 'r', encoding='utf-8') as f:
                datos_cargados = json.load(f)
            st.session_state.datos = datos_cargados
            st.session_state.preferencias = datos_cargados.get('preferencias')
            st.session_state.objetivos = datos_cargados.get('objetivos')
            st.session_state.gustos = datos_cargados.get('gustos')
            st.session_state.datos_completados = True
            st.session_state.preferencias_completadas = True
            st.session_state.objetivo_completado = True
            st.success(f"✅ Datos cargados para: {cargar_email}")
        else:
            st.error("No se encontró datos guardados con ese email.")
        
        if alimentos_path_user.exists():
            with open(alimentos_path_user, 'r', encoding='utf-8') as f:
              
                st.session_state.alimentos = json.load(f)

            st.success(f"✅ Fichero de alimentos cargado para: {cargar_email}")
        else:
            st.error("No se encontró el fichero de alimentos.")

    # pasar valores por defecto si ya estaban en sesión
    defaults = st.session_state.get('datos', {})
    datos = formulario.pedirDatosBiometricos(defaults=defaults)
    if datos:
        st.session_state.datos_completados = True
        st.session_state.datos = datos
        st.success("✅ Datos biométricos completados")
        st.write("email:", datos["email"])
        st.write("Nombre:", datos["nombre"])
        st.write("Peso:", datos["peso"], "kg")
        st.write("Altura:", datos["altura"], "cm")
        st.write("Sexo:", datos["sexo"])
        st.write("Edad:", datos["edad"], "años")
        st.write("IMC:", datos["imc"])
        st.write("TMB:", datos["tmb"], "calorías/día")
        st.write("Energía Total:", datos["energia_total"], "calorías/día")
        st.write("¡Gracias por proporcionar tus datos! Ahora puedes pasar a la siguiente sección para ingresar tus preferencias alimentarias.")

        # guardar datos por email para recuperarlos después
        st.session_state.datos = datos
        _guardar_datos_usuario()
    else:
        st.write("Por favor, completa el formulario para continuar.")

with tab2:
    if not st.session_state.datos_completados:
        st.error("❌ Debes completar los datos biométricos primero")
    preferencias = formulario.pedirPreferenciasAlimentarias(preferencias_labels, defaults=st.session_state.get('preferencias', {}))
    if preferencias:
            st.session_state.preferencias_completadas = True
            st.session_state.preferencias = preferencias
            st.success("✅ Preferencias alimentarias completadas")
            st.write("Alergias alimentarias seleccionadas:")
            for alergia in preferencias["alergias"]:
                st.write("- ", preferencias_labels[alergia])
            _guardar_datos_usuario()
    elif st.session_state.preferencias:
            st.write("Alergias alimentarias seleccionadas:")
            for alergia in st.session_state.preferencias["alergias"]:
                st.write("- ", alergia)
    else:
            st.write("Completa el formulario de alergias y restricciones alimentarias para ver los resultados.")



with tab3:
    if not st.session_state.preferencias_completadas:
        st.error("❌ Debes completar las alergias y restricciones alimentarias primero")
    st.write("Aquí podrás establecer tus objetivos nutricionales y recibir un menú personalizado basado en tus datos biométricos y preferencias alimentarias. ¡Próximamente!")
    defaults_obj = st.session_state.get('objetivos', {})
    objetivo = formulario.pedirObjetivosNutricionales(defaults=defaults_obj)
    if objetivo:
        st.session_state.objetivo_completado = True
        st.session_state.objetivos = objetivo
        st.success("✅ Objetivo nutricional completado")
        st.write("Objetivo seleccionado:", objetivo["objetivo"])
        _guardar_datos_usuario()

with tab4:
    if not st.session_state.objetivo_completado:
        st.error("❌ Debes completar el objetivo antes de continuar")
    st.write("Aquí podrás calificar tus gustos alimentarios para mejorar las recomendaciones de tu menú personalizado. ¡Próximamente!")
    defaults_gustos = st.session_state.get('gustos', {})
    st.write("gustos 1", defaults_gustos)
    gustos = formulario.pedirGustos(st.session_state.alimentos, defaults=defaults_gustos)
    st.write("gustos 2", gustos)
    if gustos:
        st.session_state.gustos = gustos
        st.success("✅ Gustos alimentarios completados")
        #Quitar el print para la versión final, lo dejo para que se vea cómo queda el objeto en el Backend
        st.write("Gustos alimentarios registrados:", gustos)
        _guardar_datos_usuario()
    # 4. Botón opcional para procesar o guardar los datos en el archivo
    st.divider()
    if st.button("Guardar y Actualizar Grafo", type="primary"):
        # Aquí puedes guardar los cambios de vuelta al fichero original si lo deseas
       # alimentos_path = Path(__file__).resolve().parent / "datos" / f"alimentos_{cargar_nombre.strip()}.json"
        with open(Path(__file__).resolve().parent / "datos" / f"alimentos_{st.session_state.datos['email']}.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.alimentos, f, ensure_ascii=False, indent=2)
            #st.session_state.alimentos = json.load(f)
            st.write(f"✅ Guardado el fichero de alimentos: alimentos_{st.session_state.datos['email']}.json")

    st.success("¡Objeto 'alimentos' actualizado y guardado con éxito!")

    # Mostramos un fragmento de cómo queda tu objeto para el Backend (descomenta la línea siguiente para mostrarlo en Streamlit)
    st.json(st.session_state.alimentos)
    fig = grafo.pintarGrafo()
    if fig is not None:
        st.pyplot(fig, use_container_width=True)
        #menu_aleatorio=grafo.generar_menu_aleatorio(st.session_state.grafo_personalizado, nodo_final="Usuario")
    else:
        st.warning('No se pudo generar el grafo. Revisa el archivo de adyacencia.')

    

    
   