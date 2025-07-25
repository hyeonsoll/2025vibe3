import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()  # 열 이름 앞뒤 공백 제거
    return df

df = load_data()

# 실제 열 이름 출력
st.subheader("📌 데이터 열 목록")
st.write(df.columns.tolist())  # 사용자가 열 이름 확인 가능

# 사용자에게 필요한 열 확인을 요청 (자동 탐지 시도)
# 아래는 우리가 예상하는 열 이름 후보들
expected_columns = {
    "region": ["시도별", "지역", "시도"],
    "crop": ["작물", "품목"],
    "year": ["연도", "년도"],
    "amount": ["생산량 (톤)", "생산량", "정곡생산량"]
}

# 실제 열 이름 매핑
def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

region_col = find_column(expected_columns["region"])
crop_col = find_column(expected_columns["crop"])
year_col = find_column(expected_columns["year"])
amount_col = find_column(expected_columns["amount"])

# 열 존재 여부 확인
if None in [region_col, crop_col, year_col, amount_col]:
    st.error("❌ 필요한 열이 데이터에 존재하지 않습니다. 아래 열 중 하나가 있어야 합니다:")
    st.json(expected_columns)
    st.stop()

# 숫자형 변환
df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
df[year_col] = pd.to_numeric(df[year_col], errors="coerce", downcast="integer")

# 결측값 제거
df = df.dropna(subset=[region_col, crop_col, year_col, amount_col])

# UI
st.title("📊 식량작물 정곡 생산량 분석")
st.markdown("시도별 · 작물별 · 연도별 생산량 데이터를 Plotly로 시각화합니다.")

# 작물 선택
crop_options = df[crop_col].unique()
selected_crop = st.selectbox("🌾 작물을 선택하세요:", crop_options)

# 연도 슬라이더
min_year = int(df[year_col].min())
max_year = int(df[year_col].max())
selected_year_range = st.slider(
    "📆 연도 범위를 선택하세요:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# 필터링
filtered_df = df[
    (df[crop_col] == selected_crop) &
    (df[year_col] >= selected_year_range[0]) &
    (df[year_col] <= selected_year_range[1])
]

# 시각화
if not filtered_df.empty:
    fig = px.bar(
        filtered_df,
        x=year_col,
        y=amount_col,
        color=region_col,
        barmode="group",
        title=f"{selected_crop} - 시도별 생산량 변화 ({selected_year_range[0]}~{selected_year_range[1]})",
        labels={amount_col: "생산량 (톤)", year_col: "연도"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다.")

# 데이터 보기
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(filtered_df)
