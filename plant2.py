import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("📊 시도별 식량작물 생산량 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)

    # 열 이름 확인 및 표준화 (한글 열이 문제가 될 수 있어서 영어로 정리)
    df.columns = [col.strip() for col in df.columns]

    # '시도', '연도', '생산량' 열이 있는지 확인
    required_columns = ["시도", "연도", "생산량"]
    if all(col in df.columns for col in required_columns):
        # 시도 선택
        selected_region = st.selectbox("시도를 선택하세요:", df["시도"].unique())

        # 선택한 시도의 데이터 필터링
        df_region = df[df["시도"] == selected_region]

        # 연도 순으로 정렬
        df_region = df_region.sort_values(by="연도")

        # 생산량 숫자형 변환
        df_region["생산량"] = pd.to_numeric(df_region["생산량"], errors="coerce")

        # 그래프 출력
        fig, ax = plt.subplots()
        ax.bar(df_region["연도"], df_region["생산량"], color='skyblue')
        ax.set_title(f"{selected_region}의 연도별 식량작물 생산량")
        ax.set_xlabel("연도")
        ax.set_ylabel("생산량 (톤)")
        st.pyplot(fig)

    else:
        st.error("⚠️ '시도', '연도', '생산량' 열이 데이터에 포함되어 있어야 합니다.")
