import grafo
import streamlit as st


"""alimentos = grafo.cargar_alimentos(nombre_usuario="richi")
print(alimentos.keys())"""

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

