import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2025 연령별 인구 분석", layout="wide")
st.title("📊 2025년 6월 연령별 인구 분석 대시보드")

# 📂 CSV 업로드
file_mf = st.file_uploader("남/여 인구 데이터 파일 업로드", type="csv", key="mf")
file_total = st.file_uploader("합계 인구 데이터 파일 업로드", type="csv", key="total")

# 📊 연령 데이터 추출 함수
def extract_age_data(df, prefix):
    age_cols = [col for col in df.columns if col.startswith(prefix) and "총인구수" not in col and "연령구간인구수" not in col]
    def parse_age(col):
        age_part = col.replace(prefix, "").replace("세", "")
        return 100 if "이상" in age_part else int(age_part)
    ages = [parse_age(col) for col in age_cols]
    values = df.iloc[0][age_cols].astype(str).str.replace(",", "").fillna("0").astype(int).tolist()
    return pd.DataFrame({"연령": ages, "인구수": values})

if file_mf and file_total:
    # 📄 데이터 불러오기
    df_mf = pd.read_csv(file_mf, encoding='cp949')
    df_total = pd.read_csv(file_total, encoding='cp949')

    # '전국' 또는 '서울특별시' 기준 데이터 선택
    df_mf = df_mf[df_mf['행정구역'].astype(str).str.contains("전국")]
    df_total = df_total[df_total['행정구역'].astype(str).str.contains("서울특별시")]

    if df_mf.empty or df_total.empty:
        st.error("❌ '전국' 또는 '서울특별시' 데이터가 포함되어 있지 않습니다.")
    else:
        # 👦 남, 👧 여, 👥 합계 데이터 프레임 생성
        df_male = extract_age_data(df_mf, "2025년06월_남_")
        df_female = extract_age_data(df_mf, "2025년06월_여_")
        df_total_age = extract_age_data(df_total, "2025년06월_계_")

        df_male["성별"] = "남"
        df_female["성별"] = "여"
        df_total_age["성별"] = "합계"

        # 전체 통합
        all_df = pd.concat([df_male, df_female, df_total_age], ignore_index=True)

        # ✅ 성별 선택
        view_mode = st.radio("보기 모드 선택", ["남", "여", "합계", "남 vs 여 비교"])

        if view_mode in ["남", "여", "합계"]:
            selected = all_df[all_df["성별"] == view_mode]

            fig = px.line(selected, x="연령", y="인구수", title=f"{view_mode} 연령별 인구 선 그래프", markers=True)
            st.plotly_chart(fig, use_container_width=True)

            fig_bar = px.bar(selected, x="연령", y="인구수", title=f"{view_mode} 연령별 인구 막대 그래프")
            st.plotly_chart(fig_bar, use_container_width=True)

            st.metric(f"총 인구 수 ({view_mode})", f"{selected['인구수'].sum():,} 명")

        else:
            # 👦 남 vs 👧 여 비교
            compare_df = all_df[all_df["성별"].isin(["남", "여"])]
            fig = px.line(compare_df, x="연령", y="인구수", color="성별",
                          title="남 vs 여 연령별 인구 비교 선 그래프", markers=True)
            st.plotly_chart(fig, use_container_width=True)

            fig_bar = px.bar(compare_df, x="연령", y="인구수", color="성별",
                             title="남 vs 여 연령별 인구 비교 막대 그래프", barmode="group")
            st.plotly_chart(fig_bar, use_container_width=True)

            # 남녀 각각 총 인구 표시
            col1, col2 = st.columns(2)
            male_total = compare_df[compare_df["성별"] == "남"]["인구수"].sum()
            female_total = compare_df[compare_df["성별"] == "여"]["인구수"].sum()
            col1.metric("총 인구 수 (남)", f"{male_total:,} 명")
            col2.metric("총 인구 수 (여)", f"{female_total:,} 명")
else:
    st.info("👆 위에 두 개의 CSV 파일을 업로드하세요.")
