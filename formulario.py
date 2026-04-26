import streamlit as st

def mostrarFormulario():
    with st.form("my_form"):
        my_weight = st.slider('Pick a weight', 1, 200)
        st.form_submit_button('Submit my picks')

    st.write(my_weight)

     