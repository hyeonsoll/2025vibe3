import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연도별 지역 생산량 시각화", layout="wide")
st.title("🌾 식량작물 생산량 (미곡:생산량) 연도별 지역 비교")

uploaded_file = st.file_uploader("📁 식량작물 CSV 업로드", type=["csv"])

if uploaded_file:
    # 파일 읽기
    df_raw = pd.read_csv(uploaded_file, encoding="utf-8")

    # 헤더와 데이터 분리
    columns = df_raw.columns.tolist()
    data = df_raw[1:].copy()
    data.columns = df_raw.iloc[0]
    data = data.rename(columns={data.columns[0]: "지역"})

    # 생산량 데이터만 추출 (열 이름이 '.1'로 끝나는 것)
    prod_cols = [col for col in data.columns if str(col).endswith(".1")]
    years = [col.split(".")[0] for col in prod_cols]  # 연도만 추출

    # 연도별 생산량 데이터 정리
    df_plot = pd.DataFrame()

    for year, col in zip(years, prod_cols):
        df_temp = data[["지역", col]].copy()
        df_temp.columns = ["지역", "생산량"]
        df_temp["연도"] = year
        df_plot = pd.concat([df_plot, df_temp], ignore_index=True)

    # 숫자 변환
    df_plot["make"] = pd.to_numeric(df_plot["make"], errors="coerce")
    df_plot = df_plot.dropna()

    # 시각화
    st.subheader("📊 연도별 지역 생산량 (단위: 톤)")
    fig = px.bar(
        df_plot,
        x="연도",
        y="make",
        color="지역",
        barmode="group",
        title="연도별 지역 생산량 (미곡:생산량)",
        labels={"연도": "연도", "생산량": "생산량 (톤)", "지역": "지역"},
    )

    fig.update_layout(
        xaxis=dict(type="category"),
        yaxis_title="생산량 (톤)",
        hovermode="x unified",
        xaxis_rangeslider=dict(visible=True)  # 아래 슬라이더
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 좌측에서 CSV 파일을 업로드해주세요.")
