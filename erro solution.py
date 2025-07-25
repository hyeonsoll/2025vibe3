import streamlit as st
import pandas as pd

# 파일 불러오기
df = pd.read_csv("식량작물_생산량_정곡__20250725141928.csv", encoding="utf-8")

# 열 이름 보여주기
st.title("📋 CSV 열 이름 확인")
st.write("아래는 CSV의 열(column) 이름 목록입니다:")
st.write(df.columns.tolist())

# 데이터 일부 미리 보기
st.write("데이터 미리보기:")
st.dataframe(df.head())
