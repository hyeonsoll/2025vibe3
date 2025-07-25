import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()
    # 숫자형 변환
    df["생산량 (톤)"] = pd.to_numeric(df["생산량 (톤)"], errors="coerce")
    df["연도"] = pd.to_numeric(df["연도"], errors="coerce", downcast="integer")
    df = df.dropna(subset=["시도별", "작물", "연도", "생산량 (톤)"])
    return df

df = load_data()

# UI
st.title("📊 식량작물 정곡 생산량 분석")
st.markdown("시도별 · 작물별 · 연도별 생산량 데이터를 Plotly로 시각화합니다.")

# 유효성 검사
required_columns = {'시도별', '작물', '연도', '생산량 (톤)'}
if not required_columns.issubset(df.columns):
    st.error(f"데이터에 다음 열이 필요합니다: {required_columns}")
    st.dataframe(df.head())
    st.stop()

# 작물 선택
crop_options = df['작물'].unique()
selected_crop = st.selectbox("🌾 작물을 선택하세요:", crop_options)

# 연도 슬라이더
min_year, max_year = int(df['연도'].min()), int(df['연도'].max())
selected_year_range = st.slider(
    "📆 연도 범위를 선택하세요:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# 필터링
filtered_df = df[
    (df["작물"] == selected_crop) &
    (df["연도"] >= selected_year_range[0]) &
    (df["연도"] <= selected_year_range[1])
]

# 시각화
if not filtered_df.empty:
    fig = px.bar(
        filtered_df,
        x="연도",
        y="생산량 (톤)",
        color="시도별",
        barmode="group",
        title=f"{selected_crop} - 시도별 생산량 변화 ({selected_year_range[0]}~{selected_year_range[1]})",
        labels={"생산량 (톤)": "생산량 (톤)", "연도": "연도"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다.")

# 데이터 보기
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(filtered_df)
