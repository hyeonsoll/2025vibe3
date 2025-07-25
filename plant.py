import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 연도별 지역 비교", layout="wide")
st.title("🌾 식량작물 생산량 및 재배면적 - 지역 간 연도별 비교 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 생산량 CSV 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # ✅ 첫 행을 컬럼명으로 설정
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # ✅ 컬럼명 정리
    if "시도별" in df.columns:
        df = df.rename(columns={"시도별": "지역"})
    elif "지역" not in df.columns:
        st.error("❌ '시도별' 또는 '지역' 컬럼이 없습니다.")
        st.stop()

    df = df[df["지역"].notna()]
    df = df[df["지역"] != "계"]

    # 숫자형으로 변환
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
    selected_regions = st.multiselect("📍 비교할 지역을 선택하세요", options=df["지역"].unique(), default=["서울특별시", "경기도"])
    crop = st.selectbox("🌿 작물 선택", list(col_map.keys()))
    metric = st.radio("📊 분석 항목", ["생산량 (톤)", "면적 (ha)"])

    # 관련 열 이름
    col_label = col_map[crop][1] if "생산량" in metric else col_map[crop][0]

    # 연도형 컬럼 추출 (예: 2024, 2024.1, ...)
    year_cols = [col for col in df.columns if col.startswith("2024") or col.startswith("202")]

    # 데이터 구조화
    compare_data = []

    for region in selected_regions:
        row = df[df["지역"] == region]
        if row.empty:
            continue
        for col in year_cols:
            if col_label in df.iloc[0].values:
                continue  # 스킵
            value = row[col].values[0]
            compare_data.append({
                "지역": region,
                "연도": col,
                "값": value
            })

    # 데이터프레임 생성
    compare_df = pd.DataFrame(compare_data)
    compare_df["값"] = pd.to_numeric(compare_df["값"], errors="coerce")

    # 시각화
    st.subheader(f"📈 선택 지역들의 '{crop} - {metric}' 연도별 변화 추이")

    if compare_df.empty:
        st.warning("선택한 지역에 대한 데이터가 존재하지 않습니다.")
    else:
        fig = px.line(
            compare_df,
            x="연도",
            y="값",
            color="지역",
            markers=True,
            title=f"{crop} - {metric} (지역별 연도 추이 비교)",
            labels={"값": metric}
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 CSV 파일을 업로드해주세요.")
