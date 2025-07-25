import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df_raw = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv")

# 첫 번째 행 제거 및 컬럼명 정리
df = df_raw.drop(index=0)
df.columns = ['시도별'] + list(range(1998, 2025))

# 숫자형으로 변환
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Streamlit 설정
st.set_page_config(page_title="시도별 미곡 생산량 비교", layout="wide")
st.title("🌾 시도별 미곡 생산량 비교 시각화 (1998–2024)")

# 시도 다중 선택
regions = df['시도별'].unique().tolist()
selected_regions = st.multiselect("🔍 비교할 시도를 선택하세요:", regions, default=[regions[0]])

if selected_regions:
    # 선택된 시도의 데이터만 추출
    df_selected = df[df['시도별'].isin(selected_regions)]
    
    # 긴 형식으로 변환 (melt)
    df_long = df_selected.melt(id_vars='시도별', var_name='연도', value_name='생산량 (톤)')
    df_long['연도'] = df_long['연도'].astype(int)

    # 그래프 그리기
    fig = px.line(df_long, x='연도', y='생산량 (톤)', color='시도별',
                  markers=True, title="선택한 시도별 연도별 미곡 생산량 비교")

    st.plotly_chart(fig, use_container_width=True)

    # 데이터 확인용 테이블
    with st.expander("📊 데이터 테이블 보기"):
        st.dataframe(df_long)
else:
    st.warning("비교할 시도를 하나 이상 선택해주세요.")
