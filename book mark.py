import streamlit as st

try:
    import folium
    from streamlit_folium import st_folium
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    FOLIUM_AVAILABLE = True
except ModuleNotFoundError:
    FOLIUM_AVAILABLE = False

st.set_page_config(page_title="주소 기반 북마크 지도", page_icon="📍", layout="wide")

st.title("📍 주소 기반 나만의 북마크 지도")
st.markdown("주소를 입력하면 자동으로 지도가 표시되고 북마크가 저장됩니다.")

if not FOLIUM_AVAILABLE:
    st.error("❌ folium, geopy 등이 설치되지 않았습니다.")
    st.stop()

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 주소 → 위도/경도 변환 함수 (개선됨)
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

# 입력 폼
with st.form("bookmark_form"):
    name = st.text_input("📌 장소 이름", placeholder="예: 내 최애 카페")
    address = st.text_input("📮 주소 입력", placeholder="예: 서울특별시 마포구 양화로 123")
    submitted = st.form_submit_button("✅ 북마크 추가")

    if submitted:
        if name and address:
            with st.spinner("주소를 검색 중입니다..."):
                lat, lon = geocode_address(address)
            if lat and lon:
                st.session_state.bookmarks.append({
                    "name": name,
                    "address": address,
                    "lat": lat,
                    "lon": lon
                })
                st.success(f"'{name}'이(가) 북마크에 추가되었습니다!")
            else:
                st.error("주소를 찾을 수 없습니다. 더 구체적인 도로명 주소를 사용해보세요.")
        else:
            st.error("장소 이름과 주소를 모두 입력해주세요.")

# 지도 중심 설정
if st.session_state.bookmarks:
    last_lat = st.session_state.bookmarks[-1]["lat"]
    last_lon = st.session_state.bookmarks[-1]["lon"]
else:
    last_lat, last_lon = 37.5665, 126.9780  # 서울

# 지도 생성
m = folium.Map(location=[last_lat, last_lon], zoom_start=12)

# 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=f"{bm['name']}<br>{bm['address']}",
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=800, height=500)

# 북마크 리스트 출력
st.markdown("### 📋 북마크 목록")
if st.session_state.bookmarks:
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.markdown(f"{i}. **{bm['name']}** - `{bm['address']}`")
else:
    st.info("아직 북마크가 없습니다. 도로명 주소를 입력해 추가해보세요!")
