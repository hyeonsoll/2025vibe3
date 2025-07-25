import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="식량작물 생산량 분석", layout="wide")
st.title("🌾 식량작물 생산량 연도별 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 식량작물 CSV 업로드", type=["csv"])

if uploaded_file:
    raw_df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 헤더 재구성: 1행이 컬럼명
    new_columns = raw_df.iloc[0, 1:].tolist()
    new_columns.insert(0, "지역")
    df = raw_df.iloc[1:, :].reset_index(drop=True)
    df.columns = new_columns

    # NaN 및 숫자 정제
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").str.replace("-", "0").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 사용자 선택
    region = st.selectbox("📍 지역 선택", df["지역"].unique())
    available_items = [col for col in df.columns if col != "지역"]
    selected_items = st.multiselect("🌿 시각화할 작물 항목 선택", available_items, default=["미곡:생산량 (톤)"])

    if not selected_items:
        st.warning("❗ 최소 하나의 항목을 선택해주세요.")
        st.stop()

    # long-form 변환
    long_df = df[df["지역"] == region].melt(id_vars="지역", value_vars=selected_items,
                                             var_name="항목", value_name="값")
    st.subheader(f"📈 {region} 지역 작물 생산량 추이")
    fig = px.bar(long_df, x="항목", y="값", color="항목", text="값", title=f"{region} 생산량")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # 추이용 꺾은선그래프: 항목별 연도 변화 (컬럼명 복원 필요)
    st.subheader("📊 연도별 항목 변화 보기 (시계열 추이)")
    year_cols = [col for col in df.columns if col not in ["지역"]]
    time_df = df[df["지역"] == region][year_cols].T.reset_index()
    time_df.columns = ["연도_항목", "값"]

    # 연도 분리
    time_df["연도"] = time_df["연도_항목"].str.extract(r'(20[0-9]{2}(?:\.[0-9]+)?)')
    time_df["항목"] = time_df["연도_항목"].str.extract(r':(.+)')
    time_df["값"] = pd.to_numeric(time_df["값"], errors="coerce")

    # 필터링
    time_filtered = time_df[time_df["항목"].isin([s.split(":")[-1].strip() for s in selected_items])]

    fig2 = px.line(time_filtered, x="연도", y="값", color="항목", markers=True,
                   title=f"{region} 연도별 항목별 변화 추이")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("👆 좌측에서 식량작물 CSV 파일을 업로드해주세요.")
