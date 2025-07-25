import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2025 연령별 인구 분석", layout="wide")
st.title("📊 2025년 6월 연령별 인구 분석 대시보드")

# 파일 업로드
file_mf = st.file_uploader("남/여 인구 데이터 파일 업로드", type="csv", key="mf")
file_total = st.file_uploader("합계 인구 데이터 파일 업로드", type="csv", key="total")

# 연령 분포 추출 함수
def extract_age_data(df, prefix):
    age_cols = [col for col in df.columns if col.startswith(prefix) and "총인구수" not in col and "연령구간인구수" not in col]
    def parse_age(col):
        age_part = col.replace(prefix, "").replace("세", "")
        return 100 if "이상" in age_part else int(age_part)
    ages = [parse_age(col) for col in age_cols]
    values = df.iloc[0][age_cols].astype(str).str.replace(",", "").fillna("0").astype(int).tolist()
    return pd.DataFrame({"연령": ages, "인구수": values})

if file_mf and file_total:
    # 데이터 불러오기
    df_mf = pd.read_csv(file_mf, encoding='cp949')
    df_total = pd.read_csv(file_total, encoding='cp949')

    # 전국 데이터 필터링
    df_mf = df_mf[df_mf['행정구역'].astype(str).str.contains("전국")]
    df_total = df_total[df_total['행정구역'].astype(str).str.contains("서울특별시")]  # 예시: '서울특별시' 기준

    # 연령별 분리
    df_male = extract_age_data(df_mf, "2025년06월_남_")
    df_female = extract_age_data(df_mf, "2025년06월_여_")
    df_total_age = extract_age_data(df_total, "2025년06월_계_")

    # 성별 추가
    df_male["성별"] = "남"
    df_female["성별"] = "여"
    df_total_age["성별"] = "합계"

    # 통합
    all_df = pd.concat([df_male, df_female, df_total_age], ignore_index=True)

    # 사용자 선택
    gender = st.radio("성별 선택", ["남", "여", "합계"])
    selected = all_df[all_df["성별"] == gender]

    # 선 그래프
    fig = px.line(selected, x="연령", y="인구수", title=f"{gender} 연령별 인구 분포", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 막대 그래프
    fig2 = px.bar(selected, x="연령", y="인구수", title=f"{gender} 연령별 인구 막대그래프")
    st.plotly_chart(fig2, use_container_width=True)

    # 총 인구 수
    st.metric(f"총 인구 수 ({gender})", f"{selected['인구수'].sum():,} 명")
else:
    st.info("👆 두 개의 파일(CSV)을 업로드하세요.")
