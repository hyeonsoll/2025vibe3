import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 경로
csv_file = "식량작물_생산량_정곡__20250725135134.csv"

# 데이터 불러오기
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거
    return df

df = load_data(csv_file)

st.title("🌽 지역별 작물 생산량 시각화 (막대그래프)")
st.markdown("선택한 **지역**에서 작물별 **연도별 생산량**을 시각화합니다.")

# 열 자동 분류
object_cols = df.select_dtypes(include='object').columns.tolist()
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# 유효성 검사
if not object_cols or not numeric_cols:
    st.error("데이터에 문자형 또는 숫자형 열이 없습니다. CSV 파일을 확인해주세요.")
    st.stop()

# 사이드바에서 열 지정
st.sidebar.subheader("⚙️ 열 선택")

region_col = st.sidebar.selectbox("지역 열", object_cols)
year_col = st.sidebar.selectbox("연도 열", object_cols)
crop_col = st.sidebar.selectbox("작물 열", object_cols)
value_col = st.sidebar.selectbox("생산량 열", numeric_cols)

# 지역 선택
regions = df[region_col].dropna().unique().tolist()
selected_region = st.sidebar.selectbox("지역 선택", regions)

# 작물 선택
crops = df[crop_col].dropna().unique().tolist()
selected_crops = st.multiselect("시각화할 작물 선택", crops, default=crops[:3] if len(crops) >= 3 else crops)

# 데이터 필터링
filtered_df = df[
    (df[region_col] == selected_region) &
    (df[crop_col].isin(selected_crops))
]

# 시각화
if filtered_df.empty:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
else:
    fig = px.bar(
        filtered_df,
        x=year_col,
        y=value_col,
        color=crop_col,
        barmode="group",
        labels={year_col: "연도", value_col: "생산량", crop_col: "작물"},
        title=f"📍 {selected_region} 지역의 연도별 작물 생산량"
    )
    st.plotly_chart(fig, use_container_width=True)
