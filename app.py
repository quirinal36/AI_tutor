import streamlit as st
from utils.ai_helper import get_ai_response
from utils.prompt_templates import SUBJECT_TEMPLATES

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
# 프로젝트에 fonts 폴더 생성 후 NanumGothic.ttf 파일 넣기
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NanumGothic.ttf')
font = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font.get_name()

st.title("나만의 AI 학습 도우미")

# 사용자 정보 입력
with st.sidebar:
    name = st.text_input("이름을 입력하세요")
    subject = st.selectbox("관심 과목", list(SUBJECT_TEMPLATES.keys()))
    st.write(f"안녕하세요, {name}님!")
# 주제별 탭 인터페이스
if subject:
    topic_options = list(SUBJECT_TEMPLATES[subject].keys())
    topic = st.selectbox("학습 유형 선택", topic_options)

    if "개념 설명" in topic or "문법 설명" in topic:
        user_input = st.text_input("개념/주제를 입력하세요")
        template_key = "topic"
    elif "문제 풀이" in topic or "문장 교정" in topic:
        user_input = st.text_area("문제/문장을 입력하세요")
        template_key = "problem" if "문제" in topic else "sentence"
    elif "연습 문제" in topic:
        user_input = st.text_input("주제를 입력하세요")
        level = st.select_slider("난이도", ["쉬움", "보통", "어려움"])
        count = st.slider("문제 수", 1, 10, 3)
        template_key = "topic"
    elif "대화 연습" in topic:
        user_input = st.text_input("상황을 입력하세요 (예: 카페에서 주문하기)")
        template_key = "situation"
        
st.write("이 앱은 AI를 활용한 맞춤형 학습을 도와줍니다.")

if name and subject:
    st.success(f"{name}님, {subject} 과목을 선택하셨습니다!")
    
    if st.button("학습 시작"):
        st.balloons()
        st.write("학습 준비가 완료되었습니다!")

st.header("AI에게 질문하기")
question = st.text_area("질문을 입력하세요")

if question and st.button("답변 받기"):
    with st.spinner("AI가 답변을 생성 중입니다..."):
        answer = get_ai_response(f"{subject}에 관한 다음 질문에 답해주세요: {question}")
        st.write("💡 AI 답변:")
        st.write(answer)

# AI 답변 생성
if st.button("생성하기"):
    if user_input:
        # 프롬프트 템플릿 가져오기
        prompt_template = SUBJECT_TEMPLATES[subject][topic]
        
        # 템플릿에 사용자 입력 삽입
        prompt = prompt_template.format(**{template_key: user_input, 
                                         "level": level if "연습 문제" in topic else "", 
                                         "count": count if "연습 문제" in topic else ""})
        
        with st.spinner("AI가 답변을 생성 중입니다..."):
            answer = get_ai_response(prompt)
            st.write("💡 AI 답변:")
            st.markdown(answer)