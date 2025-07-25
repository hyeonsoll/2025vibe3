import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
from geopy.geocoders import Nominatim

# JSON 파일 경로
BOOKMARK_FILE = 'bookmarks.json'

# 북마크 불러오기
def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 북마크 저장
def save_bookmarks(bookmarks):
    with open(BOOKMARK_FILE, 'w', encoding='utf-8') as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

# 주소 → 좌표 변환
def geocode(address):
    geolocator = Nominatim(user_agent="bookmark_app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# --- 세션 상태 초기화 ---
if "selected_bookmark_index" not in st.session_state:
    st.session_state.selected_bookmark_index = None

# --- 앱 기본 UI 설정 ---
st.set_page_config(layout="wide")
st.title("📍 나만의 북마크 지도")

# 북마크 목록 불러오기
bookmarks = load_bookmarks()

# --- 사이드바: 북마크 목록 ---
st.sidebar.header("📌 저장된 북마크")
for i, bm in enumerate(bookmarks):
    if st.sidebar.button(f"{bm['name']}", key=f"bookmark_{i}"):
        st.session_state.selected_bookmark_index = i

st.sidebar.markdown("---")
st.sidebar.header("➕ 새 북마크 추가")

# --- 사이드바: 북마크 추가 폼 ---
with st.sidebar.form("add_bookmark"):
    new_name = st.text_input("장소 이름")
    new_address = st.text_input("도로명 주소")
    submitted = st.form_submit_button("추가하기")
    if submitted:
        lat, lon = geocode(new_address)
        if lat and lon:
            bookmarks.append({
                "name": new_name,
                "address": new_address,
                "lat": lat,
                "lon": lon
            })
            save_bookmarks(bookmarks)
            st.success(f"✅ '{new_name}' 북마크가 저장되었습니다.")
            # 새 북마크 선택 상태로 전환
            st.session_state.selected_bookmark_index = len(bookmarks) - 1
            st.experimental_rerun()
        else:
            st.error("❌ 주소를 찾을 수 없습니다. 다시 입력해주세요.")

# --- 지도 위치 설정 ---
if st.session_state.selected_bookmark_index is not None:
    selected = bookmarks[st.session_state.selected_bookmark_index]
    map_center = [selected["lat"], selected["lon"]]
    zoom = 16
else:
    map_center = [37.5665, 126.9780]  # 서울 기본 위치
    zoom = 12

# --- 지도 생성 ---
m = folium.Map(location=map_center, zoom_start=zoom)

# 북마크 마커 표시
for bm in bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=f"{bm['name']}<br>{bm['address']}",
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# --- 지도 렌더링 ---
st_data = st_folium(m, width=1000, height=600)
