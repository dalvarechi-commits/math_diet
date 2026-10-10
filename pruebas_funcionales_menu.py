import csv
import json
import statistics
from copy import deepcopy
from pathlib import Path

import pandas as pd

# Importamos la lógica de negocio sin arrancar Streamlit
import grafo
import menu


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "datos"
ADYACENCIA_PATH = ROOT / "m_adyacencia.csv"


class FakeSessionState(dict):
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, key, value):
        self[key] = value


def preparar_streamlit_fake():
    import streamlit as st

    st.session_state = FakeSessionState()
    st.write = lambda *args, **kwargs: None
    st.error = lambda *args, **kwargs: None
    st.success = lambda *args, **kwargs: None
    st.warning = lambda *args, **kwargs: None
    st.header = lambda *args, **kwargs: None
    st.subheader = lambda *args, **kwargs: None
    st.dataframe = lambda *args, **kwargs: None
    st.columns = lambda *args, **kwargs: [None]
    st.tabs = lambda *args, **kwargs: [None, None, None, None]
    st.button = lambda *args, **kwargs: False
    st.form = lambda *args, **kwargs: None
    st.text_input = lambda *args, **kwargs: ""
    st.multiselect = lambda *args, **kwargs: []
    st.slider = lambda *args, **kwargs: kwargs.get("value", 0)
    st.selectbox = lambda *args, **kwargs: kwargs.get("options", [None])[0]
    st.number_input = lambda *args, **kwargs: kwargs.get("value", 0)
    st.expander = lambda *args, **kwargs: None
    st.session_state.categorias = json.loads((DATA_DIR / "categorias.json").read_text(encoding="utf-8"))
    st.session_state.distribucion = json.loads((DATA_DIR / "distribucion.json").read_text(encoding="utf-8"))
    return st


def cargar_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalizar_alimentos(alimentos_base, perfil):
    alimentos = deepcopy(alimentos_base)

    for alimento_id, datos in alimentos.items():
        if not isinstance(datos, dict):
            continue

        valor_base = perfil.get("gustos", {}).get(alimento_id, 3)
        datos["valoracion_usuario"] = valor_base

        if "alergenos" not in datos:
            datos["alergenos"] = []

    if perfil.get("alergias"):
        alergias = set(perfil["alergias"])
        for alimento_id, datos in list(alimentos.items()):
            if not isinstance(datos, dict):
                continue
            if any(alergeno in datos.get("alergenos", []) for alergeno in alergias):
                del alimentos[alimento_id]

    return alimentos


def construir_usuario(perfil):
    datos = {
        "email": perfil["email"],
        "nombre": perfil["nombre"],
        "peso": perfil["peso"],
        "altura": perfil["altura"],
        "edad": perfil["edad"],
        "sexo": perfil["sexo"],
        "actividad_diaria": perfil["actividad_diaria"],
        "imc": round(perfil["peso"] / ((perfil["altura"] / 100) ** 2), 2),
        "tmb": perfil["tmb"],
        "GETD": perfil["GETD"],
        "objetivo": perfil["objetivo"],
        "objetivos": perfil["objetivo"],
        "preferencias": {"alergias": perfil.get("alergias", [])},
        "gustos": perfil.get("gustos", {}),
    }
    return datos


def asignar_categorias_nodos(G, alimentos, categorias):
    for nodo in list(G.nodes()):
        if nodo == "USUARIO":
            G.nodes[nodo]["categoria"] = "USUARIO"
            continue

        if "_" in nodo:
            prefijo, sufijo = nodo.split("_", 1)
            mapeo = {
                "Desayuno": "Desayuno",
                "Almuerzo": "Snack",
                "Comida": "Comida",
                "Merienda": "Snack",
                "Cena": "Comida",
            }
            G.nodes[nodo]["categoria"] = mapeo.get(sufijo, sufijo)
            continue

        if nodo in alimentos and isinstance(alimentos[nodo], dict):
            G.nodes[nodo]["categoria"] = alimentos[nodo].get("categoria")
            continue

        if nodo in categorias:
            G.nodes[nodo]["categoria"] = nodo

    return G


