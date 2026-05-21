import streamlit as st
import random

# 페이지 기본 설정 (태블릿/모바일 최적화 레이아웃)
st.set_page_config(page_title="영어 타이핑 퀘스트", page_icon="🐉", layout="centered")

# 세션 상태 초기화
if 'initialized' not in st.session_state:
    st.session_state.quiz_data = [
        {"desc": "A fruit that is red and crunchy.", "answer": "apple"},
        {"desc": "The opposite of hot.", "answer": "cold"},
        {"desc": "You wear these on your feet before shoes.", "answer": "socks"},
        {"desc": "A big animal with a long trunk.", "answer": "elephant"},
        {"desc": "The color of the sky on a clear day.", "answer": "blue"},
        {"desc": "The king of the jungle, has a big mane.", "answer": "lion"},
        {"desc": "You use this to read stories and learn.", "answer": "book"},
        {"desc": "The bright yellow object in the sky during the day.", "answer": "sun"}
    ]
    st.session_state.current_q = random.choice(st.session_state.quiz_data)
    st.session_state.exp = 0
    st.session_state.boss_hp = 100
    st.session_state.combo = 0
    st.session_state.initialized = True

st.title("🐉 보스 토벌전: 타이핑 마스터")

# 상단 상태창
st.subheader("보스 몬스터 HP")
st.progress(st.session_state.boss_hp / 100)

col1, col2 = st.columns(2)
with col1:
    st.metric(label="내 경험치 (EXP)", value=st.session_state.exp)
with col2:
    st.metric(label="현재 콤보 🔥", value=f"{st.session_state.combo} Combo!")

st.divider()

# 게임 클리어 로직
if st.session_state.boss_hp <= 0:
    st.balloons()
    st.success("🎉 축하합니다! 보스를 물리쳤습니다!")
    if st.button("새로운 몬스터 소환하기"):
        st.session_state.boss_hp = 100
        st.session_state.exp += 50
        st.session_state.combo = 0
        st.session_state.current_q = random.choice(st.session_state.quiz_data)
        st.rerun()
else:
    st.info(f"💡 **힌트:** {st.session_state.current_q['desc']}")

    with st.form("attack_form", clear_on_submit=True):
        user_answer = st.text_input("정답을 영어로 입력하고 엔터를 누르세요:", autocomplete="off")
        submitted = st.form_submit_button("공격 개시! ⚔️")

        if submitted:
            if user_answer.strip().lower() == st.session_state.current_q['answer']:
                st.session_state.combo += 1
                damage = 10 + (st.session_state.combo * 2)
                st.session_state.boss_hp = max(0, st.session_state.boss_hp - damage)
                st.session_state.exp += 10
                st.toast(f"정답! {damage} 데미지를 입혔습니다!", icon="💥")
                st.session_state.current_q = random.choice(st.session_state.quiz_data)
                st.rerun()
            else:
                st.session_state.combo = 0
                st.toast("공격 실패! 오타를 확인해 보세요.", icon="💦")
                st.rerun()