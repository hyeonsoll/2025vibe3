import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 지역별 연도 비교", layout="wide")
st.title("🌾 식량작물 연도별 생산량 및 면적 - 지역 간 비교")

# CSV 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 생산량 CSV 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 첫 행을 컬럼명으로 설정
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # '시도별' → '지역'으로 변경
    if "시도별" in df.columns:
        df = df.rename(columns={"시도별": "지역"})

    df = df[df["지역"].notna()]
    df = df[df["지역"] != "계"]

    # 숫자 처리
    for col in df.columns[1:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("-", "0")
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 작물-항목 맵
    col_map = {
        "미곡": ["미곡:면적 (ha)", "미곡:생산량 (톤)"],
        "맥류": ["맥류:면적 (ha)", "맥류:생산량 (톤)"],
        "잡곡": ["잡곡:면적 (ha)", "잡곡:생산량 (톤)"],
        "두류": ["두류:면적 (ha)", "두류:생산량 (톤)"],
        "서류": ["서류:면적 (ha)", "서류:생산량 (톤)"],
    }

    # 사용자 선택
    selected_regions = st.multiselect("📍 지역 선택", df["지역"].unique(), default=["서울특별시", "경기도"])
    crop = st.selectbox("🌿 작물 선택", list(col_map.keys()))
    metric = st.radio("📊 분석 항목", ["생산량 (톤)", "면적 (ha)"])

    # 선택한 열 이름
    col_label = col_map[crop][1] if "생산량" in metric else col_map[crop][0]

    # 연도 관련 컬럼 추출 (예: 2024.1 ~ 2024.11)
    year_cols = [col for col in df.columns if col.startswith("202")]

    # 비교용 데이터프레임 구성
    compare_list = []

    for region in selected_regions:
        row = df[df["지역"] == region]
        if row.empty:
            continue

        # 연도별 값만 추출 (long-form 변환)
        long_df = row[["지역"] + year_cols].melt(id_vars="지역", var_name="연도", value_name="값")
        long_df["값"] = pd.to_numeric(long_df["값"], errors="coerce")
        long_df["작물"] = crop
        compare_list.append(long_df)

    # 모든 지역 데이터 병합
    if compare_list:
        compare_df = pd.concat(compare_list, ignore_index=True)

        # 시각화
        st.subheader(f"📈 연도별 {crop} {metric} - 지역별 비교")
        fig = px.line(
            compare_df,
            x="연도",
            y="값",
            color="지역",
            markers=True,
            title=f"{crop} {metric} 연도별 추이 (지역별 비교)",
            labels={"값": metric}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠ 선택한 지역들에 대해 유효한 데이터가 없습니다.")
else:
    st.info("👆 CSV 파일을 업로드해주세요.")
