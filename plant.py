import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 연도별 분석", layout="wide")
st.title("🌾 식량작물 연도별 생산량 시각화 대시보드")

# CSV 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 생산량 CSV 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 첫 행을 컬럼명으로 설정
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # 시도 컬럼명 변경
    if "시도별" in df.columns:
        df = df.rename(columns={"시도별": "지역"})

    # '계' 행 제외
    df = df[df["지역"].notna()]
    df = df[df["지역"] != "계"]

    # 숫자 변환
    for col in df.columns[1:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("-", "0")
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 작물별 컬럼 매핑
    crop_map = {
        "미곡": "미곡:생산량 (톤)",
        "맥류": "맥류:생산량 (톤)",
        "잡곡": "잡곡:생산량 (톤)",
        "두류": "두류:생산량 (톤)",
        "서류": "서류:생산량 (톤)"
    }

    # 사용자 선택
    region = st.selectbox("📍 지역 선택", df["지역"].unique())
    crops = st.multiselect("🌿 작물 선택 (복수 선택 가능)", list(crop_map.keys()), default=["미곡"])

    # 선택한 지역의 데이터 추출
    region_data = df[df["지역"] == region]

    # 연도별 데이터프레임 구성
    year_data = pd.DataFrame()
    for crop in crops:
        if crop_map[crop] in region_data.columns:
            year_data = pd.concat([
                year_data,
                pd.DataFrame({
                    "연도": [2024],  # 현재 파일은 2024년 데이터만 존재
                    "작물": crop,
                    "생산량": [region_data[crop_map[crop]].values[0]]
                })
            ])
        else:
            st.warning(f"{crop} 데이터가 없습니다.")

    # 시각화
    if not year_data.empty:
        st.subheader(f"📈 {region} - 연도별 {', '.join(crops)} 생산량 변화")
        fig = px.bar(year_data, x="작물", y="생산량", color="작물", title=f"{region} 작물 생산량 (2024)")
        st.plotly_chart(fig, use_container_width=True)
        st.metric("총 생산량 (톤)", f"{year_data['생산량'].sum():,.0f}")
    else:
        st.error("해당 작물에 대한 데이터가 없습니다.")
else:
    st.info("👆 CSV 파일을 업로드해주세요.")
