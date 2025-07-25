import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="손놀림 요정들의 배틀랜드", page_icon="🧚‍♀️")

# 하늘색 테마 CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background: linear-gradient(135deg, #d0f0ff, #e6f7ff);
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .title {
        font-size: 48px;
        color: #007acc;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 0px #ffffff;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #444;
        margin-bottom: 30px;
    }
    .result-box {
        background-color: #ffffffee;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #87cefa;
        color: black;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00bfff;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="title">🧚‍♀️ 손놀림 요정들의 배틀랜드</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">하늘색 요정들과 함께하는 귀여운 가위바위보 대결 ✨</div>', unsafe_allow_html=True)

# 이모지 가위바위보 옵션
emoji_options = {
    "가위 ✂️🐱": "가위",
    "바위 ✊🐻": "바위",
    "보 ✋🦊": "보"
}

# 사용자 선택
user_choice_display = st.radio("👉 당신의 선택은?", list(emoji_options.keys()), horizontal=True)
user_choice = emoji_options[user_choice_display]

# 점수 저장
if 'score' not in st.session_state:
    st.session_state['score'] = 0

# 대결 시작 버튼
if st.button("🎮 대결 시작!"):
    computer_choice = random.choice(["가위", "바위", "보"])
    emoji_reverse = {v: k for k, v in emoji_options.items()}

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.write(f"💻 컴퓨터의 선택: **{emoji_reverse[computer_choice]}**")
    st.write(f"🧑‍💻 당신의 선택: **{user_choice_display}**")

    # 결과 판별
    if user_choice == computer_choice:
        result = "🤝 비겼습니다!"
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        result = "🎉 당신이 이겼어요!"
        st.session_state['score'] += 1
    else:
        result = "😭 아쉽게도 졌어요!"
        st.session_state['score'] -= 1

    st.subheader(result)
    st.markdown(f"🌟 현재 점수: **{st.session_state['score']}점**")
    st.markdown('</div>', unsafe_allow_html=True)

# 점수 초기화 버튼
if st.button("🔄 점수 초기화"):
    st.session_state['score'] = 0
    st.success("점수가 0점으로 초기화됐어요!")

