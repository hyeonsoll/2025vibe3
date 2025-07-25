import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()
    df_melted = df.melt(id_vars=["시도별"], var_name="연도", value_name="생산량")
    df_melted["생산량"] = pd.to_numeric(df_melted["생산량"], errors="coerce")
    df_melted["연도"] = pd.to_numeric(df_melted["연도"], errors="coerce")
    df_melted = df_melted.dropna(subset=["시도별", "연도", "생산량"])
    return df_melted

df = load_data()

st.title("🌾 미곡 생산량 시도별 변화")
st.markdown("CSV 파일을 연도별로 변환하여 시도별 생산량 추이를 시각화합니다.")

# 연도 슬라이더
min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

selected_years = st.slider(
    "📆 연도 범위 선택:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 시도 멀티셀렉트 필터
all_regions = sorted(df["시도별"].unique())
selected_regions = st.multiselect(
    "📍 시도 선택:",
    options=all_regions,
    default=all_regions  # 기본값은 전체 선택
)

# 필터링
filtered_df = df[
    (df["연도"] >= selected_years[0]) &
    (df["연도"] <= selected_years[1]) &
    (df["시도별"].isin(selected_regions))
]

# 시각화
if not filtered_df.empty:
    fig = px.bar(
        filtered_df,
        x="연도",
        y="생산량",
        color="시도별",
        barmode="group",
        title=f"시도별 미곡 생산량 변화 ({selected_years[0]}~{selected_years[1]})",
        labels={"생산량": "생산량 (톤)", "연도": "연도"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("해당 조건에 맞는 데이터가 없습니다.")

# 데이터 보기
with st.expander("📋 데이터 보기"):
    st.dataframe(filtered_df)
