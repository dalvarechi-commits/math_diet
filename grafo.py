# dibujar un grafo con matplotlib
import csv
import json
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import random
import menu


if "categorias" not in st.session_state:
    # Cargamos el fichero JSON relativo a este archivo (repo_root/datos/categorias.json)
    categorias_path = Path(__file__).resolve().parent / "datos" / "categorias.json"
    with open(categorias_path, 'r', encoding='utf-8') as f:
        categorias = json.load(f)

# generar adyacencia desde .csv
def cargar_adyacencia_desde_csv(m_adyacencia):
    if not Path(m_adyacencia).is_absolute():
        m_adyacencia = Path(__file__).resolve().parent / m_adyacencia

    adyacencia = {}
    with open(m_adyacencia, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=';')
        header = next(lector, None)
        if not header or len(header) < 2:
            raise ValueError(f'Cabecera inválida en {m_adyacencia}')
        node_names = header[1:]
        for fila in lector:
            if not fila or len(fila) < 2:
                continue
            nodo = fila[0]
            valores = fila[1:]
            vecinos = []
            for i, val in enumerate(valores):
                text = val.strip().replace(',', '.')
                if not text:
                    continue
                try:
                    peso = float(text)
                except ValueError:
                    continue
                if peso > 0:
                    vecinos.append((node_names[i], peso))
            adyacencia[nodo] = vecinos
    return adyacencia



def cargar_alimentos(ruta=None, nombre_usuario=None):
    """Carga los alimentos desde datos/alimentos.json o desde un archivo de usuario."""
    if ruta:
        alimentos_path = Path(ruta)
    elif nombre_usuario:
        alimentos_path = Path(__file__).resolve().parent / "datos" / f"alimentos_{nombre_usuario}.json"
        if not alimentos_path.exists():
            alimentos_path = Path(__file__).resolve().parent / "datos" / "alimentos.json"
    else:
        alimentos_path = Path(__file__).resolve().parent / "datos" / "alimentos.json"

    with open(alimentos_path, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    if isinstance(datos, dict):
        if "alimentos" in datos and isinstance(datos["alimentos"], dict):
            return datos["alimentos"]
        return datos

    raise ValueError(f"Formato no soportado en {alimentos_path}")


def obtener_alimentos(alimentos=None, nombre_usuario=None, ruta=None):
    if alimentos is not None:
        return alimentos

    if "alimentos" in st.session_state and st.session_state.alimentos:
        if nombre_usuario is not None:
            return st.session_state.alimentos_user
        return st.session_state.alimentos

    return cargar_alimentos(ruta=ruta, nombre_usuario=nombre_usuario)


# crear un grafo desde una lista de adyacencia
def crear_grafo(adyacencia):
    G = nx.DiGraph()
    for nodo, vecinos in adyacencia.items():
        for vecino, peso in vecinos:
            if peso > 0:
                st.write("nodos solo adyacencia")
                G.add_edge(nodo, vecino, weight=peso)
    return G

def crear_grafo(adyacencia, alimentos=None, datos_usuario=None):
    G = nx.DiGraph()
    if alimentos is None:
        for nodo, vecinos in adyacencia.items():
            for vecino, peso in vecinos:
                if peso > 0:  
                    st.write("nodos con alimentos none")
                    G.add_edge(nodo, vecino, weight=peso)
    else:
        for nodo, vecinos in adyacencia.items():
            if nodo not in alimentos:
                continue  # Saltar nodos que no están en la lista de alimentos del usuario  
            else: 
                for vecino, peso in vecinos:
                    if peso > 0:
                       st.write("nodos con alimentos personalizados")
                       #calcular_peso(alimento, alimentos, objetivos_nutricionales
                       peso_personalizado = menu.calcular_peso(vecino, alimentos, datos_usuario.get('objetivos').get('objetivo'))
                       st.write(f"Peso personalizado2:",{peso_personalizado})
                       G.add_edge(nodo, vecino, weight=peso_personalizado)
    
    return G



def _normalizar_color(color):
    if not color:
        return 'lightgray'

    aliases = {
        'light red': 'mistyrose',     
        'light yellow': 'lemonchiffon',
        'dark pink': 'hotpink',        
        'light blue': 'powderblue',    
        'lightgray': 'gainsboro',      
        'red': 'salmon',               
        'yellow': 'yellow',           
        'light green': 'palegreen',    
        'orange': 'navajowhite',       
        'light purple': 'lavender',    
        'mint': 'aquamarine',          
        'peach': 'peachpuff',          
        'lilac': 'thistle',            
        'beige': 'wheat'
    }
    return aliases.get(color.lower(), color)


# dibujar el grafo
def dibujar_grafo(G, alimentos=None):
    alimentos_data = obtener_alimentos(alimentos)
    fig, ax = plt.subplots(figsize=(30, 25))

    # Orden de capas según macroprincipal de cada categoría
    macroprincipales = []
    categoria_a_macro = {}
    for categoria, meta in categorias.items():
        macro = meta.get('macroprincipal')
        categoria_a_macro[categoria] = macro
        if macro is not None and macro not in macroprincipales:
            macroprincipales.append(macro)

    # Garantizar que las categorías sin macroprincipal queden al final
    if None not in macroprincipales:
        macroprincipales.append(None)
    macro_a_capa = {macro: idx for idx, macro in enumerate(macroprincipales)}

    # Determinar la categoría y macroprincipal de cada nodo
    categoria_por_nodo = {}
    macro_por_nodo = {}
    capa_por_nodo = {}
    for nodo in G.nodes():
        categoria = None
        if nodo in alimentos_data:
            categoria = alimentos_data[nodo].get('categoria')
            G.nodes[nodo]['categoria'] = categoria  # Guardar la categoría en el nodo para uso futuro
      
        categoria_por_nodo[nodo] = categoria
        macro_por_nodo[nodo] = categoria_a_macro.get(categoria)
        capa_por_nodo[nodo] = categorias.get(categoria, {}).get('capa')

    # Posiciones por capas: y fija según macroprincipal, x distribuida por nodo
    nodos = list(G.nodes())
    nodos_por_capa = {}
    for nodo in nodos:
        categoria = categoria_por_nodo.get(nodo)
        macro = macro_por_nodo.get(nodo)
        capa = capa_por_nodo.get(nodo)
        nodos_por_capa.setdefault(capa, []).append(nodo)

    pos = {}
    total_capas = max(len(nodos_por_capa), 1)
    if nodos_por_capa is not None:
        for capa, nodos_capa in nodos_por_capa.items():
            cantidad = len(nodos_capa)
            divisor_x = max(1, cantidad + 1) # Ajusta el espaciado horizontal dentro de la capa

            # Calculamos la posición Y distribuida uniformemente entre 0 y 1
            # Si solo hay 1 capa, la ponemos en el centro (0.5)
            if capa is not None:
                if total_capas > 1:
                    y_pos = 1.0 - (capa / (total_capas - 1))
                else:
                    y_pos = 0.5

                for i_nodo, nodo in enumerate(nodos_capa):
                    x_pos = (i_nodo + 1) / divisor_x
                    pos[nodo] = (x_pos, y_pos)

   
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
    edge_widths = [1 * w for w in edge_weights]

    color_map = []
    for nodo in G.nodes():
        categoria = categoria_por_nodo.get(nodo)
        color = _normalizar_color(categorias.get(categoria, {}).get('color', 'lightgray'))
        color_map.append(color)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=color_map, node_size=2000)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight='bold')
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        arrows=True,
        arrowstyle='->',
        arrowsize=15,
        width=edge_widths,
        edge_color='black',
        connectionstyle='arc3,rad=0',
        min_source_margin=30,
        min_target_margin=30,
    )
    ax.set_axis_off()
    return fig
    

