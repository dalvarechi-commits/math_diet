# dibujar un grafo con matplotlib
import csv
import json
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

'''
if "alimentos" not in st.session_state:
    # Cargamos el fichero JSON relativo a este archivo (repo_root/datos/alimentos.json)
    datos_path_default = Path(__file__).resolve().parent / "datos" / "alimentos.json"
    datos_path_user = Path(__file__).resolve().parent / "datos" / f"alimentos_{st.session_state.get('datos', {}).get('nombre', 'default')}.json"
       
    try:
        with datos_path_user.open("r", encoding="utf-8") as f:
            st.session_state.alimentos = json.load(f)
           
    except FileNotFoundError:
        #st.error(f"No se encontró el fichero de alimentos: {datos_path_user}. Se cargará el fichero por defecto: {datos_path_default}.")
        with datos_path_default.open("r", encoding="utf-8") as f:
            st.session_state.alimentos = json.load(f)
        # Simulación por si aún no creas el archivo
           
    except Exception as e:
        st.error(f"Error cargando {datos_path_default}: {e}")
        st.session_state.alimentos = {
            "251111": {"nombre_bedca": "Huevo de gallina entero", "categoria": "Huevos y derivados", "valoracion_usuario": 4.5},
            "295000": {"nombre_bedca": "Merluza fresca", "categoria": "Pescados y derivados", "valoracion_usuario": 4.0}
        }
    '''

if "categorias" not in st.session_state:
    # Cargamos el fichero JSON relativo a este archivo (repo_root/datos/categorias.json)
    categorias_path = Path(__file__).resolve().parent / "datos" / "categorias.json"
    with open(categorias_path, 'r', encoding='utf-8') as f:
        categorias = json.load(f)

# crear un grafo desde una lista de adyacencia
def crear_grafo(adyacencia):
    G = nx.DiGraph()
    for nodo, vecinos in adyacencia.items():
        for vecino, peso in vecinos:
            if peso > 0:
                G.add_edge(nodo, vecino, weight=peso)
    return G

def _normalizar_color(color):
    if not color:
        return 'lightgray'

    aliases = {
        'light red': 'lightcoral',
        'light yellow': 'khaki',
        'dark pink': 'deeppink',
        'light blue': 'lightskyblue',
        'lightgray': 'lightgray',
        'red': 'red',
        'yellow': 'yellow',
        'light green': 'lightgreen',
        'orange': 'orange',
        'light purple': 'cyan',
        'pink': 'pink',
    }
    return aliases.get(color.lower(), color)


# dibujar el grafo
def dibujar_grafo(G):
    fig, ax = plt.subplots(figsize=(25, 25))
    pos = nx.spring_layout(G, weight='weight', seed=50, k=1.8)
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
    edge_widths = [1 * w for w in edge_weights]
    # dibujamos los nodos con los colores de las categorías
    color_map = []
    for nodo in G.nodes():
        categoria = None
        # 1) buscar por el nombre exacto
        if nodo in st.session_state.alimentos:
            categoria = st.session_state.alimentos[nodo].get('categoria')
        else:
            # 2) buscar por coincidencia flexible (sin acentos, minúsculas)
            nodo_norm = ''.join(ch.lower() for ch in nodo if ch.isalnum())
            for alimento_id, alimento in st.session_state.alimentos.items():
                nombre_norm = ''.join(ch.lower() for ch in alimento.get('nombre_bedca', '') if ch.isalnum())
                if nodo_norm in nombre_norm or nombre_norm in nodo_norm:
                    categoria = alimento.get('categoria')
                    break

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
        min_source_margin=20,
        min_target_margin=20,
    )
    ax.set_axis_off()
    return fig

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


def pintarGrafo(m_adyacencia='m_adyacencia.csv'):
    adyacencia = cargar_adyacencia_desde_csv(m_adyacencia)
    G = crear_grafo(adyacencia)
    if len(G) == 0:
        return None
    return dibujar_grafo(G)


def cargar_adyacencia_desde_json(grafo_nodos_enlaces):
    with open(grafo_nodos_enlaces, 'r', encoding='utf-8') as archivo:
        adyacencia = json.load(archivo)
    return adyacencia    


