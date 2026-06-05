# dibujar un grafo con matplotlib

import matplotlib.pyplot as plt
import networkx as nx
# crear un grafo desde una lista de adyacencia
def crear_grafo(adyacencia):
    G = nx.Graph()
    for nodo, vecinos in adyacencia.items():
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
    return G

# dibujar el grafo
def dibujar_grafo(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=16, font_weight='bold')
    plt.show()


#generar adyacencia desde .csv
import csv
def cargar_adyacencia_desde_csv(m_adyacencia):
    adyacencia = {}
    with open(m_adyacencia, 'r') as archivo:
        lector = csv.reader(archivo)
        header = next(lector)  # Leer encabezado
        node_names = header[1:]  # Nombres de nodos desde la segunda columna
        for fila in lector:
            nodo = fila[0]
            valores = fila[1:]
            vecinos = []
            for i, val in enumerate(valores):
                if val == '1':
                    vecinos.append(node_names[i])
            adyacencia[nodo] = vecinos
    return adyacencia