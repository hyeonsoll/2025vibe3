import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="신·재생에너지 시각화", layout="wide")
st.title("🔋 신·재생에너지 총생산량 시각화 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')

    # 연도 컬럼만 추출
    year_cols = [col for col in df.columns if col.startswith("20")]

    # '총생산량' 관련 행만 추출
    df_filtered = df[df["에너지원별(1)"].str.contains("총생산량", na=False)].copy()

    # 긴 형식으로 변환
    df_long = df_filtered.melt(
        id_vars=["에너지원별(1)", "에너지원별(2)", "에너지원별(3)"],
        value_vars=year_cols,
        var_name="연도",
        value_name="생산량"
    )
    df_long["생산량"] = pd.to_numeric(df_long["생산량"], errors="coerce")

    # 🔘 에너지원 선택
    all_sources = df_long["에너지원별(2)"].unique().tolist()
    selected_sources = st.multiselect("에너지원 분류 선택", all_sources, default=all_sources)

    # 📅 연도 선택 (파이/막대용)
    available_years = sorted(df_long["연도"].unique())
    selected_year = st.selectbox("분석할 연도 선택 (막대 & 파이차트용)", available_years)

    # 선택된 데이터 필터링
    chart_df = df_long[df_long["에너지원별(2)"].isin(selected_sources)]
    year_df = chart_df[chart_df["연도"] == selected_year]

    # 📈 선 그래프
    st.subheader("📈 연도별 생산량 추이 (선 그래프)")
    fig_line = px.line(
        chart_df,
        x="연도",
        y="생산량",
        color="에너지원별(2)",
        markers=True,
        title="신·재생에너지 생산량 추이"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # 📊 막대 그래프 (선택 연도)
    st.subheader(f"📊 {selected_year}년 에너지원별 생산량 (막대그래프)")
    fig_bar = px.bar(
        year_df,
        x="에너지원별(2)",
        y="생산량",
        color="에너지원별(2)",
        title=f"{selected_year}년 에너지원별 생산량 비교",
        labels={"에너지원별(2)": "에너지원", "생산량": "생산량 (toe)"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 🥧 파이 차트
    st.subheader(f"🥧 {selected_year}년 에너지원별 비중 (파이차트)")
    fig_pie = px.pie(
        year_df,
        names="에너지원별(2)",
        values="생산량",
        title=f"{selected_year}년 에너지원별 생산 비율",
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("👆 왼쪽 또는 위에서 신·재생에너지 CSV 파일을 업로드해주세요.")
