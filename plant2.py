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

st.title("🌾 식량작물 정곡 생산량 시각화 (막대그래프)")
st.markdown("업로드된 데이터를 기반으로 작물별 **생산량**을 연도별로 **막대그래프**로 시각화합니다.")

# 데이터 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 열 자동 탐색
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
category_cols = df.select_dtypes(include=['object']).columns.tolist()

# 설정
st.sidebar.subheader("시각화 설정")
year_col = st.sidebar.selectbox("연도 열 선택", category_cols)
crop_col = st.sidebar.selectbox("작물 열 선택", category_cols)
value_col = st.sidebar.selectbox("생산량 열 선택", numeric_cols)

# 작물 선택
available_crops = df[crop_col].unique().tolist()
selected_crops = st.multiselect("시각화할 작물을 선택하세요", available_crops, default=available_crops[:3])

# 데이터 필터링
filtered_df = df[df[crop_col].isin(selected_crops)]

# 막대그래프 시각화
fig = px.bar(
    filtered_df,
    x=year_col,
    y=value_col,
    color=crop_col,
    barmode="group",
    labels={year_col: "연도", value_col: "생산량", crop_col: "작물"},
    title="연도별 작물 생산량 (막대그래프)"
)

st.plotly_chart(fig, use_container_width=True)
