import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Diet Planner & Calorie Calculator",
    page_icon="🥗",
    layout="wide"
)

# -------------------------
# 데이터
# -------------------------

MEALS = {
    "체중 감량": {
        "아침": [("오트밀", 250), ("삶은 달걀 2개", 140), ("블루베리", 50)],
        "점심": [("닭가슴살 샐러드", 350), ("방울토마토", 30)],
        "저녁": [("연어구이", 350), ("채소볶음", 120)],
        "간식": [("그릭요거트", 120)]
    },
    "체중 유지": {
        "아침": [("토스트 2장", 220), ("삶은 달걀 2개", 140)],
        "점심": [("현미밥", 300), ("닭가슴살", 200), ("야채", 80)],
        "저녁": [("생선구이", 350), ("샐러드", 100)],
        "간식": [("바나나", 100)]
    },
    "근육 증가": {
        "아침": [("오트밀", 300), ("계란 3개", 210), ("바나나", 100)],
        "점심": [("현미밥", 350), ("닭가슴살", 250), ("아보카도", 150)],
        "저녁": [("소고기 스테이크", 450), ("고구마", 200)],
        "간식": [("단백질 쉐이크", 200)]
    }
}

FOODS = {
    "닭가슴살 100g": 165,
    "현미밥 100g": 111,
    "고구마 100g": 86,
    "계란 1개": 70,
    "바나나 1개": 100,
    "사과 1개": 95,
    "그릭요거트 100g": 97,
    "오트밀 100g": 389,
    "연어 100g": 208,
    "아보카도 100g": 160
}


# -------------------------
# 함수
# -------------------------

def calculate_meal_calories(meal_data):
    total = 0

    for items in meal_data.values():
        for _, calorie in items:
            total += calorie

    return total


# -------------------------
# 헤더
# -------------------------

st.title("🥗 Diet Planner & Calorie Calculator")
st.caption("다이어트 식단 추천과 칼로리 계산을 한 번에")

# -------------------------
# 사이드바
# -------------------------

st.sidebar.header("⚙️ 목표 설정")

goal = st.sidebar.selectbox(
    "다이어트 목표",
    ["체중 감량", "체중 유지", "근육 증가"]
)

target_calories = st.sidebar.number_input(
    "하루 목표 칼로리(kcal)",
    min_value=1000,
    max_value=5000,
    value=2000,
    step=50
)

# -------------------------
# 탭 구성
# -------------------------

tab1, tab2, tab3 = st.tabs(
    ["🍽️ 식단 추천", "🔥 칼로리 계산기", "📊 하루 요약"]
)

# -------------------------
# 식단 추천
# -------------------------

with tab1:

    st.subheader("추천 식단")

    meal_plan = MEALS[goal]

    total_meal_calories = calculate_meal_calories(meal_plan)

    for meal_name, foods in meal_plan.items():

        with st.expander(meal_name, expanded=True):

            meal_total = 0

            rows = []

            for food, calorie in foods:
                rows.append([food, calorie])
                meal_total += calorie

            df = pd.DataFrame(
                rows,
                columns=["음식", "칼로리(kcal)"]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.success(f"{meal_name} 칼로리: {meal_total} kcal")

    st.markdown("---")

    st.metric(
        "추천 식단 총 칼로리",
        f"{total_meal_calories} kcal"
    )

# -------------------------
# 칼로리 계산기
# -------------------------

with tab2:

    st.subheader("음식 칼로리 계산")

    selected_foods = st.multiselect(
        "음식 선택",
        list(FOODS.keys())
    )

    user_total = 0

    if selected_foods:

        result_rows = []

        for food in selected_foods:

            amount = st.number_input(
                f"{food} 섭취량 배수",
                min_value=0.5,
                max_value=10.0,
                value=1.0,
                step=0.5,
                key=food
            )

            calories = int(FOODS[food] * amount)

            result_rows.append(
                [food, amount, calories]
            )

            user_total += calories

        df = pd.DataFrame(
            result_rows,
            columns=[
                "음식",
                "배수",
                "총 칼로리(kcal)"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"총 섭취 칼로리: {user_total} kcal"
        )

    st.session_state["user_total"] = user_total
    st.session_state["meal_total"] = total_meal_calories

# -------------------------
# 하루 요약
# -------------------------

with tab3:

    st.subheader("하루 섭취 현황")

    meal_total = st.session_state.get(
        "meal_total",
        total_meal_calories
    )

    user_total = st.session_state.get(
        "user_total",
        0
    )

    combined = meal_total + user_total

    st.metric(
        "추천 식단 칼로리",
        f"{meal_total} kcal"
    )

    st.metric(
        "직접 계산한 칼로리",
        f"{user_total} kcal"
    )

    st.metric(
        "총 칼로리",
        f"{combined} kcal"
    )

    progress = min(combined / target_calories, 1.0)

    st.progress(progress)

    difference = combined - target_calories

    if difference > 0:
        st.error(
            f"목표보다 {difference} kcal 초과했습니다."
        )
    elif difference < 0:
        st.info(
            f"목표보다 {abs(difference)} kcal 부족합니다."
        )
    else:
        st.success("목표 칼로리를 정확히 달성했습니다.")
