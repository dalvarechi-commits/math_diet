#import grafo
import streamlit as st
import json
from pathlib import Path


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
"""



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
    for alimento1 in alimentos.items():
        if alimento1.get('categoria') == alimento.get('categoria'):
            nalimentos_por_cat= nalimentos_por_cat + 1
    

    if nalimentos_por_cat == 0: #Esto no debería pasar porque alimento está en la lista de alimentos.
        st.warning(f"No se encontraron alimentos en la categoría '{alimento.get('categoria')}'.")
        return 0
    peso_personalizado = alimento.get('peso')*distribucion.get(alimento.get('categoria'))/nalimentos_por_cat
    st.write(f"Peso calculado para {alimento}:{peso_personalizado}")
    return peso_personalizado