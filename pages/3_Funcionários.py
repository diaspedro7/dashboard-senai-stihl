import streamlit as st
import pandas as pd
import plotly.express as px
import time
from components.historico import trocar_meses_para_portugues
from components.funcionarios import mostrar_funcionarios
from components.database import get_database
from components.page_configs import page_config, rerun_page

page_config()

mydb = get_database()

mostrar_funcionarios(mydb)

rerun_page()