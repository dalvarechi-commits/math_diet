# dibujar un grafo con matplotlib
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

# crear un grafo desde una lista de adyacencia
def crear_grafo(adyacencia):
    G = nx.Graph()
    for nodo, vecinos in adyacencia.items():
        for vecino, peso in vecinos:
            if peso > 0:
                G.add_edge(nodo, vecino, weight=peso)
    return G

# dibujar el grafo
def dibujar_grafo(G):
    fig, ax = plt.subplots(figsize=(25, 25))
    pos = nx.spring_layout(G, weight='weight')
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
    edge_widths = [1 * w for w in edge_weights]
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color='lightblue',
        node_size=1400,
        font_size=8,
        font_weight='bold',
        width=edge_widths,
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