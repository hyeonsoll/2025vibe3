import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", page_icon="✊✋✌️")

st.title("✊✋✌️ 가위바위보 게임!")
st.markdown("컴퓨터와 가위바위보 대결을 해보세요!")

# 선택 옵션
options = ['가위', '바위', '보']
user_choice = st.radio("당신의 선택은?", options, horizontal=True)

# 세션 상태로 점수 저장
if 'score' not in st.session_state:
    st.session_state['score'] = 0

# 게임 시작 버튼
if st.button("대결 시작!"):
    computer_choice = random.choice(options)

    st.write(f"💻 컴퓨터의 선택: **{computer_choice}**")
    st.write(f"🧑‍💻 당신의 선택: **{user_choice}**")

    # 승패 판단
    if user_choice == computer_choice:
        result = "🤝 비겼습니다!"
    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "🎉 당신이 이겼습니다!"
        st.session_state['score'] += 1
    else:
        result = "😭 컴퓨터가 이겼습니다!"
        st.session_state['score'] -= 1

    st.subheader(result)
    st.markdown(f"현재 점수: **{st.session_state['score']}점**")

# 점수 초기화 버튼
if st.button("점수 초기화"):
    st.session_state['score'] = 0
    st.success("점수가 초기화되었습니다!")

