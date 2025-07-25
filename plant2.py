import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 시도별 연도별 식량작물 생산량 시각화")

@st.cache_data
def load_data():
    return pd.read_csv("식량작물_생산량_정곡__20250725135134.csv", encoding='utf-8')

df = load_data()

# 열 이름 정의 (사용자 요청에 따라 변경)
region_col = "시도별"
year_col = "시점"
amount_col = "곡물 생산량(톤)"  # 실제 열 이름이 다를 경우 수정 필요

# 데이터 미리보기
st.subheader("📋 데이터 미리보기")
st.dataframe(df.head())

# 시도별 선택
regions = df[region_col].dropna().unique()
selected_region = st.selectbox("시도(지역)을 선택하세요", sorted(regions))

# 선택된 시도 데이터 필터링
df_filtered = df[df[region_col] == selected_region]

# 생산량 숫자형으로 변환
df_filtered[amount_col] = pd.to_numeric(df_filtered[amount_col], errors='coerce')
df_filtered = df_filtered.sort_values(by=year_col)

# 그래프 그리기 (Plotly 사용)
fig = px.bar(
    df_filtered,
    x=year_col,
    y=amount_col,
    title=f"{selected_region}의 연도별 생산량",
    labels={year_col: "연도", amount_col: "생산량 (톤)"},
    color_discrete_sequence=['#80b1d3']
)

st.plotly_chart(fig)
