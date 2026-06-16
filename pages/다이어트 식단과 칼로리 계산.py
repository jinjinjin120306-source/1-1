```python
import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Diet Coach AI",
    page_icon="🥗",
    layout="wide"
)

# ===================================
# Gemini
# ===================================

def ask_gemini(question):
    try:
        from google import genai

        api_key = st.secrets["GEMINI_API_KEY"]

        client = genai.Client(api_key=api_key)

        prompt = f"""
당신은 전문 다이어트 코치입니다.

사용자가 먹고 싶은 음식을
다이어트 식단으로 바꾸는 방법을 알려주세요.

질문:
{question}

답변 형식

1. 먹어도 되는지
2. 칼로리 줄이는 방법
3. 추천 식단 조합
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


# ===================================
# 음식 DB
# ===================================

food_db = {
    "닭가슴살":165,
    "닭다리살":215,
    "계란":70,
    "삶은계란":70,
    "현미밥":150,
    "백미밥":210,
    "고구마":128,
    "감자":77,
    "바나나":105,
    "사과":95,
    "배":100,
    "오렌지":62,
    "귤":35,
    "토마토":22,
    "오이":15,
    "브로콜리":35,
    "양배추":25,
    "상추":12,
    "두부":80,
    "연어":208,
    "참치":150,
    "고등어":205,
    "오트밀":190,
    "그릭요거트":120,
    "우유":120,
    "아몬드":116,
    "호두":130,
    "아보카도":160,
    "통밀빵":80,
    "베이글":270,
    "치킨":320,
    "후라이드치킨":350,
    "피자":285,
    "햄버거":540,
    "떡볶이":450,
    "라면":500,
    "삼겹살":518,
    "소고기":250,
    "돼지고기안심":180,
    "새우":99,
    "오징어":92,
    "김밥":350,
    "샌드위치":280,
    "단백질쉐이크":150,
    "샐러드":80,
    "콩":120,
    "렌틸콩":115,
    "치즈":113,
    "파스타":350,
    "메밀국수":280,
    "우동":420,
    "짜장면":800,
    "짬뽕":750,
    "돈까스":700,
    "카레":450,
    "김치찌개":250,
    "된장찌개":180,
    "순두부찌개":220,
    "비빔밥":550,
    "잡곡밥":170,
    "복숭아":58,
    "수박":46,
    "딸기":33,
    "블루베리":57
}

food_df = pd.DataFrame(
    list(food_db.items()),
    columns=["음식","칼로리"]
)

# ===================================
# 식단
# ===================================

weight_loss = [
("오트밀+바나나+닭가슴살 샐러드+두부",660),
("삶은계란+현미밥+연어+샐러드",730),
("그릭요거트+고구마+닭가슴살+브로콜리",690),
("오트밀+사과+참치샐러드+두부",640),
("바나나+현미밥+연어+샐러드",710),
("계란+고구마+닭가슴살+토마토",620),
("그릭요거트+현미밥+연어+양배추",700),
("사과+고구마+참치+브로콜리",650),
("바나나+두부+닭가슴살+샐러드",610),
("오트밀+계란+연어+브로콜리",720),
("현미밥+닭가슴살+샐러드+아몬드",760),
("고구마+연어+샐러드+토마토",670),
("그릭요거트+바나나+참치+양배추",650),
("계란+현미밥+두부+브로콜리",640),
("오트밀+고구마+닭가슴살+샐러드",680)
]

maintain = [
("계란+현미밥+연어+샐러드",850),
("오트밀+통밀빵+닭가슴살",890),
("고구마+연어+현미밥",920),
("그릭요거트+참치+잡곡밥",880),
("계란+소고기+현미밥",980),
("닭가슴살+잡곡밥+브로콜리",870),
("연어+감자+샐러드",910),
("참치+현미밥+아보카도",940),
("고등어+잡곡밥+샐러드",960),
("소고기+감자+브로콜리",990)
]

bulkup = [
("오트밀+단백질쉐이크+닭가슴살+현미밥",1250),
("계란+통밀빵+연어+잡곡밥",1320),
("소고기+현미밥+아몬드",1400),
("닭가슴살+고구마+단백질쉐이크",1280),
("연어+현미밥+아보카도",1350),
("소고기+감자+우유",1420),
("고등어+현미밥+단백질쉐이크",1300),
("닭가슴살+잡곡밥+아몬드",1260),
("연어+통밀빵+우유",1330),
("소고기+고구마+단백질쉐이크",1450)
]

# ===================================
# UI
# ===================================

st.title("🥗 Diet Coach AI")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "식단 추천",
    "칼로리 계산기",
    "음식 검색",
    "BMI/TDEE",
    "AI 식단 코치"
])

# ===================================
# 식단 추천
# ===================================

with tab1:

    goal = st.selectbox(
        "목표 선택",
        ["체중 감량","체중 유지","근육 증가"]
    )

    if st.button("추천 받기"):

        if goal == "체중 감량":
            meal = random.choice(weight_loss)
        elif goal == "체중 유지":
            meal = random.choice(maintain)
        else:
            meal = random.choice(bulkup)

        st.success(meal[0])
        st.metric("총 칼로리", f"{meal[1]} kcal")

# ===================================
# 칼로리 계산기
# ===================================

with tab2:

    selected = st.multiselect(
        "음식 선택",
        food_df["음식"]
    )

    total = 0

    for food in selected:

        qty = st.number_input(
            f"{food} 수량",
            min_value=1,
            value=1,
            key=food
        )

        cal = food_db[food] * qty
        total += cal

    st.metric("총 칼로리", f"{total} kcal")

# ===================================
# 음식 검색
# ===================================

with tab3:

    keyword = st.text_input(
        "검색어 입력"
    )

    if keyword:

        result = food_df[
            food_df["음식"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        if len(result) > 0:
            st.dataframe(
                result,
                use_container_width=True
            )
        else:
            st.warning("검색 결과 없음")

# ===================================
# BMI
# ===================================

with tab4:

    gender = st.selectbox(
        "성별",
        ["남성","여성"]
    )

    age = st.number_input(
        "나이",
        10,
        100,
        25
    )

    height = st.number_input(
        "키(cm)",
        100,
        250,
        170
    )

    weight = st.number_input(
        "몸무게(kg)",
        30,
        200,
        70
    )

    activity = st.selectbox(
        "활동량",
        [
            1.2,
            1.375,
            1.55,
            1.725,
            1.9
        ]
    )

    bmi = weight / ((height/100)**2)

    if gender == "남성":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    tdee = bmr * activity

    st.metric("BMI", round(bmi,1))
    st.metric("기초대사량", round(bmr))
    st.metric("유지칼로리", round(tdee))

# ===================================
# AI
# ===================================

with tab5:

    question = st.text_area(
        "먹고 싶은 음식을 입력하세요",
        placeholder="치킨 먹고 싶은데 다이어트 식단으로 먹을 수 있나요?"
    )

    if st.button("AI 상담"):

        if question.strip():

            with st.spinner("분석중..."):

                answer = ask_gemini(question)

            st.write(answer)

        else:
            st.warning("질문을 입력하세요.")
```

```
```
