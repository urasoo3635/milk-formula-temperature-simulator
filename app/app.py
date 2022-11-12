import streamlit as st
import numpy as np
import sympy as sym
import json
import os
import plotly.graph_objects as go

# パス
ROOT_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(ROOT_DIR, "./config/config.json")
ADVERTISEMENT_DIR_PATH = os.path.join(ROOT_DIR, "./advertisement")


def app():
     # 設定ファイルを読み込む
     with open(CONFIG_PATH) as f:
          cfg = json.load(f)

     st.title("調乳温度シミュレーション")
     st.markdown("ニュートンの冷却法則を用いて、調乳時のミルク温度の時間変化をシミュレーションします。", unsafe_allow_html=True)

     ht_dict = {"水道水かけ流し": 1.2e3, "貯めた水で冷却": 2.8e2, "扇風機で冷却": 50, "空気中に放置": 5}
     reikyaku = st.radio("冷却方法", options=list(ht_dict.keys()))
     around_temperature = st.number_input("冷媒の温度(℃) ※水温が不明な場合、水温＝気温で入力。", 0, 100, 30)
     milk_temperature = st.number_input("粉ミルクを溶かすお湯の温度(℃)", 0, 100, 70, step=5)
     hw_quality = st.number_input("お湯の量(ml)", 1, 500, 100, step=10) / 1000
     bin_quality = st.number_input("哺乳瓶の重さ(g) ※乳首除く", 10) / 1000
     bottle_r = st.number_input("哺乳瓶の半径(cm)", 1.0, 10.0, 3.0, step=0.5)
     bottle_r = bottle_r / 100
     bottle_h = st.number_input("ミルクの高さ(cm)", 1.0, 20.0, 5.0, step=0.5)
     bottle_h = bottle_h / 100

     hinetu_dict = {"ポリフェニルサルホン(PPSU) 970(j/kg*k)": 970,
                    "ガラス 677(j/kg*k)": 677,
                    "ホウケイ酸ガラス 830(j/kg*k)": 830,
                    "プラスチック 1500(j/kg*k)": 1500}

     col1_1, col1_2 = st.columns(2)

     with col1_1:
          hinetu_tuple = tuple(list(hinetu_dict.keys()) + ["その他"])
          hinetu_key = st.selectbox('哺乳瓶の比熱(j/(kg*k))', hinetu_tuple)

     if hinetu_key != "その他":
          hinetu = hinetu_dict[hinetu_key]
     else:
          hinetu = 0

     with col1_2:
          hinetu = st.number_input(label="", value=hinetu)

     col2_1, col2_2 = st.columns(2)

     ht = st.number_input("熱伝達率", value=ht_dict[reikyaku])
     st.markdown("※熱伝達率は代表的な値なので適宜調整してください。")
     ref_link_1 = '<a href="https://cattech-lab.com/science-tools/ht-forced/">平板の熱伝達率の計算(強制対流熱伝達)</a>'
     ref_link_2 = '<a href="https://cattech-lab.com/science-tools/ht-natural/">平板の熱伝達率の計算(自然対流熱伝達)</a>'
     st.markdown(ref_link_1, unsafe_allow_html=True)
     st.markdown(ref_link_2, unsafe_allow_html=True)


     # 計算
     WATER_HINETU = 4180
     surface_of_bottle = 2 * np.pi * bottle_r * (bottle_h + bottle_r) * 1
     shc = hw_quality * WATER_HINETU + bin_quality * hinetu
     k, t = sym.symbols("k t")
     formula = (milk_temperature - around_temperature) * sym.exp(-ht * surface_of_bottle / shc * t) + around_temperature

     # 冷却が止まる時間を算出
     tmp = milk_temperature
     time_ = 0
     while tmp > around_temperature:
          tmp = formula.subs([(t, time_)])
          tmp = np.round(float(tmp), 1)
          time_ += 1
          
          if time_ > cfg["graph"]["x_max"]:
               break

     sec = np.array([x for x in np.arange(0, time_, 1)])
     temperature = np.array([np.round(float(formula.subs([(t, s)])), 3) for s in sec])



     # グラフ表示
     fig = go.Figure()
     data = go.Scatter(x=sec, y=temperature, mode="lines", text=temperature)

     layout = go.Layout(xaxis={'title': '経過時間（秒）'},
                    yaxis={'title': '温度（℃）'},
                    title="調乳温度シミュレーション結果")

     fig = go.Figure(data, layout)
     fig.add_hline(y=40, line_color="red", line_width=1, line_dash="dash")
     st.plotly_chart(fig)

     st.markdown('##### スポンサードリンク', unsafe_allow_html=True)

     ad_list = os.listdir(ADVERTISEMENT_DIR_PATH)
     ad_list.sort()
     for fname in ad_list:
          fpath = os.path.join(ADVERTISEMENT_DIR_PATH, fname)

          try:
               with open(fpath, encoding='utf-8') as f:
                    ad = f.read()
          except Exception as e:
               print(e)
          else:
               st.markdown(ad, unsafe_allow_html=True)

     st.write("")
     st.write("")
     st.markdown('##### <font color="red">注意事項<font>', unsafe_allow_html=True)
     st.markdown("本サイトのシミュレーション結果に伴う事故について作成者は一切責任を負いません。")

     return

if __name__ == "__main__":
     app()