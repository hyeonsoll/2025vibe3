import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("📊 지역별 연도별 식량작물 생산량 시각화")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("식량작물_생산량_정곡__20250725135134.csv", encoding='utf-8')
    return df

df = load_data()

# 열 이름 확인
st.write("데이터 샘플")
st.dataframe(df.head())

# 필요한 열 자동 필터링 (예: 지역, 연도, 생산량이 포함된 열 찾기)
try:
    # '지역' 또는 '시도' 같은 지역 컬럼 탐색
    region_col = next(col for col in df.columns if '지역' in col or '시도' in col)
    year_col = next(col for col in df.columns if '연도' in col or '년도' in col)
    amount_col = next(col for col in df.columns if '생산량' in col or '생산' in col)
except StopIteration:
    st.error("⚠️ '지역', '연도', '생산량' 관련 열을 찾을 수 없습니다. CSV 파일 구조를 확인해주세요.")
    st.stop()

# 지역 선택
regions = df[region_col].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 선택된 지역 데이터 필터링
df_filtered = df[df[region_col] == selected_region]

# 연도 순으로 정렬
df_filtered = df_filtered.sort_values(by=year_col)

# 생산량이 숫자형인지 확인
df_filtered[amount_col] = pd.to_numeric(df_filtered[amount_col], errors='coerce')

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df_filtered[year_col].astype(str), df_filtered[amount_col], color='skyblue')
ax.set_title(f"{selected_region} 연도별 생산량")
ax.set_xlabel("연도")
ax.set_ylabel("생산량 (톤)")
plt.xticks(rotation=45)
st.pyplot(fig)
