```python
import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Smart Diet Planner",
    page_icon="🥗",
    layout="wide"
)

# -----------------------
# 식단 데이터
# -----------------------

DIET_PLANS = {
    "체중 감량": [
        {"name":"닭가슴살 샐러드 식단","foods":[("오트밀",250),("닭가슴살 샐러드",350),("연어",300),("그릭요거트",120)]},
        {"name":"저탄수 식단","foods":[("계란 2개",140),("닭가슴살",250),("두부",180),("샐러드",100)]},
        {"name":"지중해식 식단","foods":[("오트밀",250),("연어",350),("아보카도",150),("샐러드",120)]},
        {"name":"현미 다이어트 식단","foods":[("현미밥",250),("닭가슴살",250),("채소",100),("요거트",120)]},
        {"name":"고단백 감량 식단","foods":[("계란",210),("닭가슴살",300),("그릭요거트",120),("채소",80)]},
        {"name":"연어 감량 식단","foods":[("연어",350),("채소",100),("고구마",180),("요거트",120)]},
        {"name":"채식 다이어트 식단","foods":[("두부",200),("현미밥",250),("채소",120),("바나나",100)]},
        {"name":"오트밀 식단","foods":[("오트밀",300),("계란",140),("샐러드",100),("요거트",120)]},
        {"name":"균형 감량 식단","foods":[("현미밥",250),("생선",250),("채소",120),("과일",100)]},
        {"name":"저지방 식단","foods":[("계란",140),("닭가슴살",250),("채소",150),("사과",95)]},
    ],
    "체중 유지": [
        {"name":"한식 균형식","foods":[("현미밥",300),("생선",300),("채소",150),("과일",100)]},
        {"name":"일반 균형식","foods":[("토스트",250),("닭가슴살",250),("현미밥",300),("요거트",120)]},
        {"name":"직장인 도시락 식단","foods":[("현미밥",350),("닭가슴살",250),("채소",150)]},
        {"name":"지중해 유지 식단","foods":[("연어",350),("아보카도",180),("샐러드",120),("과일",100)]},
        {"name":"생선 위주 식단","foods":[("생선",350),("현미밥",300),("채소",150)]},
        {"name":"닭고기 위주 식단","foods":[("닭가슴살",300),("현미밥",300),("채소",150)]},
        {"name":"건강 유지 식단","foods":[("오트밀",250),("연어",300),("채소",150),("요거트",120)]},
        {"name":"균형 영양 식단","foods":[("계란",210),("현미밥",300),("생선",300)]},
        {"name":"가정식 식단","foods":[("현미밥",350),("계란",140),("채소",150),("과일",100)]},
        {"name":"활동량 유지 식단","foods":[("오트밀",300),("닭가슴살",300),("고구마",200)]},
    ],
    "근육 증가": [
        {"name":"벌크업 식단","foods":[("오트밀",350),("계란",280),("현미밥",400),("소고기",500)]},
        {"name":"고단백 식단","foods":[("닭가슴살",400),("계란",280),("고구마",250),("쉐이크",250)]},
        {"name":"운동선수 식단","foods":[("현미밥",450),("소고기",500),("채소",150)]},
        {"name":"린매스업 식단","foods":[("닭가슴살",400),("현미밥",400),("요거트",150)]},
        {"name":"고탄수 식단","foods":[("오트밀",350),("현미밥",500),("고구마",300)]},
        {"name":"헬스 식단","foods":[("계란",280),("닭가슴살",450),("고구마",250)]},
        {"name":"근성장 식단","foods":[("소고기",500),("현미밥",450),("쉐이크",250)]},
        {"name":"파워 식단","foods":[("오트밀",350),("계란",280),("소고기",500)]},
        {"name":"운동 전후 식단","foods":[("바나나",100),("쉐이크",250),("닭가슴살",400)]},
        {"name":"하드 벌크업 식단","foods":[("현미밥",600),("소고기",600),("계란",280)]},
    ]
}

# -----------------------
# 칼로리 계산기 DB
# -----------------------

FOODS = {
    "닭가슴살 100g":165,
    "현미밥 100g":111,
    "고구마 100g":86,
    "계란 1개":70,
    "바나나 1개":100,
    "사과 1개":95,
    "그릭요거트 100g":97,
    "오트밀 100g":389,
    "연어 100g":208,
    "아보카도 100g":160
}

st.title("🥗 Smart Diet Planner")

goal = st.sidebar.selectbox(
    "목표 선택",
    ["체중 감량","체중 유지","근육 증가"]
)

target = st.sidebar.number_input(
    "하루 목표 칼로리",
    min_value=1000,
    max_value=5000,
    value=2000
)

tab1, tab2, tab3 = st.tabs(
    ["식단 추천","칼로리 계산기","하루 분석"]
)

# -----------------------
# 추천 식단
# -----------------------

with tab1:

    plans = DIET_PLANS[goal]

    def total_cal(plan):
        return sum(cal for _, cal in plan["foods"])

    best_plan = min(
        plans,
        key=lambda x: abs(total_cal(x)-target)
    )

    if st.button("🎲 다른 식단 추천"):
        best_plan = random.choice(plans)

    st.subheader(best_plan["name"])

    rows = []
    total = 0

    for food, cal in best_plan["foods"]:
        rows.append([food, cal])
        total += cal

    df = pd.DataFrame(
        rows,
        columns=["음식","칼로리"]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.success(f"추천 식단 총 칼로리 : {total} kcal")

    st.markdown("---")

    st.subheader("사용자 음식 추가")

    custom_name = st.text_input("음식 이름")

    custom_cal = st.number_input(
        "칼로리(kcal)",
        min_value=0,
        value=0
    )

    if "custom_total" not in st.session_state:
        st.session_state.custom_total = 0

    if st.button("추가"):
        st.session_state.custom_total += custom_cal
        st.success("추가 완료")

# -----------------------
# 계산기
# -----------------------

with tab2:

    selected = st.multiselect(
        "음식 선택",
        list(FOODS.keys())
    )

    calc_total = 0

    for food in selected:

        amount = st.number_input(
            f"{food} 배수",
            min_value=0.5,
            max_value=10.0,
            value=1.0,
            step=0.5,
            key=food
        )

        calc_total += FOODS[food] * amount

    st.metric(
        "총 칼로리",
        f"{int(calc_total)} kcal"
    )

# -----------------------
# 분석
# -----------------------

with tab3:

    final_total = (
        total +
        st.session_state.custom_total +
        calc_total
    )

    st.metric(
        "추천 식단",
        f"{total} kcal"
    )

    st.metric(
        "추가 음식",
        f"{st.session_state.custom_total} kcal"
    )

    st.metric(
        "계산기 음식",
        f"{int(calc_total)} kcal"
    )

    st.metric(
        "총 섭취량",
        f"{int(final_total)} kcal"
    )

    progress = min(final_total / target, 1.0)

    st.progress(progress)

    diff = int(final_total - target)

    if diff > 0:
        st.error(f"{diff} kcal 초과")
    elif diff < 0:
        st.info(f"{abs(diff)} kcal 부족")
    else:
        st.success("목표 달성")
```
