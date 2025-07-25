import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="나만의 북마크 지도", page_icon="📍", layout="wide")

st.title("📍 나만의 북마크 지도 만들기")
st.markdown("원하는 장소를 입력해서 북마크 핀을 꽂아보세요!")

# 북마크 저장할 세션 상태
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 북마크 입력 폼
with st.form("bookmark_form"):
    name = st.text_input("📌 장소 이름", placeholder="예: 카페 연남동")
    lat = st.number_input("🧭 위도 (Latitude)", format="%.6f", step=0.000001)
    lon = st.number_input("🧭 경도 (Longitude)", format="%.6f", step=0.000001)
    submitted = st.form_submit_button("✅ 북마크 추가")

    if submitted:
        if name and lat and lon:
            st.session_state.bookmarks.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })
            st.success(f"'{name}' 이(가) 북마크에 추가되었습니다!")
        else:
            st.error("모든 항목을 입력해주세요.")

# 기본 지도 중심 위치 설정 (서울 기준)
if st.session_state.bookmarks:
    last_lat = st.session_state.bookmarks[-1]["lat"]
    last_lon = st.session_state.bookmarks[-1]["lon"]
else:
    last_lat, last_lon = 37.5665, 126.9780  # 서울

# folium 지도 생성
m = folium.Map(location=[last_lat, last_lon], zoom_start=12)

# 북마크들을 지도에 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=800, height=500)

# 저장된 북마크 리스트 출력
st.markdown("### 📋 현재 북마크 목록")
if st.session_state.bookmarks:
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.markdown(f"{i}. **{bm['name']}** (위도: {bm['lat']}, 경도: {bm['lon']})")
else:
    st.write("아직 북마크가 없습니다.")
