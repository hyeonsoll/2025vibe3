import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연도별 지역 작물 생산량 비교", layout="wide")
st.title("🌾 연도별 지역 작물 생산량 비교 대시보드")

# CSV 업로드
uploaded_file = st.file_uploader("📁 식량작물 CSV 업로드", type=["csv"])

if uploaded_file:
    raw_df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 헤더 정리
    new_columns = raw_df.iloc[0, 1:].tolist()
    new_columns.insert(0, "지역")
    df = raw_df.iloc[1:, :].reset_index(drop=True)
    df.columns = new_columns

    # 데이터 정제
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").str.replace("-", "0").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ▶ 연도 & 항목 추출
    melted_df = df.melt(id_vars="지역", var_name="연도_항목", value_name="값")
    melted_df["연도"] = melted_df["연도_항목"].str.extract(r'(20[0-9]{2})')
    melted_df["항목"] = melted_df["연도_항목"].str.extract(r':(.+)')
    melted_df.dropna(subset=["연도", "항목"], inplace=True)

    # 사용자 입력
    항목선택 = st.selectbox("🌿 분석할 작물 항목 선택", melted_df["항목"].unique(), index=0)

    # 필터링
    df_filtered = melted_df[melted_df["항목"] == 항목선택]
    df_filtered["연도"] = df_filtered["연도"].astype(str)

    # 그래프 출력
    st.subheader(f"📊 {항목선택} - 연도별 지역별 생산량 비교")
    fig = px.bar(
        df_filtered,
        x="연도",
        y="값",
        color="지역",
        barmode="group",
        title=f"{항목선택} - 연도별 지역별 생산량",
        labels={"값": "생산량 (톤)", "연도": "연도"},
    )
    fig.update_layout(
        xaxis=dict(type="category"),
        yaxis_title="생산량 (톤)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 CSV 파일을 업로드해주세요.")