def generar_menu_perfil(perfil, run_id=1):
    base_alimentos = cargar_json(DATA_DIR / "alimentos.json")
    alimentos = normalizar_alimentos(base_alimentos, perfil)

    import streamlit as st
    st.session_state.alimentos_user = alimentos
    st.session_state.datos = construir_usuario(perfil)
    st.session_state.preferencias = {"alergias": perfil.get("alergias", [])}
    st.session_state.objetivo = perfil["objetivo"]
    st.session_state.gustos = perfil.get("gustos", {})
    st.session_state.distribucion = cargar_json(DATA_DIR / "distribucion.json")

    grafo.categorias = st.session_state.categorias

    adyacencia = grafo.cargar_adyacencia_desde_csv(str(ADYACENCIA_PATH))
    G_base = grafo.crear_grafo(adyacencia, alimentos, {"objetivos": perfil["objetivo"]})
    G_base = asignar_categorias_nodos(G_base, alimentos, st.session_state.categorias)
    G_personalizado = grafo.podarGrafo(G_base.copy(), alimentos, st.session_state.datos)
    G_personalizado = asignar_categorias_nodos(G_personalizado, alimentos, st.session_state.categorias)
    menu_aleatorio = grafo.generar_menu_aleatorio(G_personalizado, nodo_final="USARIO")

    if menu_aleatorio is None:
        raise ValueError(f"No se pudo generar menú para el perfil: {perfil['nombre']} en la ejecución {run_id}")

    df_menu = menu.calcular_cantidades_alimentos(menu_aleatorio, alimentos, st.session_state.datos, st.session_state.categorias)

    alimentos_unicos = sorted({alimento for datos in menu_aleatorio.values() for alimento in datos.get("alimentos", [])})
    gustos_usuario = perfil.get("gustos", {})
    gusto_medio = round(statistics.mean(gustos_usuario.values()), 2) if gustos_usuario else 0.0

    resultado = {
        "perfil": perfil["nombre"],
        "email": perfil["email"],
        "objetivo": perfil["objetivo"],
        "alergias": ";".join(perfil.get("alergias", [])) if perfil.get("alergias") else "ninguna",
        "gustos": json.dumps(gustos_usuario, ensure_ascii=False),
        "gustos_promedio": gusto_medio,
        "run": run_id,
        "nodos_generados": len(menu_aleatorio),
        "num_alimentos_unicos": len(alimentos_unicos),
        "alimentos_unicos": "; ".join(alimentos_unicos),
        "menu_json": json.dumps(menu_aleatorio, ensure_ascii=False),
        "tabla_json": json.dumps(df_menu.to_dict(orient="index"), ensure_ascii=False) if isinstance(df_menu, pd.DataFrame) else "{}",
    }

    return resultado


def perfiles_prueba():
    return [
        {
            "nombre": "Ana balanceada",
            "email": "ana@test.com",
            "objetivo": "mantener",
            "peso": 68,
            "altura": 170,
            "edad": 31,
            "sexo": "Mujer",
            "actividad_diaria": "Actividad moderada",
            "tmb": 1420,
            "GETD": 2200,
            "alergias": [],
            "gustos": {
                "260000": 5,
                "280000": 4,
                "289000": 5,
                "300000": 4,
                "900000": 5,
            },
        },
        {
            "nombre": "Luis pérdida de peso",
            "email": "luis@test.com",
            "objetivo": "perder",
            "peso": 85,
            "altura": 176,
            "edad": 34,
            "sexo": "Hombre",
            "actividad_diaria": "Poca actividad",
            "tmb": 1660,
            "GETD": 2100,
            "alergias": ["LAC", "GLU"],
            "gustos": {
                "260000": 4,
                "280000": 3,
                "289000": 5,
                "300000": 2,
                "900000": 4,
            },
        },
        {
            "nombre": "Marta vegana",
            "email": "marta@test.com",
            "objetivo": "ganar",
            "peso": 57,
            "altura": 165,
            "edad": 29,
            "sexo": "Mujer",
            "actividad_diaria": "Muy activo",
            "tmb": 1360,
            "GETD": 2400,
            "alergias": ["VEG"],
            "gustos": {
                "260000": 5,
                "280000": 5,
                "289000": 4,
                "300000": 3,
                "900000": 5,
            },
        },
        {
            "nombre": "Pablo con intolerancia",
            "email": "pablo@test.com",
            "objetivo": "mantener",
            "peso": 74,
            "altura": 178,
            "edad": 41,
            "sexo": "Hombre",
            "actividad_diaria": "Actividad moderada",
            "tmb": 1580,
            "GETD": 2300,
            "alergias": ["LAC", "FRU"],
            "gustos": {
                "260000": 5,
                "280000": 4,
                "289000": 4,
                "300000": 3,
                "900000": 5,
            },
        },
    ]


