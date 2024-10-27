import streamlit as st
import pandas as pd
import numpy as np


class Advinador():
    def __init__(self):
        st.set_page_config(
            page_title="Adivinador",
            page_icon="🤔",
            layout='centered',
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.extremelycoolapp.com/help',
                'Report a bug': "https://www.extremelycoolapp.com/bug",
                'About': "# This is a header. This is an *extremely* cool app!"
            })
        st.title("Org. Y Arquitectura Del Computador - Adivinador 🤔")

    def generar_tablas(self, rango_inferior=1, rango_superior=100):
        df = pd.DataFrame()
        max_num = rango_superior
        num_tablas = max_num.bit_length()

        tablas = {f'Tabla {i + 1} (2^{i})': [] for i in range(num_tablas)}

        for num in range(rango_inferior, rango_superior - 1):
            for j in range(num_tablas):
                if (num & (1 << j)) != 0:
                    tablas[f'Tabla {j + 1} (2^{j})'].append(num)

        df_tablas = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in tablas.items()]))

        #for i in range(len(df_tablas.columns)):
        #   df["Columna1" + str(i)] = df_tablas[df_tablas.columns[i]].sample(frac=1).reset_index(drop=True)

        return df_tablas

    def adivinar_numero(self, df=pd.DataFrame):
        numero_adivinado = 0
        st.write("Responde a las siguientes preguntas:")

        with st.form("Responde a las siguientes preguntas:"):
            for i in range(len(df.columns)):
                columna = df[df.columns[i]]
                columna = columna.dropna()
                columna = columna.astype(int)
                columna = str(columna.tolist())
                st.write(columna)
                respuesta = st.radio(f"¿Está tu número en la lista {i + 1}?", options=["Sí", "No"], key=i)
                if respuesta == "Sí":
                    numero_adivinado += 2 ** i

            if st.form_submit_button("Advinar"):
                st.session_state.numero_resultado = numero_adivinado

    def aplicacion_principal(self):
        if "num1" not in st.session_state:
            st.session_state.num1 = ""
        if "num2" not in st.session_state:
            st.session_state.num2 = ""
        self.numero1 = st.session_state.num1
        self.numero2 = st.session_state.num2

        if self.numero1 and self.numero2:
            df2 = self.generar_tablas(int(self.numero1), int(self.numero2))
            if st.session_state.get('mostrar_formulario', False):
                self.adivinar_numero(df2)

            if 'numero_resultado' in st.session_state:
                st.write(f"Tu numero es el: {st.session_state.numero_resultado}")

    def run(self):
        st.divider()

        st.write("Seleccione El Rango de Números para jugar o inicie el juego")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(label="Número 1", key="num1", value=1)
        with col2:
            st.text_input(label="Número 2", key="num2", value=100)

        st.divider()
        st.write("Primero piense en un número, cuando esté listo inicie el juego")

        if st.button(label="Iniciar Juego ✅"):
            st.session_state.mostrar_formulario = True
            self.aplicacion_principal()
        elif st.session_state.get('mostrar_formulario', False):
            self.aplicacion_principal()


if __name__ == "__main__":
    app = Advinador()
    app.run()  
