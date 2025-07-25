import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")

st.title("📊 2025년 6월 연령별 인구 현황 (전국)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')

    # '전국' 데이터만 추출
    national_data = df[df['행정구역'].str.contains("전국")]

    # 연령별 컬럼 추출
    male_cols = [col for col in df.columns if "2025년06월_남_" in col and "총인구수" not in col and "연령구간인구수" not in col]
    female_cols = [col for col in df.columns if "2025년06월_여_" in col and "총인구수" not in col and "연령구간인구수" not in col]

    # 연령 숫자 추출
    def parse_age(col_name):
        last = col_name.split("_")[-1]
        if "이상" in last:
            return 100
        return int(last.replace("세", ""))

    ages = [parse_age(col) for col in male_cols]

    # 값 정리
    male_pop = national_data[male_cols].iloc[0].str.replace(",", "").fillna("0").astype(int)
    female_pop = national_data[female_cols].iloc[0].str.replace(",", "").fillna("0").astype(int)

    # 데이터프레임 구성
    data = pd.DataFrame({
        "연령": ages + ages,
        "성별": ["남"] * len(ages) + ["여"] * len(ages),
        "인구수": list(male_pop) + list(female_pop)
    })

    # Plotly 시각화
    fig = px.line(
        data, x="연령", y="인구수", color="성별", markers=True,
        title="2025년 6월 연령별 인구 그래프 (전국)",
        labels={"연령": "나이", "인구수": "인구 수"}
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 좌측 상단 또는 위에 CSV 파일을 업로드하세요.")
