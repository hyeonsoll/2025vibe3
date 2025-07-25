import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()  # 컬럼명 공백 제거
    return df

df = load_data()

# 기본 확인
st.title("📊 식량작물 정곡 생산량 분석")
st.markdown("시도별 · 작물별 · 연도별 생산량 데이터를 Plotly로 시각화합니다.")

# 유효한 컬럼 확인
if not {'시도별', '작물', '연도', '생산량 (톤)'}.issubset(df.columns):
    st.error("데이터에 '시도별', '작물', '연도', '생산량 (톤)' 열이 포함되어 있어야 합니다.")
    st.dataframe(df.head())
    st.stop()

# 사용자 입력
crop_options = df['작물'].unique()
selected_crop = st.selectbox("작물을 선택하세요:", crop_options)

# 필터링
filtered_df = df[df['작물'] == selected_crop]

# 시각화
fig = px.bar(
    filtered_df,
    x="연도",
    y="생산량 (톤)",
    color="시도별",
    barmode="group",
    title=f"{selected_crop} - 시도별 연도 생산량",
    labels={"생산량 (톤)": "생산량 (톤)", "연도": "연도"}
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 보기
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(filtered_df)
