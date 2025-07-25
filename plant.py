import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 생산량 분석", layout="wide")
st.title("🌾 식량작물 생산량 및 재배면적 시각화 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 생산량 CSV 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # ✅ 첫 행을 컬럼명으로 사용
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # ✅ '시도별' → '지역'으로 이름 변경
    if "시도별" in df.columns:
        df = df.rename(columns={"시도별": "지역"})
    elif "지역" not in df.columns:
        st.error("❌ '시도별' 또는 '지역' 컬럼이 없습니다.")
        st.stop()

    # ✅ 지역 데이터 필터링
    df = df[df["지역"].notna()]
    df = df[df["지역"] != "계"]

    # 숫자 변환
    for col in df.columns[1:]:
        df[col] = (
            df[col].astype(str)
            .str.replace(",", "")
            .str.replace("-", "0")
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 작물 매핑
    col_map = {
        "미곡": ["미곡:면적 (ha)", "미곡:생산량 (톤)"],
        "맥류": ["맥류:면적 (ha)", "맥류:생산량 (톤)"],
        "잡곡": ["잡곡:면적 (ha)", "잡곡:생산량 (톤)"],
        "두류": ["두류:면적 (ha)", "두류:생산량 (톤)"],
        "서류": ["서류:면적 (ha)", "서류:생산량 (톤)"],
    }

    # 사용자 입력
    region = st.selectbox("📍 지역 선택", df["지역"].unique())
    crop = st.selectbox("🌿 작물 선택", list(col_map.keys()))
    metric = st.radio("📊 분석 항목", ["생산량 (톤)", "면적 (ha)"])
    chart_type = st.radio("📈 차트 유형", ["막대그래프", "선 그래프"])

    # 분석할 컬럼
    col_label = col_map[crop][1] if "생산량" in metric else col_map[crop][0]

    # 선택된 지역 데이터
    region_row = df[df["지역"] == region].copy()

    # ----------------------------
    # 1) 선택 작물 단일 그래프
    # ----------------------------
    value = region_row[col_label].values[0]
    chart_df = pd.DataFrame({"작물": [crop], "값": [value]})

    st.subheader(f"📊 {region} 지역 - {crop} {metric} 분석")
    if chart_type == "막대그래프":
        fig = px.bar(chart_df, x="작물", y="값", color="작물", labels={"값": metric})
    else:
        fig = px.line(chart_df, x="작물", y="값", markers=True, labels={"값": metric})
    st.plotly_chart(fig, use_container_width=True)
    st.metric(f"총 {metric} ({region} - {crop})", f"{value:,.0f}")

    # ----------------------------
    # 2) 연도별 생산량 추이 그래프
    # ----------------------------
    st.subheader(f"📈 {region} 지역 - {crop} 연도별 {metric} 추이")

    # 연도별 데이터 추출 (2024, 2024.1, 2024.2 ...)
    year_cols = [col for col in df.columns if col.startswith("2024")]
    crop_cols = [c for c in year_cols if col_label.split(":")[0] in df.iloc[0].values]

    # 해당 작물의 연도 데이터 변환
    crop_year_data = region_row[year_cols].T.reset_index()
    crop_year_data.columns = ["연도", "값"]
    crop_year_data["값"] = pd.to_numeric(crop_year_data["값"], errors="coerce")

    # 시각화
    fig_line = px.line(crop_year_data, x="연도", y="값", markers=True, title=f"{region} - {crop} 연도별 {metric} 추이")
    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("👆 CSV 파일을 업로드해주세요.")
