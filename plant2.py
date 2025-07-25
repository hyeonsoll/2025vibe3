import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 경로
csv_file = "식량작물_생산량_정곡__20250725135134.csv"

# CSV 파일 불러오기
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거
    return df

df = load_data(csv_file)

st.title("🌾 지역별 작물 생산량 시각화 (막대그래프)")
st.markdown("선택한 **지역**에서 작물별 **연도별 생산량**을 **막대그래프**로 시각화합니다.")

# 데이터 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 열 자동 탐색
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
category_cols = df.select_dtypes(include=['object']).columns.tolist()

# 설정: 컬럼 선택
st.sidebar.subheader("열 선택")
region_col = st.sidebar.selectbox("지역 열 선택", category_cols)
year_col = st.sidebar.selectbox("연도 열 선택", category_cols)
crop_col = st.sidebar.selectbox("작물 열 선택", category_cols)
value_col = st.sidebar.selectbox("생산량 열 선택", numeric_cols)

# 지역 선택
available_regions = df[region_col].dropna().unique().tolist()
selected_region = st.sidebar.selectbox("분석할 지역 선택", available_regions)

# 작물 선택
available_crops = df[crop_col].dropna().unique().tolist()
selected_crops = st.multiselect("시각화할 작물 선택", available_crops, default=available_crops[:3])

# 데이터 필터링
filtered_df = df[
    (df[region_col] == selected_region) &
    (df[crop_col].isin(selected_crops))
]

# 시각화
fig = px.bar(
    filtered_df,
    x=year_col,
    y=value_col,
    color=crop_col,
    barmode="group",
    labels={
        year_col: "연도",
        value_col: "생산량",
        crop_col: "작물"
    },
    title=f"{selected_region} 지역의 연도별 작물 생산량"
)

st.plotly_chart(fig, use_container_width=True)
