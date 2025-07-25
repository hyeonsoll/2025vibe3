import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 시도별 미곡 생산량 비교")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 열 이름 공백 제거
    df.columns = [col.strip() for col in df.columns]

    # 열 이름 바꾸기 (사용자 요청대로)
    df = df.rename(columns={
        "시도": "시도별",
        "생산량": "미곡:생산량 (톤)"
    })

    # 필요한 열만 사용
    if "시도별" in df.columns and "미곡:생산량 (톤)" in df.columns:
        # 시도 선택
        selected_region = st.selectbox("시도별을 선택하세요:", sorted(df["시도별"].unique()))

        # 해당 시도 데이터 필터링
        df_filtered = df[df["시도별"] == selected_region]

        # 생산량 숫자형 변환
        df_filtered["미곡:생산량 (톤)"] = pd.to_numeric(df_filtered["미곡:생산량 (톤)"], errors="coerce")

        # index 기준으로 나열 (연도 제거 요청이므로 x축을 index로)
        df_filtered = df_filtered.reset_index()

        fig = px.bar(df_filtered,
                     x=df_filtered.index,
                     y="미곡:생산량 (톤)",
                     title=f"{selected_region}의 미곡 생산량 비교",
                     labels={"index": "항목 순서", "미곡:생산량 (톤)": "미곡:생산량 (톤)"},
                     color_discrete_sequence=["#58a6ff"])

        st.plotly_chart(fig)
    else:
        st.error("⚠️ '시도별' 또는 '미곡:생산량 (톤)' 열이 존재하지 않습니다.")
