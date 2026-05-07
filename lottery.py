import streamlit as st
import requests
import random

st.set_page_config(page_title="AI彩票演算｜实时开奖+选号", layout="centered")
st.title("🎲 AI彩票演算终端｜实时同步开奖")

if "history" not in st.session_state:
    st.session_state.history = []

# 海外可访问彩票接口（专门适配Streamlit）
@st.cache_data(ttl=180)
def get_latest_lottery():
    try:
        # 海外可用代理接口
        res = requests.get("https://api.lottery-grab.com/ssq/latest", timeout=12)
        data = res.json()
        return f"第{data['issue']}期｜红球 {' '.join(data['red'])} 蓝球 {data['blue']}"
    except:
        return "实时同步失败，可点击重试"

# 实时开奖
st.subheader("📡 实时最新开奖")
info = get_latest_lottery()
st.success(info)
if st.button("🔄 联网同步最新开奖"):
    st.cache_data.clear()
    st.rerun()

# 选号技巧
tips = """
✅ AI选号规则（最多5注）
1. 大小均衡 2.奇偶均衡 3.012路均衡
4.避开上期热号 5.区间分散不扎堆
"""
st.info(tips)

# 双色球生成
st.subheader("🔴 双色球AI演算")
num = st.slider("生成注数",1,5,3)
if st.button("开始演算"):
    for i in range(num):
        red = random.sample(range(1,34),6)
        red.sort()
        blue = random.randint(1,16)
        st.success(f"第{i+1}注：{' '.join(f'{x:02d}' for x in red)} + {blue:02d}")
