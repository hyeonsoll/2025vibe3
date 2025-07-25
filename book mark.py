import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json
import os

# 📁 JSON 파일 경로
BOOKMARK_FILE = "bookmarks.json"

# 📥 북마크 불러오기
def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 💾 북마크 저장하기
def save_bookmarks(data):
    with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 📍 주소 → 위도/경도 변환
def geocode_address(address):
    geolocator = Nominatim(user_agent="bookmark_map_app", timeout=10)
    try:
        location = geolocator.geocode(address, language='ko')
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        st.warning(f"지오코딩 오류: {e}")
        return None, None

# 🌐 페이지 설정
st.set_page_config(page_title="나만의 북마크 지도", page_icon="📍", layout="wide")

st.title("📍 주소 기반 나만의 북마크 지도")
st.markdown("도로명 주소를 입력하면 자동으로 위치가 검색되고, 지도를 북마크할 수 있습니다.")

# 🗂 세션 상태 초기화 및 불러오기
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = load_bookmarks()

# 📮 입력 폼
with st.form("bookmark_form"):
    name = st.text_input("📌 장소 이름", placeholder="예: 연남동 카페")
    address = st.text_input("📮 주소 입력", placeholder="예: 서울특별시 마포구 양화로 123")
    submitted = st.form_submit_button("✅ 북마크 추가")

    if submitted:
        if name and address:
            with st.spinner("주소를 검색 중입니다..."):
                lat, lon = geocode_address(address)
            if lat and lon:
                new_bm = {
                    "name": name,
                    "address": address,
                    "lat": lat,
                    "lon": lon
                }
                st.session_state.bookmarks.append(new_bm)
                save_bookmarks(st.session_state.bookmarks)
                st.success(f"'{name}' 이(가) 북마크에 추가되었습니다!")
            else:
                st.error("주소를 찾을 수 없습니다. 도로명 주소를 다시 확인해주세요.")
        else:
            st.error("장소 이름과 주소를 모두 입력해주세요.")

# 🗺 지도 중심 설정 (마지막 북마크 또는 서울)
if st.session_state.bookmarks:
    last_lat = st.session_state.bookmarks[-1]["lat"]
    last_lon = st.session_state.bookmarks[-1]["lon"]
else:
    last_lat, last_lon = 37.5665, 126.9780

# 🌍 folium 지도 생성
m = folium.Map(location=[last_lat, last_lon], zoom_start=12)

# 📍 지도에 북마크 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=f"{bm['name']}<br>{bm['address']}",
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 🖼 지도 출력
st_data = st_folium(m, width=800, height=500)

# 📋 북마크 리스트 출력
st.markdown("### 📑 저장된 북마크 목록")
if st.session_state.bookmarks:
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.markdown(f"{i}. **{bm['name']}** - `{bm['address']}`")
else:
    st.info("아직 북마크가 없습니다. 위에서 추가해보세요!")
