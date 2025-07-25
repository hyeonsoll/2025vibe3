import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
df_raw = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv")

# 첫 번째 행 제거 및 컬럼 정리
df = df_raw.drop(index=0)
df.columns = ['시도별'] + list(range(1998, 2025))

# 숫자로 변환
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Streamlit 앱 시작
st.set_page_config(page_title="시도별 미곡 생산량 분석", layout="wide")
st.title("🌾 시도별 미곡 생산량 분석 (1998–2024)")

# 시도 선택
regions = df['시도별'].unique().tolist()
selected_region = st.selectbox("🔍 시도를 선택하세요:", regions)

# 선택된 시도 데이터 추출
df_region = df[df['시도별'] == selected_region].set_index('시도별').T
df_region.columns = ['미곡 생산량 (톤)']
df_region = df_region.reset_index().rename(columns={'index': '연도'})

# 시각화
fig = px.bar(df_region, x='연도', y='미곡 생산량 (톤)',
             title=f"{selected_region} 연도별 미곡 생산량 변화",
             labels={"연도": "연도", "미곡 생산량 (톤)": "생산량 (톤)"})

st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블
with st.expander("📊 데이터 보기"):
    st.dataframe(df_region)
