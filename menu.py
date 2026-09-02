#import grafo
import streamlit as st
import json
from pathlib import Path
import math

"""alimentos = grafo.cargar_alimentos(nombre_usuario="richi")
print(alimentos.keys())

def generar_menu_aleatorio(G_final, nodo_final):
    for nodo in G_final.nodes():
        categoria = nodo.get('categoria', None )

        if categoria == "Comida":
            st.write(f"Nodo inicial: {nodo}")
            menu_aleatorio = grafo.generar_random_walk(
                G=G_final, 
                nodo_inicio=nodo, 
                pasos_maximos=15, 
                nodos_terminales=nodo_final
            )
            st.write(f"Camino generado: {menu_aleatorio}")

            
            
            
            def calcular_peso(alimento, alimentos, objetivos_nutricionales=None):
    #Recuperamos las categorías
    if "categorias" not in st.session_state:
        # Cargamos el fichero JSON relativo a este archivo (repo_root/datos/categorias.json)
        categorias_path = Path(__file__).resolve().parent / "datos" / "categorias.json"
        with open(categorias_path, 'r', encoding='utf-8') as f:
            categorias = json.load(f)
            st.session_state.categorias = categorias
    else:        
        categorias = st.session_state.get("categorias", {})    



    if "distribucion" not in st.session_state:
        # Cargamos el fichero JSON relativo a este archivo (repo_root/datos/distribucion.json)
        distribucion_path = Path(__file__).resolve().parent / "datos" / "distribucion.json"
        with open(distribucion_path, 'r', encoding='utf-8') as f:
            distribuciones = json.load(f)
            st.session_state.distribucion = distribuciones.get(objetivos_nutricionales, {})
    else:        
        distribucion = st.session_state.get("distribucion", {})        
    
    nalimentos_por_cat = 0
    categoria = alimentos.get('categoria')
    for alimento1, propiedades_alimento1 in alimentos.items():
            
        if propiedades_alimento1.get('categoria') == categoria:
        
            nalimentos_por_cat= nalimentos_por_cat + 1
    

    if nalimentos_por_cat == 0: #Esto no debería pasar porque alimento está en la lista de alimentos.
        st.write(f"No se encontraron alimentos en la categoría:",categoria,".")
        return 0
    #peso_personalizado = alimento.get('peso')*distribucion.get(categoria)/nalimentos_por_cat
    peso_personalizado = nalimentos_por_cat
    st.write(f"Peso calculado para {alimento}:{peso_personalizado}")
    return peso_personalizado"""



def nalimentos_por_cat(categoria_buscada, alimentos):
    
    # Recorre el diccionario/lista de alimentos y cuenta cuántos pertenecen a 'categoria_buscada'.
    if not categoria_buscada:
        return 0

    contador = 0
    # Recorremos todos los alimentos disponbles
    for nombre_alimento, propiedades in alimentos.items():
        # Si propiedades es un diccionario (ej: {"categoria": "Carnes", "peso": 100})
        if isinstance(propiedades, dict):
            if propiedades.get('categoria') == categoria_buscada:
                contador += 1
        # Si la estructura fuera simplemente {"Pollo": "Carnes"}
        elif propiedades == categoria_buscada:
            contador += 1

    return contador


def calcular_peso(alimento, alimentos, objetivos_nutricionales=None, w=1, l=5, b=1):
    # Recuperamos las categorías desde session_state o el fichero JSON
    if "categorias" not in st.session_state:
        categorias_path = Path(__file__).resolve().parent / "datos" / "categorias.json"
        with open(categorias_path, 'r', encoding='utf-8') as f:
            categorias = json.load(f)
            st.session_state.categorias = categorias
    else:        
        categorias = st.session_state.get("categorias", {})    

    # Recuperamos la distribución según objetivos
    if "distribucion" not in st.session_state:
        distribucion_path = Path(__file__).resolve().parent / "datos" / "distribucion.json"
        with open(distribucion_path, 'r', encoding='utf-8') as f:
            distribucion = json.load(f)
            st.session_state.distribucion = distribucion.get(objetivos_nutricionales, {})
    else:        
        distribucion = st.session_state.get("distribucion", {})        
    
    # Extraemos el objeto del alimento y su categoría
    datos_alimento = alimentos.get(alimento, {})
    
    if isinstance(datos_alimento, dict):
        categoria = datos_alimento.get('categoria')
    else:
        categoria = datos_alimento  # Por si no se encuentra la categoría en alimentos

    # Llamamos a la función para contar los alimentos de esa categoría
    num_alimentos = nalimentos_por_cat(categoria, alimentos)

    #Validamos que hemos encontrado alimientos porque vamos a dividir por ese número
    if num_alimentos == 0:
        st.write(f"No se encontraron alimentos en la categoría: {categoria}.")
        return 0

    #Cálculo del peso personalizado
    valoracion = datos_alimento.get('valoracion_usuario', 1) if isinstance(datos_alimento, dict) else 1
    # nveces_categoria = distribucion.get("nveces")
    distribucion_categoria =  distribucion.get(categoria)
    #nveces_todo = distribucion.get(categoria)
    # nveces_categoria = eval(nveces_todo) if isinstance(nveces_todo, str) and "/" in nveces_todo else float(nveces_todo)
    """if isinstance(distribucion_categoria, dict):
        distribucion_categoria = distribucion_categoria.get("frecuencia", distribucion_categoria.get("valor", 1))
        st.write(f"distribucion_categoria", distribucion_categoria )
    else:
        st.write(f"ncomidas categoria no es dicionario")"""
    # Conversión segura según el tipo de dato
    st.write(f"distribucion_categoria", distribucion_categoria )
    if isinstance(distribucion_categoria, str) and "/" in distribucion_categoria:
        partes = distribucion_categoria.split("/")
        distribucion_categoria = float(partes[0]) / float(partes[1]) if float(partes[1]) != 0 else 0.0
        st.write(f"distribucion_categoria", distribucion_categoria )
    else:
        try:
            distribucion_categoria = float(distribucion_categoria)
        except (ValueError, TypeError):
            distribucion_categoria = 1.0  # Valor de respaldo si el dato no es convertible
    st.write(f" distribucion_categoria: ", distribucion_categoria)
   
   
    try:
        peso_base = float(distribucion_categoria)
    except:
        st.write(f" distribucion_categoria error: ", distribucion_categoria)
        peso_base = 1 
    
    st.write(f"peso base", peso_base)
    peso_personalizado = w * valoracion + l * math.log(peso_base)
   
   
    st.write(f"Peso calculado para {alimento}: {peso_personalizado} (Total en {categoria}: {num_alimentos})")
    
    return peso_personalizado