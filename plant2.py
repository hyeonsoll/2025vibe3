import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("📊 지역별 연도별 식량작물 생산량 시각화")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("식량작물_생산량_정곡__20250725135134.csv", encoding='utf-8')
    return df

df = load_data()

# 데이터 샘플 보기
st.subheader("🔍 데이터 미리보기")
st.dataframe(df.head())

# 자동으로 컬럼명 탐색
try:
    region_col = next(col for col in df.columns if '지역' in col or '시도' in col)
    year_col = next(col for col in df.columns if '연도' in col or '년도' in col)
    amount_col = next(col for col in df.columns if '생산량' in col or '생산' in col)
except StopIteration:
    st.error("⚠️ '지역', '연도', '생산량' 관련 열을 찾을 수 없습니다. CSV 파일 구조를 확인해주세요.")
    st.stop()

# 지역 선택
regions = df[region_col].dropna().unique()
selected_region = st.selectbox("지역을 선택하세요", sorted(regions))

# 선택된 지역 필터링
df_filtered = df[df[region_col] == selected_region]

# 생산량 숫자형으로 변환
df_filtered[amount_col] = pd.to_numeric(df_filtered[amount_col], errors='coerce')
df_filtered = df_filtered.sort_values(by=year_col)

# Plotly 그래프
fig = px.bar(
    df_filtered,
    x=year_col,
    y=amount_col,
    title=f"{selected_region}의 연도별 생산량",
    labels={year_col: "연도", amount_col: "생산량 (톤)"},
    color_discrete_sequence=['#66c2a5']
)

st.plotly_chart(fig)
