import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 생산량 분석", layout="wide")
st.title("🌾 식량작물 생산량 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 CSV 업로드", type=["csv"])

if uploaded_file:
    raw_df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 헤더 재설정
    new_columns = raw_df.iloc[0, 1:].tolist()
    new_columns.insert(0, "지역")
    df = raw_df.iloc[1:, :].reset_index(drop=True)
    df.columns = new_columns

    # 숫자 처리
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").str.replace("-", "0").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 사용 가능한 지역과 항목
    available_regions = df["지역"].unique().tolist()
    available_items = [col for col in df.columns if col != "지역"]

    # ✅ 여러 지역 & 항목 선택
    selected_regions = st.multiselect("📍 지역 선택", available_regions, default=available_regions[:3])
    selected_items = st.multiselect("🌿 항목 선택 (예: 미곡:생산량)", available_items, default=["미곡:생산량 (톤)"])

    if not selected_regions or not selected_items:
        st.warning("지역과 항목을 최소 하나씩 선택해주세요.")
        st.stop()

    # -----------------------------------
    # 1. 지역별 항목 비교 막대그래프
    # -----------------------------------
    st.subheader("📊 선택한 항목에 대한 지역별 생산량 비교")

    compare_df = df[df["지역"].isin(selected_regions)][["지역"] + selected_items]
    compare_long = compare_df.melt(id_vars="지역", var_name="항목", value_name="값")

    fig_compare = px.bar(
        compare_long,
        x="지역",
        y="값",
        color="항목",
        barmode="group",
        title="지역별 항목 생산량 비교"
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    # -----------------------------------
    # 2. 기존 지역 1개 선택의 연도별 꺾은선 그래프 (선택)
    # -----------------------------------
    st.subheader("📈 특정 지역의 연도별 항목 변화 추이")
    region_for_time = st.selectbox("📍 연도별 추이를 볼 지역 선택", available_re_
