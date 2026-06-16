import streamlit as st
import random

st.set_page_config(
    page_title="Diet Planner AI",
    page_icon="🥗",
    layout="wide"
)

# =========================
# Gemini
# =========================

def ask_gemini(question):
    try:
        from google import genai

        api_key = st.secrets["GEMINI_API_KEY"]

        client = genai.Client(api_key=api_key)

        prompt = f"""
당신은 전문 영양사입니다.

사용자가 먹고 싶은 음식을
다이어트 식단 형태로 바꾸는 방법을 알려주세요.

질문:
{question}

답변 형식:
1. 먹어도 되는지
2. 칼로리 줄이는 방법
3. 추천 조합
4. 주의사항
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text

    except KeyError:
        return "GEMINI_API_KEY가 설정되지 않았습니다."

    except Exception as e:
        return f"AI 응답 오류: {e}"

# =========================
# 음식 DB
# =========================

food_db = {
    "닭가슴살(100g)": 165,
    "삶은계란": 70,
    "바나나": 105,
    "사과": 95,
    "고구마(100g)": 128,
    "현미밥(100g)": 150,
    "오트밀(50g)": 190,
    "그릭요거트": 120,
    "두부(100g)": 80,
    "연어(100g)": 208,
    "브로콜리": 35,
    "아몬드(20g)": 116,
    "아보카도": 160,
    "토마토": 22,
    "샐러드": 80,
    "우유": 120,
    "참치캔": 150,
    "통밀빵": 80,
    "단백질쉐이크": 150,
    "오렌지": 62
}

# =========================
# 식단 데이터
# =========================

diet_plans = {
    "체중 감량": [
        {
            "아침": [("오트밀(50g)",190),("바나나",105)],
            "점심": [("닭가슴살(100g)",165),("현미밥(100g)",150),("브로콜리",35)],
            "저녁": [("두부(100g)",80),("샐러드",80)],
            "간식": [("그릭요거트",120)]
        },
        {
            "아침": [("삶은계란",70),("사과",95)],
            "점심": [("연어(100g)",208),("샐러드",80)],
            "저녁": [("닭가슴살(100g)",165),("브로콜리",35)],
            "간식": [("아몬드(20g)",116)]
        },
        {
            "아침": [("그릭요거트",120),("바나나",105)],
            "점심": [("참치캔",150),("현미밥(100g)",150)],
            "저녁": [("두부(100g)",80),("토마토",22)],
            "간식": [("사과",95)]
        }
    ],

    "유지": [
        {
            "아침":[("오트밀(50g)",190),("우유",120)],
            "점심":[("연어(100g)",208),("현미밥(100g)",150)],
            "저녁":[("두부(100g)",80),("샐러드",80)],
            "간식":[("바나나",105)]
        },
        {
            "아침":[("삶은계란",70),("통밀빵",80)],
            "점심":[("닭가슴살(100g)",165),("현미밥(100g)",150)],
            "저녁":[("연어(100g)",208),("브로콜리",35)],
            "간식":[("그릭요거트",120)]
        }
    ],

    "근육 증가": [
        {
            "아침":[("오트밀(50g)",190),("단백질쉐이크",150)],
            "점심":[("닭가슴살(100g)",165),("현미밥(100g)",150),("브로콜리",35)],
            "저녁":[("연어(100g)",208),("현미밥(100g)",150)],
            "간식":[("아몬드(20g)",116),("바나나",105)]
        },
        {
            "아침":[("삶은계란",70),("통밀빵",80),("우유",120)],
            "점심":[("닭가슴살(100g)",165),("현미밥(100g)",150)],
            "저녁":[("연어(100g)",208),("두부(100g)",80)],
            "간식":[("단백질쉐이크",150)]
        }
    ]
}

# =========================
# UI
# =========================

st.title("🥗 Diet Planner AI")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "식단 추천",
        "칼로리 계산기",
        "음식 검색",
        "AI 식단 상담"
    ]
)

# =========================
# 식단 추천
# =========================

with tab1:

    st.header("다이어트 식단 추천")

    goal = st.selectbox(
        "목표 선택",
        ["체중 감량","유지","근육 증가"]
    )

    if st.button("식단 추천 받기"):

        plan = random.choice(diet_plans[goal])

        total = 0

        for meal, foods in plan.items():

            st.subheader(meal)

            meal_total = 0

            for food, cal in foods:
                st.write(f"• {food} - {cal} kcal")
                meal_total += cal

            total += meal_total

            st.success(f"{meal} 칼로리: {meal_total} kcal")

        st.info(f"총 칼로리: {total} kcal")

# =========================
# 칼로리 계산기
# =========================

with tab2:

    st.header("칼로리 계산기")

    selected = st.multiselect(
        "음식 선택",
        list(food_db.keys())
    )

    total = 0

    for food in selected:

        qty = st.number_input(
            f"{food} 개수",
            min_value=1,
            value=1,
            key=food
        )

        total += food_db[food] * qty

    st.metric(
        "총 칼로리",
        f"{total} kcal"
    )

# =========================
# 음식 검색
# =========================

with tab3:

    st.header("음식 칼로리 검색")

    keyword = st.text_input("음식 이름 입력")

    if keyword:

        found = False

        for food, cal in food_db.items():

            if keyword.lower() in food.lower():

                st.write(f"{food} : {cal} kcal")

                found = True

        if not found:
            st.warning("검색 결과가 없습니다.")

# =========================
# AI 상담
# =========================

with tab4:

    st.header("AI 다이어트 식단 상담")

    question = st.text_area(
        "먹고 싶은 음식이나 고민을 입력하세요",
        placeholder="치킨이 먹고 싶은데 다이어트 식단으로 먹을 수 있을까요?"
    )

    if st.button("AI 상담 받기"):

        if question.strip():

            with st.spinner("AI 분석 중..."):

                answer = ask_gemini(question)

            st.write(answer)

        else:
            st.warning("질문을 입력해주세요.")
