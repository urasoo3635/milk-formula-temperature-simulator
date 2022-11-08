import streamlit as st
import numpy as np
import sympy as sym

st.title("調乳温度シミュレーション")

baitai = st.radio(
     "冷媒を選んでください。",
     ('流水', '空気'))

around_temperature = st.number_input("冷媒の温度　※水温が不明な場合、水温＝気温で入力。", 0, 100, 30)
milk_temperature = st.number_input("粉ミルクを溶かすお湯の温度", 0, 100, 70)
# bottle_r = st.number_input("哺乳瓶の半径(cm)", 1, 10)
# bottle_r = bottle_r / 100
bottle_h = st.number_input("ミルクの高さ(cm)", 1, 20, 5)
bottle_h = bottle_h / 100

if baitai == "流水":
     heat_transfer_coef = 4.3e2
elif baitai == "空気":
     delta_temperature = milk_temperature - around_temperature
     heat_transfer_coef = 2.51 * 0.55 * (delta_temperature / bottle_h)**(25/100)

st.write(f"{baitai}の熱伝達率: {np.round(heat_transfer_coef, 3)}")
st.write("※流水の熱伝達率は計算が困難なため取り得る範囲の中央値としています。")

k, t = sym.symbols("k t")
formula = (milk_temperature - around_temperature) * sym.exp(k * t) + around_temperature





