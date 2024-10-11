import streamlit as st
import pandas as pd
import time
from components.database import get_database
from components.historico import mostrar_historico
from components.historico import trocar_meses_para_portugues
from components.database import get_database
from components.page_configs import page_config, rerun_page

page_config()

mydb = get_database()

mostrar_historico(mydb)

rerun_page()