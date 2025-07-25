import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="신·재생에너지 분석", layout="wide")
st.title("🔋 신·재생에너지 총생산량 추이 분석 (toe 기준)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    try:
        # CSV 읽기
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')

    # 연도 컬럼만 추출
    year_cols = [col for col in df.columns if col.startswith("20")]

    # '신·재생에너지 총생산량' 항목 필터링
    df_filtered = df[df["에너지원별(1)"].str.contains("총생산량", na=False)].copy()

    # long-form 변환
    df_long = df_filtered.melt(
        id_vars=["에너지원별(1)", "에너지원별(2)", "에너지원별(3)"],
        value_vars=year_cols,
        var_name="연도",
        value_name="생산량"
    )

    # 숫자 변환
    df_long["생산량"] = pd.to_numeric(df_long["생산량"], errors="coerce")

    # 선택 박스: 에너지원 그룹
    options = df_long["에너지원별(2)"].unique().tolist()
    selected_sources = st.multiselect("에너지원 분류 선택", options, default=options)

    # 필터링
    chart_df = df_long[df_long["에너지원별(2)"].isin(selected_sources)]

    # Plotly 그래프
    fig = px.line(
        chart_df,
        x="연도",
        y="생산량",
        color="에너지원별(2)",
        markers=True,
        title="📈 신·재생에너지 총생산량 추이"
    )
    fig.update_layout(yaxis_title="생산량 (toe)")

    st.plotly_chart(fig, use_container_width=True)

    st.success(f"✅ 선택된 에너지원 개수: {len(selected_sources)}")
else:
    st.info("👆 좌측 또는 위에서 CSV 파일을 업로드해주세요.")