def exportar_csv(resultados, path):
    fieldnames = [
        "perfil",
        "email",
        "objetivo",
        "alergias",
        "gustos",
        "gustos_promedio",
        "run",
        "nodos_generados",
        "num_alimentos_unicos",
        "alimentos_unicos",
        "menu_json",
        "tabla_json",
    ]

    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fila in resultados:
            writer.writerow({k: fila.get(k, "") for k in fieldnames})


def generar_resumen_por_perfil(resultados):
    resumen = []
    por_perfil = {}

    for fila in resultados:
        perfil = fila["perfil"]
        por_perfil.setdefault(perfil, []).append(fila)

    for perfil, ejecuciones in por_perfil.items():
        nodos = [e["nodos_generados"] for e in ejecuciones]
        alimentos = [e["num_alimentos_unicos"] for e in ejecuciones]
        gustos_promedios = [e["gustos_promedio"] for e in ejecuciones]
        objetivos = {e["objetivo"] for e in ejecuciones}
        alergias = sorted({e["alergias"] for e in ejecuciones})
        gustos_global = json.loads(ejecuciones[0]["gustos"]) if ejecuciones else {}

        resumen.append(
            {
                "perfil": perfil,
                "objetivo": ", ".join(sorted(objetivos)),
                "alergias": "; ".join(alergias),
                "gustos": json.dumps(gustos_global, ensure_ascii=False),
                "gustos_promedio": round(statistics.mean(gustos_promedios), 2),
                "ejecuciones": len(ejecuciones),
                "media_nodos_generados": round(statistics.mean(nodos), 2),
                "min_nodos_generados": min(nodos),
                "max_nodos_generados": max(nodos),
                "media_alimentos_unicos": round(statistics.mean(alimentos), 2),
                "min_alimentos_unicos": min(alimentos),
                "max_alimentos_unicos": max(alimentos),
            }
        )

    return resumen


def guardar_resumen_csv(resumen, path):
    fieldnames = [
        "perfil",
        "objetivo",
        "alergias",
        "gustos",
        "gustos_promedio",
        "ejecuciones",
        "media_nodos_generados",
        "min_nodos_generados",
        "max_nodos_generados",
        "media_alimentos_unicos",
        "min_alimentos_unicos",
        "max_alimentos_unicos",
    ]

    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fila in resumen:
            writer.writerow({k: fila.get(k, "") for k in fieldnames})


def guardar_resultados(resultados):
    salida_json = ROOT / "resultados_pruebas_funcionales_10x.json"
    salida_csv = ROOT / "resultados_pruebas_funcionales_10x.csv"
    salida_summary = ROOT / "resumen_pruebas_funcionales_por_perfil.csv"

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    exportar_csv(resultados, salida_csv)
    resumen = generar_resumen_por_perfil(resultados)
    guardar_resumen_csv(resumen, salida_summary)

    print(f"\n[OK] JSON guardado en: {salida_json}")
    print(f"[OK] CSV guardado en: {salida_csv}")
    print(f"[OK] Resumen por perfil guardado en: {salida_summary}")
    return salida_json, salida_csv, salida_summary, resumen


def main():
    preparar_streamlit_fake()
    resultados = []

    for perfil in perfiles_prueba():
        print(f"\n=== Ejecutando 10 repeticiones para {perfil['nombre']} ===")
        for run_id in range(1, 11):
            resultado = generar_menu_perfil(perfil, run_id)
            resultados.append(resultado)
            print(f"  Run {run_id}: nodos={resultado['nodos_generados']}, alimentos={resultado['num_alimentos_unicos']}, gustos_promedio={resultado['gustos_promedio']}")

    _, _, _, resumen = guardar_resultados(resultados)

    print("\n=== Resumen por perfil ===")
    for fila in resumen:
        print(
            f"- {fila['perfil']}: media nodos={fila['media_nodos_generados']}, "
            f"media alimentos={fila['media_alimentos_unicos']}, gusto medio={fila['gustos_promedio']}, "
            f"ejecuciones={fila['ejecuciones']}"
        )

    print("\nPruebas funcionales completadas: 10 ejecuciones por perfil.")


if __name__ == "__main__":
    main()
