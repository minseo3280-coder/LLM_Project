"""
AI BURGER HOUSE - Streamlit 앱 (수정판)
로컬 LLM(Ollama) 기반 자연어 주문 시스템 + 음성 인식

수정사항:
- 동시성 문제 해결 (입력 잠금 메커니즘)
- @st.cache_data 캐싱 전략 추가
- 타입 힌팅 추가
"""
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from voice_utils import transcribe_audio, text_to_speech, is_api_error, is_valid_transcription
from menu_data import get_menu_data, get_categories
from menu_recommender import recommend_menus, suggest_combo
from llm_engine import get_engine
from typing import Dict, List, Optional, Tuple
import time

# ===== Streamlit 설정 =====
st.set_page_config(
    page_title="AI BURGER HOUSE",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 캐싱된 데이터 로드 함수 =====
@st.cache_data(ttl=3600)  # 1시간 캐싱
def load_menu_data() -> List[Dict]:
    """메뉴 데이터를 캐싱하여 로드"""
    return get_menu_data()

@st.cache_data(ttl=3600)
def load_categories() -> Dict[str, List[Dict]]:
    """카테고리 데이터를 캐싱하여 로드"""
    return get_categories()

@st.cache_resource
def load_engine():
    """LLM 엔진을 캐싱하여 로드 (리소스 캐싱)"""
    return get_engine(
        "ollama",
        model="gemma2:latest",
        base_url="http://localhost:11434"
    )

# ===== 세션 상태 초기화 =====
def init_session_state():
    """세션 상태 초기화 함수"""
    defaults = {
        "last_intent": None,
        "last_recommendations": [],
        "engine": None,
        "audio_processed": False,
        "ai_response_text": "",
        "last_processed_input": "",
        "last_input": "",
        "processing_lock": False,  # 동시성 제어용 잠금
        "last_input_source": None,  # 'voice' 또는 'text'
        "input_timestamp": 0  # 입력 시간 추적
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ===== 캐싱된 데이터 로드 =====
menu_data = load_menu_data()
categories = load_categories()

# ===== 헤더 =====
st.title("🍔 AI BURGER HOUSE")
st.subheader("지능형 햄버거 주문 시스템")
st.caption("마이크 버튼을 누르고 말씀하시거나, 텍스트로 입력해 주세요.")

# ===== 사이드바 설정 =====
with st.sidebar:
    st.markdown("### ⚙️ 시스템 설정")

    # 캐싱된 엔진 로드
    engine = load_engine()
    st.session_state.engine = engine

    if engine and engine.is_available:
        st.success("✅ 시스템 연결됨 (Ollama)")
    else:
        st.warning("⚠️ AI 엔진 미연결")
        st.info("서버 상태를 확인해 주세요.")

    st.markdown("---")
    st.markdown("#### 📊 메뉴 현황")
    st.write(f"전체 메뉴: **{len(menu_data)}종**")
    for cat, menus in categories.items():
        st.write(f"• {cat}: {len(menus)}종")

    st.markdown("---")
    st.markdown("#### 💡 Usage Tip")
    st.markdown("""
    - **음성 주문**: 마이크 아이콘을 클릭하세요.
    - **텍스트 주문**: 키워드 중심으로 입력하세요.
    - (예: "매운 버거 추천", "5천원 이하")
    """)

# ===== 입력 처리 함수 (동시성 제어) =====
def acquire_processing_lock(source: str) -> bool:
    """
    처리 잠금 획득 시도
    동시 입력 방지를 위한 메커니즘
    """
    current_time = time.time()

    # 이미 처리 중이면 거부
    if st.session_state.processing_lock:
        # 5초 이상 잠금 상태면 강제 해제 (데드락 방지)
        if current_time - st.session_state.input_timestamp > 5:
            st.session_state.processing_lock = False
        else:
            return False

    st.session_state.processing_lock = True
    st.session_state.last_input_source = source
    st.session_state.input_timestamp = current_time
    return True

def release_processing_lock():
    """처리 잠금 해제"""
    st.session_state.processing_lock = False

def process_user_input(user_input: str, source: str) -> Tuple[Optional[Dict], List[Dict]]:
    """
    사용자 입력 처리 (통합 함수)

    Args:
        user_input: 사용자 입력 텍스트
        source: 입력 소스 ('voice' 또는 'text')

    Returns:
        (intent, recommendations) 튜플
    """
    if not user_input or not user_input.strip():
        return None, []

    if not acquire_processing_lock(source):
        st.warning("⏳ 이전 요청을 처리 중입니다. 잠시 후 다시 시도해주세요.")
        return None, []

    try:
        with st.spinner("🤖 AI가 주문을 분석하고 있습니다..."):
            intent, recommendations = recommend_menus(
                menu_data, 
                user_input, 
                st.session_state.engine
            )
        return intent, recommendations
    finally:
        release_processing_lock()

# ===== 메인 콘텐츠 =====
col1, col2 = st.columns([1, 1.3], gap="large")

# ===== 좌측: 입력 섹션 =====
with col1:
    st.markdown("### 🎙️ 주문하기")

    # 1. 음성 입력 위젯
    st.write("음성으로 입력:")
    audio_bytes = mic_recorder(
        start_prompt="🎤 말하기 (Click)",
        stop_prompt="⏹️ 완료 (Click)",
        key='recorder',
        use_container_width=True
    )
    # st.write("DEBUG:", audio_bytes)
    st.markdown("---")

    # 2. 텍스트 입력 위젯
    st.write("텍스트로 입력:")
    text_input_area = st.text_area(
        "주문 내용을 입력하세요",
        height=100,
        placeholder="예: 운동 후에 먹기 좋은 단백질 많은 버거 추천해줘",
        label_visibility="collapsed",
        disabled=st.session_state.processing_lock  # 처리 중 비활성화
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        analyze_clicked = st.button(
            "🚀 주문 분석", 
            type="primary", 
            use_container_width=True,
            disabled=st.session_state.processing_lock  # 처리 중 비활성화
        )
    with col_btn2:
        reset_clicked = st.button("🔄 초기화", use_container_width=True)

    # --- 입력 처리 로직 (동시성 제어 적용) ---
    final_user_input = None
    input_source = None

    # A) 음성 입력 감지 (우선순위 높음)
    if audio_bytes and not st.session_state.audio_processed:
        with st.spinner("🎤 음성을 텍스트로 변환 중..."):
            transcribed_text = transcribe_audio(audio_bytes)

        if transcribed_text and transcribed_text != "API_ERROR":
            final_user_input = transcribed_text
            st.session_state.audio_processed = True
            st.success(f'✅ 인식된 음성: "{final_user_input}"')
        elif transcribed_text == "API_ERROR":
            st.error("❌ 음성 인식 서버 연결 실패")
        else:
            # 🔽 여기 추가: 인식이 안 돼도 일단 더미 텍스트로 분석까지 흘려보기
            final_user_input = "매운 버거 추천해줘"
            st.warning("음성이 잘 인식되지 않아 예시 문장으로 테스트합니다.")

    # B) 텍스트 입력 감지 (버튼 클릭 시, 음성 처리 중이 아닐 때만)
    if analyze_clicked and text_input_area.strip() and not final_user_input:
        final_user_input = text_input_area.strip()
        input_source = "text"
        st.session_state.audio_processed = False

    # C) 공통 분석 실행
    if final_user_input and input_source:
        intent, recommendations = process_user_input(final_user_input, input_source)

        if intent is not None:
            st.session_state.last_intent = intent
            st.session_state.last_recommendations = recommendations
            st.session_state.last_input = final_user_input
            st.session_state.ai_response_text = ""  # 새로운 입력이므로 응답 초기화

    # 초기화 로직
    if reset_clicked:
        st.session_state.last_intent = None
        st.session_state.last_recommendations = []
        st.session_state.last_input = ""
        st.session_state.audio_processed = False
        st.session_state.ai_response_text = ""
        st.session_state.processing_lock = False
        st.rerun()

# ===== 우측: 결과 섹션 =====
with col2:
    st.subheader("📋 추천 결과")

    if st.session_state.last_recommendations:
        intent = st.session_state.last_intent
        recs = st.session_state.last_recommendations
        user_input_display = st.session_state.last_input

        # 1. AI 분석 요약
        st.markdown(f'> **고객님 요청:** "{user_input_display}"')

        # 분석 태그 표시
        tags_cols = st.columns(3)
        if intent and intent.get("budget"):
            tags_cols[0].info(f"💰 예산: {intent['budget']:,}원")
        if intent and intent.get("allergies"):
            tags_cols[1].warning(f"⚠️ 제외: {', '.join(intent['allergies'])}")

        st.markdown("---")

        # 2. 추천 메뉴 리스트
        st.markdown("#### ✨ 맞춤 추천 메뉴")
        for idx, menu in enumerate(recs, 1):
            with st.expander(
                f"{idx}. {menu['name']} — {menu['price']:,}원",
                expanded=(idx == 1)
            ):
                st.write(menu["description"])
                col_i1, col_i2, col_i3 = st.columns(3)
                col_i1.caption(f"🔥 {menu.get('calories')} kcal")
                col_i2.caption(f"💪 단백질 {menu.get('protein')}g")
                col_i3.caption(f"🌶️ 맵기 {menu.get('spicy')}/3")

        # 3. 조합 제안 (세트 메뉴)
        combo = suggest_combo(recs, menu_data, budget=intent.get("budget") if intent else None)
        if combo:
            st.markdown("---")
            st.markdown("#### 🍽️ 꿀조합 제안")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**🍔 메인**")
                st.write(combo['main']['name'])
            with c2:
                st.markdown("**🍟 사이드**")
                st.write(combo['side']['name'])
            with c3:
                st.markdown("**🥤 음료**")
                st.write(combo['drink']['name'])
            st.success(f"💰 총 주문 금액: {combo['total_price']:,}원")

        st.markdown("---")

        # 4. LLM 응답 및 TTS (음성 안내)
        if st.session_state.engine and st.session_state.engine.is_available:
            # 응답 생성 (한 번만 실행)
            if not st.session_state.ai_response_text:
                with st.spinner("💬 답변 생성 중..."):
                    menu_names = ", ".join([m['name'] for m in recs])
                    response_prompt = f"""상황: 키오스크가 손님에게 메뉴를 추천함.
손님요청: "{user_input_display}"
추천메뉴: {menu_names}

지시: 추천 메뉴 중 하나를 골라 왜 좋은지 1문장으로 자연스럽게 권유해주세요.
(주의: JSON 형식 사용 금지, 일반 텍스트만 응답)"""

                    try:
                        response_text = st.session_state.engine.generate_response(
                            response_prompt, 
                            json_mode=False
                        )
                        st.session_state.ai_response_text = response_text if response_text else "추천 드린 메뉴를 선택해 주세요!"
                    except Exception as e:
                        st.error(f"❌ 답변 생성 오류: {e}")
                        st.session_state.ai_response_text = "죄송합니다. 오류가 발생했습니다."

            # 텍스트 출력
            final_response = st.session_state.get("ai_response_text", "")
            if final_response:
                st.info(f"💁 **AI 매니저:** {final_response}")

                # [TTS] 음성 재생
                audio_data = text_to_speech(final_response)
                if audio_data:
                    st.audio(audio_data, format="audio/mp3")
                else:
                    st.caption("(TTS 생성 실패)")
    else:
        st.info("👈 왼쪽에서 음성이나 텍스트로 주문을 시작해 보세요!")

# ===== 푸터 =====
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
<strong>AI BURGER HOUSE</strong><br>
Intelligent Kiosk System powered by Local LLM
</div>
""", unsafe_allow_html=True)