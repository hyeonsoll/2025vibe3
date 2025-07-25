import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("📊 시도별 식량작물 생산량 시각화")

# 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    # CSV 파일 읽기
    df = pd.read_csv(uploaded_file)

    # 열 이름 정리
    df.columns = [col.strip() for col in df.columns]

    # 필수 열 확인
    required_columns = ["시도", "연도", "생산량"]
    if all(col in df.columns for col in required_columns):
        # 시도 선택
        selected_region = st.selectbox("시도를 선택하세요:", sorted(df["시도"].unique()))

        # 선택한 시도만 필터링
        df_region = df[df["시도"] == selected_region]

        # 연도별 정렬 및 숫자 변환
        df_region["연도"] = pd.to_numeric(df_region["연도"], errors="coerce")
        df_region["생산량"] = pd.to_numeric(df_region["생산량"], errors="coerce")
        df_region = df_region.sort_values("연도")

        # Plotly 시각화
        fig = px.bar(df_region, x="연도", y="생산량",
                     title=f"{selected_region}의 연도별 식량작물 생산량",
                     labels={"연도": "연도", "생산량": "생산량 (톤)"},
                     color_discrete_sequence=["#58a6ff"])

        st.plotly_chart(fig)

    else:
        st.error("⚠️ '시도', '연도', '생산량' 열이 포함되어 있지 않습니다. 열 이름을 확인해주세요.")

