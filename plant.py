import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 생산량 분석", layout="wide")
st.title("🌾 식량작물 생산량 및 재배면적 시각화 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 생산량 CSV 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # ✅ 첫 행이 컬럼명이 아니므로 컬럼명 수동 지정
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # ✅ '시도별' 컬럼명 정리
    if "시도별" in df.columns:
        df = df.rename(columns={"시도별": "지역"})
    elif "지역" not in df.columns:
        st.error("❌ '시도별' 또는 '지역' 컬럼이 존재하지 않습니다.")
        st.stop()

    # ✅ 지역 컬럼만 추출
    df = df[df["지역"].notna()]
    df = df[df["지역"] != "계"]

    # ✅ 모든 값 숫자 변환 (면적/생산량)
    for col in df.columns[1:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("-", "0")
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 작물 매핑 정의
    col_map = {
        "미곡": ["미곡:면적 (ha)", "미곡:생산량 (톤)"],
        "맥류": ["맥류:면적 (ha)", "맥류:생산량 (톤)"],
        "잡곡": ["잡곡:면적 (ha)", "잡곡:생산량 (톤)"],
        "두류": ["두류:면적 (ha)", "두류:생산량 (톤)"],
        "서류": ["서류:면적 (ha)", "서류:생산량 (톤)"],
    }

    # 사용자 선택 영역
    region = st.selectbox("📍 지역 선택", df["지역"].unique())
    crop = st.selectbox("🌿 작물 선택", list(col_map.keys()))
    metric = st.radio("📊 분석 항목", ["생산량 (톤)", "면적 (ha)"])
    chart_type = st.radio("📈 차트 유형", ["막대그래프", "선 그래프"])

    # 분석용 컬럼 추출
    col_label = col_map[crop][1] if "생산량" in metric else col_map[crop][0]

    # 시각화용 데이터프레임 생성
    value = df[df["지역"] == region][col_label].values[0]
    chart_df = pd.DataFrame({
        "작물": [crop],
        "값": [value],
    })

    # 그래프 출력
    st.subheader(f"📊 {region} 지역 - {crop} {metric} 분석")

    if chart_type == "막대그래프":
        fig = px.bar(chart_df, x="작물", y="값", color="작물", labels={"값": metric})
    else:
        fig = px.line(chart_df, x="작물", y="값", markers=True, labels={"값": metric})

    st.plotly_chart(fig, use_container_width=True)

    st.metric(f"총 {metric} ({region} - {crop})", f"{value:,.0f}")

else:
    st.info("👆 CSV 파일을 업로드해주세요.")
