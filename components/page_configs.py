import streamlit as st
import time

def page_config():
    st.set_page_config(
        page_title="Monitoramento de Higiene Stihl",
        page_icon="🖥️",
        layout="wide",
    )


def rerun_page():
    TEMPO = 10  # 10s eh pouco tempo, o que gasta bastante memoria do pc. Em fase final, mudar para cada 1min

    time.sleep(TEMPO)
    st.rerun()