def pintarGrafo(m_adyacencia='m_adyacencia.csv', alimentos=None, nombre_usuario=None, ruta=None):
    st.write("Generando grafo de alimentos con parámetros...")
    adyacencia = cargar_adyacencia_desde_csv(m_adyacencia)
    if alimentos is None:
        alimentos = obtener_alimentos(nombre_usuario=nombre_usuario, ruta=ruta)

    if nombre_usuario is None:
       G = crear_grafo(adyacencia)
       st.session_state.grafo = G
       alimentos_data = obtener_alimentos(alimentos)
    else:
       
        G = crear_grafo(adyacencia, st.session_state.alimentos_user, st.session_state.datos)
        st.session_state.grafo_personalizado = G   
        alimentos_data = obtener_alimentos(st.session_state.alimentos_user, nombre_usuario=nombre_usuario, ruta=ruta)
    if len(G) == 0:
        return None
    return dibujar_grafo(G, alimentos_data)


def cargar_adyacencia_desde_json(grafo_nodos_enlaces):
    with open(grafo_nodos_enlaces, 'r', encoding='utf-8') as archivo:
        adyacencia = json.load(archivo)
    return adyacencia    

def podarGrafo(G, alimentos_usuario):
    """Elimina del grafo G los nodos que no están en la lista de alimentos del usuario y 
    recalcula los pesos en función de los alimentos y objetivos del usuario"""
    nodos_a_eliminar = [nodo for nodo in G.nodes() if nodo not in alimentos_usuario]
    G.remove_nodes_from(nodos_a_eliminar)

    for nodo in G.nodes():
        #Recorremos los nodos del grafo para modificar todas sus aristas con los pesos calculados

        '''st.write("nodos con alimentos personalizados")
        #calcular_peso(alimento, alimentos, objetivos_nutricionales
                            peso_personalizado = menu.calcular_peso(vecino, alimentos, datos_usuario.get('objetivos').get('objetivo'))
                            st.write(f"Peso personalizado2:",{peso_personalizado})
                            G.add_edge(nodo, vecino, weight=peso_personalizado)'''
    return G


