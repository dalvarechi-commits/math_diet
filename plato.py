import streamlit as st
import plotly.graph_objects as go

def dibujar_plato():
    

    st.caption("Ajustado según los principios de la International Society of Sports Nutrition (ISSN) y Harvard.")

   
    sexo = st.session_state.datos.get("sexo", "Mujer")
    edad = st.session_state.datos.get("edad", 25)
    peso = st.session_state.datos.get("peso", 60.0)
    altura = st.session_state.datos.get("altura", 165)

    actividad = st.session_state.datos.get("actividad_diaria", "Sedentario (Poco o nada de ejercicio)")

    objetivo = st.session_state.datos.get("objetivo", "Mantener Peso")

 
    GETD = st.session_state.datos.get("GETD", 2400)  # Valor por defecto si no se encuentra

    # Lógica de Distribución Corregida
    if objetivo == "ganar":
        calorias = GETD * 1.10
        # Carbohidratos altos (35%) para glucógeno/fuerza + Proteína alta (30%)
        # Frutas y Verduras reducidas al 35% para no saciar en exceso
        secciones = {
            "Fuentes de Carbohidratos": 35,
            "Fuentes de Proteína": 30,
            "Verduras y hortalizas": 25,
            "Frutas y derivados": 10
        }
        g_prot_kg = 1.8
    elif objetivo == "perder":
        calorias = GETD * 0.80
        # Verduras + Frutas al 50% para saciedad + Proteína alta (30%) para proteger masa magra
        secciones = {
            "Verduras y hortalizas": 40,
            "Fuentes de Proteína": 30,
            "Fuentes de Carbohidratos": 20,
            "Frutas y derivados": 10
        }
        g_prot_kg = 1.4
    else:  # Mantener Peso
        calorias = GETD
        # Plato Harvard estándar (50% Frutas/Verduras, 25% Proteína, 25% Carbohidratos)
        secciones = {
            "Verduras y hortalizas": 35,
            "Fuentes de Proteína": 25,
            "Fuentes de Carbohidratos": 25,
            "Frutas y derivados": 15
        }
        g_prot_kg = 0.8

    gramos_proteina = peso * g_prot_kg
    colores = ["#2ECC71", "#E42E2E", "#E9E177", "#A367E7FF"]
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Metas Energéticas y de Macronutrientes")
        st.metric("Gasto Calórico Estimado (GETD)", f"{round(GETD)} kcal")
        st.metric("Calorías Diarias Objetivo", f"{round(calorias)} kcal", delta=f"{round(calorias - GETD)} kcal")
        
        st.subheader("Ingesta Proteica Recomendada")
        st.metric("Proteína Diaria", f"{round(gramos_proteina)} g", delta=f"{g_prot_kg} g/kg peso")


    with col2:
        st.subheader("Distribución del Plato")
        
        fig = go.Figure()

        # Borde exterior simulando vajilla de loza
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=-1.1, y0=-1.1, x1=1.1, y1=1.1,
            line=dict(color="#BDC3C7", width=14),
            fillcolor="#FAF9F6", 
            layer="below"
        
        )

        # Borde interior del plato
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=-0.98, y0=-0.98, x1=0.98, y1=0.98,
            line=dict(color="#D0D3D4", width=2), 
            layer="below"
        )

        # Graficar sectores
        
        fig.add_trace(go.Pie(
            labels=list(secciones.keys()),
            values=list(secciones.values()),
            marker=dict(colors=colores, line=dict(color='#FFFFFF', width=3)),
            textinfo='label+percent',
            hoverinfo='label+percent',
            hole=0.0,
            domain=dict(x=[0.10, 0.90], y=[0.10, 0.90]),
            sort=False
        ))

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(t=20, b=20, l=20, r=20),
            height=620,
            width=480,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

