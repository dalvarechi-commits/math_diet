import networkx as nx
import matplotlib.pyplot as plt
import grafo


alimentos = grafo.cargar_alimentos(nombre_usuario="richi")
print(alimentos.keys())