# ------------------------------------------------------------------
# FUNCION AUXILIAR: Extrae el diccionario de reglas directamente
# ------------------------------------------------------------------
def extraer_reglas_desde_json():
    """Extrae las listas de 'cat_alimentos' de cada comida del JSON."""
    reglas = {}
    for comida, info in categorias.items():
        if isinstance(info, dict) and "cat_alimentos" in info:
            # Como en el JSON 'cat_alimentos' ya es una lista [...],
            # Python la lee directamente como list sin necesidad de parsear.
            reglas[comida] = info["cat_alimentos"]
    return reglas


# ------------------------------------------------------------------
# 1. FUNCION: generar_random_walk
# ------------------------------------------------------------------
def generar_random_walk(
    G, nodo_inicio, pasos_maximos=20, nodos_terminales=None, categorias_permitidas=None
):
    """Genera un camino aleatorio en el grafo G limitando los pasos a nodos que

    tengan una categoría que esté dentro de 'categorias_permitidas'.
    """
    # Convertir nodos_terminales a conjunto (set) de forma segura
    if nodos_terminales is None:
        nodos_terminales_set = set()
    elif isinstance(nodos_terminales, (str, int)):
        nodos_terminales_set = {nodos_terminales}
    else:
        nodos_terminales_set = set(nodos_terminales)

    camino = [nodo_inicio]
    nodo_actual = nodo_inicio

    for _ in range(pasos_maximos - 1):
        vecinos = list(G.neighbors(nodo_actual))
        if not vecinos:
            break

        # Filtrar solo los vecinos cuyas categorías sean válidas para esta comida
        vecinos_validos = []
        for v in vecinos:
            # Si el vecino es el nodo final/terminal, siempre se permite para cerrar el recorrido
            if v in nodos_terminales_set:
                vecinos_validos.append(v)
            else:
                cat_vecino = G.nodes[v].get("categoria")
                # Permitir solo si no hay restricciones O la categoría está en la lista permitida
                if (
                    categorias_permitidas is None
                    or cat_vecino in categorias_permitidas
                ):
                    vecinos_validos.append(v)

        # Si no hay vecinos válidos según la regla, nos detenemos para evitar errores
        if not vecinos_validos:
            break

        # Elegimos el siguiente nodo de forma aleatoria solo entre los válidos
        siguiente_nodo = random.choice(vecinos_validos)
        camino.append(siguiente_nodo)

        # Si alcanzamos un nodo final, terminamos el recorrido
        if siguiente_nodo in nodos_terminales_set:
            break

        nodo_actual = siguiente_nodo

    return camino


# ------------------------------------------------------------------
# 2. FUNCION: generar_menu_aleatorio
# ------------------------------------------------------------------
def generar_menu_aleatorio(G, nodo_final):
    """Recorre las comidas del grafo y genera un random walk usando

    las categorías permitidas definidas en el JSON.
    """
    # 1. Obtener el mapa de categorías permitidas directamente del JSON
    reglas = extraer_reglas_desde_json()
    if G is None:
        st.write("El grafo es None. No se puede generar un menú aleatorio.")
        return None
    
    nodos = list(G.nodes())
    

    for nodo in nodos:
        categoria_tipo_comida = G.nodes[nodo].get("categoria")

        # Comprobar si la categoría del nodo está definida en las reglas (ej: "Desayuno", "Comida", "Snack")
        if categoria_tipo_comida in reglas:
            permitidas = reglas[categoria_tipo_comida]

            #st.write(f"**Nodo inicial ({categoria_tipo_comida}):** {nodo}")

            # Generar el recorrido filtrado por las categorías de la lista
            menu_aleatorio = generar_random_walk(
                G=G,
                nodo_inicio=nodo,
                pasos_maximos=15,
                nodos_terminales=nodo_final,
                categorias_permitidas=permitidas,  # <-- Se pasa la lista extraída del JSON
            )

            st.write(f"**Camino generado:** {menu_aleatorio}")