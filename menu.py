#import grafo
import streamlit as st
import json
from pathlib import Path
import math
import os




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
    distribucion_categoria =  distribucion.get(categoria)
   
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

def calcular_logit_alimento(alimento, alimentos,objetivos_nutricionales=None, distribucion=None, w=1.0, l=5.0, b=0.0):
    #Calcula la puntuación raw (logit) z_i para un alimento.
    if "distribucion" not in st.session_state:
        distribucion_path = Path(__file__).resolve().parent / "datos" / "distribucion.json"
        with open(distribucion_path, 'r', encoding='utf-8') as f:
            distribucion = json.load(f)
            st.session_state.distribucion = distribucion.get(objetivos_nutricionales, {})
    else:        
        distribucion = st.session_state.get("distribucion", {})        
    
    
    datos_alimento = alimentos.get(alimento, {})
    
    categoria = datos_alimento.get('categoria') if isinstance(datos_alimento, dict) else datos_alimento
    valoracion = datos_alimento.get('valoracion_usuario', 1) if isinstance(datos_alimento, dict) else 1

    distribucion_categoria = distribucion.get(categoria, 1.0)
    # Conversión segura de fracciones a float
    if isinstance(distribucion_categoria, str) and "/" in distribucion_categoria:
            partes = distribucion_categoria.split("/")
            distribucion_categoria = float(partes[0]) / float(partes[1]) if float(partes[1]) != 0 else 0.0
            #st.write(f"distribucion_categoria logit", distribucion_categoria )
    else:
        try:
                distribucion_categoria = float(distribucion_categoria)
                #st.write(f"distribucion_categoria logit", distribucion_categoria )

        except (ValueError, TypeError):
                distribucion_categoria = 1.0  # Valor de respaldo si el dato no es convertible
                st.write(f"distribucion_categoria error")
    try:
        peso_base = float(distribucion_categoria)

    except:
        #st.write(f" distribucion_categoria error: ", distribucion_categoria)
        peso_base = 1 
    
    
 

    # Evitamos log(0) asegurando que peso_base > 0
   # peso_base = max(peso_base, 1e-5)
    
    # Puntuación lineal z_i = w * valoracion + l * ln(peso_base) + b
    z_i = (w * valoracion) + (l * math.log(peso_base)) + b
    return z_i



def aplicar_softmax(diccionario_logits):
    # Aplica Softmax estable a un diccionario {vecino: logit}.
    if not diccionario_logits:
        return {}

    logits = list(diccionario_logits.values())
    max_logit = max(logits)

    exps = {item: math.exp(score - max_logit) for item, score in diccionario_logits.items()}
    suma_exps = sum(exps.values())

    return {item: exp_val / suma_exps for item, exp_val in exps.items()}


def recalcular_pesos_grafo_softmax_local(G, alimentos_usuario, distribucion, w=1, l=5, b=1):
    # Calculamos Softmax de forma LOCAL para cada nodo origen.
    # Las aristas salientes de cada nodo sumarán 1.0.
    for u in G.nodes():
        vecinos = list(G.neighbors(u))
        
        if not vecinos:
            continue

        # Obtenemos los logits SOLO de los vecinos de 'u'
        logits_vecinos = {}
        for v in vecinos:
            logits_vecinos[v] = calcular_logit_alimento(
                alimento=v,
                alimentos=alimentos_usuario,
                distribucion=distribucion,
                w=w, l=l, b=b
            )

        # Aplicamos Softmax únicamente sobre este grupo local
        pesos_locales = aplicar_softmax(diccionario_logits=logits_vecinos)

        # Y asignamos la probabilidad local a cada arista (u, v)
        for v, probabilidad in pesos_locales.items():
            G.edges[u, v]['weight'] = probabilidad

    return G



def calcular_cantidades_alimentos(menu_semanal, alimentos_usuario, distribucion, datos_usuario, categorias):

    menu_calculado = {}
    distribucion_usuario = distribucion.get(datos_usuario.get("objetivo", {}).get("objetivo"), {})
    st.write(f"Distribución del usuario según objetivo {datos_usuario.get('objetivo')}: {distribucion_usuario}")
    calorias_diarias = datos_usuario.get("energia_total", 2000)  # Valor por defecto si no se encuentra

    porcentajes_comidas = {
        "Desayuno": distribucion_usuario.get("pcal_desayuno"),
        "Almuerzo": distribucion_usuario.get("pcal_almuerzo"),
        "Comida": distribucion_usuario.get("pcal_comida"),
        "Snack": distribucion_usuario.get("pcal_snack"),
        "Cena": distribucion_usuario.get("pcal_cena")
        }
    porcentajes_macros_dia = {
        "Hidratos de Carbono": distribucion_usuario.get("pcal_hc/d", 0),
        "Proteínas": distribucion_usuario.get("pcal_prot/d", 0),
        "Lípidos": distribucion_usuario.get("pcal_lip/d", 0)
    }
    #creamos un diccionario para añadir las cantidades de cada alimento en el menú semanal
    # Recorremos el menú semanal y calculamos la cantidad de cada alimento según su categoría y la distribución del usuario
    for comida, datos in menu_semanal.items():
        
        alimentos = datos.get("alimentos", [])
        for alimento in alimentos:
            st.write(f"Calculando cantidad para {alimento} en {comida}")
            categoria = alimentos_usuario.get(alimento, {}).get("categoria") if isinstance(alimentos_usuario.get(alimento, {}), dict) else None
            macro_pincipal = categorias.get(categoria, {}).get("macroprincipal") 
            st.write(f"Categoría: {categoria}, Macro principal: {macro_pincipal}")
            calorías_alimento = alimentos_usuario.get(alimento, {}).get("nutricion_por_100g").get("energia_kcal", 0) if isinstance(alimentos_usuario.get(alimento, {}).get("nutricion_por_100g"), dict) else 0

            porcentaje_categoria = porcentajes_macros_dia.get(categoria, 0)
            porcentaje_comida = porcentajes_comidas.get(categoria, 0)
            st.write(f"Porcentaje de la categoría {categoria}: {porcentaje_categoria}, Porcentaje de la comida {comida}: {porcentaje_comida}")
            # Calculamos la cantidad de alimento en gramos según la distribución y las calorías diarias
            cantidad_alimento = porcentaje_categoria * porcentaje_comida
            if alimento in menu_calculado:
                    menu_calculado[alimento] += cantidad_alimento
            else:
                    menu_calculado[alimento] = cantidad_alimento    

    st.write(f"**Cantidades calculadas para el menú semanal:** {menu_calculado}")