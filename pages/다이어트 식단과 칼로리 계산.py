import streamlit as st

st.set_page_config(page_title="Diet Buddy", page_icon="🥗", layout="wide")

# ---------------------------
# FOOD DATABASE
# ---------------------------
foods = {
    "닭가슴살": 165,
    "삶은계란(1개)": 70,
    "현미밥(1공기)": 300,
    "흰쌀밥(1공기)": 310,
    "김치": 20,
    "샐러드": 80,
    "고구마": 140,
    "바나나": 100,
    "사과": 95,
    "라면": 500,
    "치킨(후라이드)": 290,
    "피자(1조각)": 285,
    "햄버거": 550,
    "콜라(1캔)": 140,
    "삼겹살(100g)": 330,
    "떡볶이": 400,
    "초밥(1세트)": 320,
    "우유": 120,
    "그릭요거트": 100
}

# ---------------------------
# DIET MENU
# ---------------------------
diet_menus = [
    {
        "name": "기본 저칼로리 식단",
        "menu": ["삶은계란(1개)", "현미밥(1공기)", "샐러드", "닭가슴살"],
    },
    {
        "name": "균형 다이어트 식단",
        "menu": ["고구마", "닭가슴살", "김치", "사과"],
    },
    {
        "name": "가벼운 하루 식단",
        "menu": ["그릭요거트", "바나나", "샐러드", "우유"],
    }
]

# ---------------------------
# FUNCTIONS
# ---------------------------
def calc_calories(selected_items):
    total = 0
    for item, qty in selected_items:
        total += foods.get(item, 0) * qty
    return total


def diet_tip(text):
    text = text.lower()

    if "치킨" in text:
        return "🍗 치킨 → 에어프라이어 구운 치킨 / 양을 반으로 줄이고 샐러드 추가 추천"
    elif "피자" in text:
        return "🍕 피자 → 1~2조각만 + 탄산 대신 물 / 얇은 도우 선택"
    elif "라면" in text:
        return "🍜 라면 → 면 절반 + 계란 + 야채 추가"
    elif "햄버거" in text:
        return "🍔 햄버거 → 단품 + 감자튀김 제외 + 물 선택"
    elif "떡볶이" in text:
        return "🔥 떡볶이 → 양 줄이고 삶은계란/야채 추가"
    else:
        return "🥗 양을 줄이고 단백질 + 채소를 추가하면 다이어트 식단으로 바꿀 수 있어요"


# ---------------------------
# UI
# ---------------------------
st.title("🥗 Diet Buddy - 다이어트 식단 & 칼로리 계산기")

menu = st.sidebar.selectbox("메뉴 선택", ["칼로리 계산기", "식단 추천", "음식 검색", "먹고 싶은 음식 다이어트화"])

# ---------------------------
# CALORIE CALCULATOR
# ---------------------------
if menu == "칼로리 계산기":
    st.subheader("🔥 칼로리 계산기")

    selected_items = []

    food_list = list(foods.keys())

    for i in range(5):
        col1, col2 = st.columns(2)
        with col1:
            food = st.selectbox(f"음식 {i+1}", ["선택"] + food_list, key=i)
        with col2:
            qty = st.number_input(f"수량 {i+1}", min_value=0, max_value=10, value=0, key=f"q{i}")

        if food != "선택" and qty > 0:
            selected_items.append((food, qty))

    if st.button("총 칼로리 계산"):
        try:
            total = calc_calories(selected_items)
            st.success(f"총 섭취 칼로리: {total} kcal")
        except Exception as e:
            st.error("계산 중 오류 발생")

# ---------------------------
# DIET RECOMMENDATION
# ---------------------------
elif menu == "식단 추천":
    st.subheader("🥗 다이어트 식단 추천")

    for diet in diet_menus:
        st.markdown(f"### 🍱 {diet['name']}")
        total = 0
        for item in diet["menu"]:
            cal = foods.get(item, 0)
            total += cal
            st.write(f"- {item} ({cal} kcal)")
        st.info(f"총 칼로리: {total} kcal")
        st.markdown("---")

# ---------------------------
# FOOD SEARCH
# ---------------------------
elif menu == "음식 검색":
    st.subheader("🔍 음식 검색")

    keyword = st.text_input("음식 이름 입력 (예: 치킨, 피자, 라면)")

    if keyword:
        results = {k: v for k, v in foods.items() if keyword in k}

        if results:
            for k, v in results.items():
                st.write(f"🍽 {k} : {v} kcal")
        else:
            st.warning("검색 결과가 없습니다")

# ---------------------------
# DIET TRANSFORMATION
# ---------------------------
elif menu == "먹고 싶은 음식 다이어트화":
    st.subheader("🍔 먹고 싶은 음식 → 다이어트 방법")

    user_input = st.text_input("먹고 싶은 음식 입력")

    if user_input:
        try:
            result = diet_tip(user_input)
            st.success(result)
        except Exception:
            st.error("처리 중 오류 발생")
