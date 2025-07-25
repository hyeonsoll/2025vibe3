import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 생산량 분석", layout="wide")
st.title("🌾 식량작물 생산량 및 재배면적 시각화 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 생산량 CSV 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 데이터 정제
    df = df.iloc[1:].reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df = df.rename(columns={"시도별": "지역"})
    df = df[df["지역"].notna()]

    # 숫자형으로 변환
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip().replace("-", "0"), errors="coerce")

    # 작물 종류 추출
    col_map = {
        "미곡": ["미곡:면적 (ha)", "미곡:생산량 (톤)"],
        "맥류": ["맥류:면적 (ha)", "맥류:생산량 (톤)"],
        "잡곡": ["잡곡:면적 (ha)", "잡곡:생산량 (톤)"],
        "두류": ["두류:면적 (ha)", "두류:생산량 (톤)"],
        "서류": ["서류:면적 (ha)", "서류:생산량 (톤)"],
    }

    # 사용자 선택
    region = st.selectbox("📍 지역 선택", df["지역"].unique())
    crop = st.selectbox("🌿 작물 선택", list(col_map.keys()))
    metric = st.radio("📊 분석 항목", ["생산량 (톤)", "면적 (ha)"])
    chart_type = st.radio("📈 차트 유형", ["막대그래프", "선 그래프"])

    # 필터링
    col_label = col_map[crop][1] if "생산량" in metric else col_map[crop][0]
    chart_df = df[df["지역"] == region][["지역", col_label]].copy()
    chart_df["작물"] = crop
    chart_df["값"] = chart_df[col_label]

    # 시각화
    st.subheader(f"{region} - {crop} {metric} 분석")

    if chart_type == "막대그래프":
        fig = px.bar(chart_df, x="작물", y="값", color="작물", labels={"값": metric})
    else:
        fig = px.line(chart_df, x="작물", y="값", markers=True, labels={"값": metric})

    st.plotly_chart(fig, use_container_width=True)

    st.metric(f"{region} - {crop} 총 {metric}", f"{chart_df['값'].sum():,.0f}")
else:
    st.info("👆 상단에서 식량작물 CSV 파일을 업로드해주세요.")
