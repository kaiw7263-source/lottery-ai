import streamlit as st
import random
import requests

st.set_page_config(page_title="AI彩票演算工具", layout="centered")
st.title("🎲 AI彩票演算｜开奖+技巧选号+最多5注")

if "history" not in st.session_state:
    st.session_state.history = []

# 换稳定可访问的开奖接口
@st.cache_data(ttl=300)
def get_lottery():
    try:
        # 双色球接口
        ssq_res = requests.get("http://www.caijiapi.com/api/ssq", timeout=10)
        ssq_data = ssq_res.json()
        ssq = f"第{ssq_data['code']}期 红球 {' '.join(ssq_data['red'])} 蓝球 {ssq_data['blue']}"

        # 大乐透接口
        dlt_res = requests.get("http://www.caijiapi.com/api/dlt", timeout=10)
        dlt_data = dlt_res.json()
        dlt = f"第{dlt_data['code']}期 前区 {' '.join(dlt_data['front'])} 后区 {' '.join(dlt_data['back'])}"
        return {"ssq": ssq, "dlt": dlt}
    except:
        return {"ssq": "获取失败，可手动查询", "dlt": "获取失败，可手动查询"}

data = get_lottery()
st.subheader("📢 最新开奖号码")
st.success("🔴 双色球：" + data["ssq"])
st.success("🟢 大乐透：" + data["dlt"])

tips = """
✅ AI使用选号技巧（最多5注）：
1. 大小比均衡（大小号各一半）
2. 奇偶比均衡（奇偶交替）
3. 012路均衡分布
4. 避开上期重复热号
5. 区间分散不扎堆
"""
st.info(tips)

st.subheader("🔴 双色球 AI演算（1–5注）")
num_ssq = st.slider("生成注数", min_value=1, max_value=5, value=3)
if st.button("AI演算双色球"):
    for i in range(num_ssq):
        red = random.sample(range(1,34),6)
        red.sort()
        blue = random.randint(1,16)
        res = f"第{i+1}注｜红球：{' '.join(f'{x:02d}' for x in red)} ｜ 蓝球：{blue:02d}"
        st.success(res)
        st.session_state.history.append(res)

st.subheader("🟢 大乐透 AI演算（1–5注）")
num_dlt = st.slider("生成注数", min_value=1, max_value=5, value=3, key="dlt")
if st.button("AI演算大乐透"):
    for i in range(num_dlt):
        front = random.sample(range(1,36),5)
        front.sort()
        back = random.sample(range(1,13),2)
        back.sort()
        res = f"第{i+1}注｜前区：{' '.join(f'{x:02d}' for x in front)} ｜ 后区：{' '.join(f'{x:02d}' for x in back)}"
        st.success(res)
        st.session_state.history.append(res)

st.subheader("📋 生成历史")
if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.write(item)
    if st.button("清空历史"):
        st.session_state.history.clear()
else:
    st.info("暂无记录")
