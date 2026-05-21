import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="영어 타이핑 퀘스트", page_icon="🐉", layout="centered")

# 1. 세션 상태 초기화
if 'quiz_data' not in st.session_state:
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
    st.session_state.last_result = "" # 결과 메시지 저장용

st.title("🐉 보스 토벌전: 타이핑 마스터")

# 2. 상단 스테이터스 표시
st.subheader("보스 몬스터 HP")
st.progress(st.session_state.boss_hp / 100)

col1, col2 = st.columns(2)
with col1:
    st.metric(label="내 경험치 (EXP)", value=st.session_state.exp)
with col2:
    st.metric(label="현재 콤보 🔥", value=f"{st.session_state.combo} Combo!")

st.divider()

# 3. 게임 클리어 또는 진행 화면
if st.session_state.boss_hp <= 0:
    st.balloons()
    st.success("🎉 축하합니다! 보스를 물리쳤습니다!")
    if st.button("새로운 몬스터 소환하기"):
        st.session_state.boss_hp = 100
        st.session_state.exp += 50
        st.session_state.combo = 0
        st.session_state.last_result = ""
        st.session_state.current_q = random.choice(st.session_state.quiz_data)
        st.rerun()
else:
    # 퀴즈 힌트 출력
    st.info(f"💡 **힌트:** {st.session_state.current_q['desc']}")
    
    # 입력창과 버튼 (st.form을 쓰지 않고 분리)
    user_answer = st.text_input("정답을 영어로 입력하세요 (대소문자 상관없음):", key="answer_input")
    
    if st.button("공격 개시! ⚔️"):
        if user_answer:
            if user_answer.strip().lower() == st.session_state.current_q['answer']:
                st.session_state.combo += 1
                damage = 10 + (st.session_state.combo * 2)
                st.session_state.boss_hp = max(0, st.session_state.boss_hp - damage)
                st.session_state.exp += 10
                st.session_state.last_result = f"success|💥 정답! {damage} 데미지를 입혔습니다!"
                st.session_state.current_q = random.choice(st.session_state.quiz_data)
            else:
                st.session_state.combo = 0
                st.session_state.last_result = "error|💦 공격 실패! 오타를 확인해 보세요."
            
            # 입력창을 수동으로 비우기 위해 리런하지 않고 화면 갱신 유도
            st.rerun()

    # 4. 공격 결과 출력 영역 (가장 아래에 안정적으로 배치)
    if st.session_state.last_result:
        res_type, res_msg = st.session_state.last_result.split("|")
        if res_type == "success":
            st.success(res_msg)
        else:
            st.error(res_msg)
