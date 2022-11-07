import streamlit as st
import numpy as np


st.title("調乳温度シミュレーション")

baitai = st.radio(
     "冷媒を選んでください。",
     ('水', '空気'))

around_temperature = st.number_input("冷媒の温度", 0, 100, 30)
milk_temperature = st.number_input("粉ミルクを溶かすお湯の温度", 0, 100, 70)

# 式


