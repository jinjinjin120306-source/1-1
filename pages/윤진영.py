import streamlit as st

st.set_page_config(
    page_title="다이어트 운동 추천 앱",
    page_icon="🏃",
    layout="centered"
)

st.title("🏃 다이어트 운동 추천 앱")
st.write("현재 상황에 맞는 운동을 추천해드립니다.")

st.divider()

# 입력 받기
time_available = st.selectbox(
    "운동 가능한 시간",
    ["선택하세요", "10~20분", "20~40분", "40분 이상"]
)

place = st.selectbox(
    "운동 장소",
    ["선택하세요", "집", "헬스장", "야외"]
)

intensity = st.selectbox(
    "원하는 운동 강도",
    ["선택하세요", "낮음", "보통", "높음"]
)

knee_condition = st.radio(
    "무릎 상태",
    ["정상", "약간 불편함", "많이 불편함"]
)

st.divider()

def recommend_exercise(time_available, place, intensity, knee_condition):
    """
    상황에 따른 운동 추천
    """

    if knee_condition == "많이 불편함":
        return (
            "가벼운 스트레칭 + 상체 운동",
            "약 80~150 kcal",
            "무릎에 부담이 적은 운동 위주로 진행하세요."
        )

    if place == "집":
        if intensity == "낮음":
            return (
                "홈 스트레칭 + 제자리 걷기",
                "약 100~200 kcal",
                "꾸준히 하는 것이 중요합니다."
            )
        elif intensity == "보통":
            return (
                "홈트레이닝 서킷",
                "약 200~350 kcal",
                "스쿼트, 런지, 플랭크를 조합해보세요."
            )
        else:
            return (
                "HIIT 홈트레이닝",
                "약 300~500 kcal",
                "충분한 휴식을 병행하세요."
            )

    if place == "헬스장":
        if intensity == "낮음":
            return (
                "러닝머신 걷기",
                "약 150~250 kcal",
                "심박수를 적당히 유지하세요."
            )
        elif intensity == "보통":
            return (
                "유산소 + 근력운동",
                "약 300~500 kcal",
                "근력 운동도 함께 해야 체지방 감소에 도움이 됩니다."
            )
        else:
            return (
                "인터벌 러닝 + 웨이트",
                "약 500~800 kcal",
                "운동 전후 스트레칭을 충분히 하세요."
            )

    if place == "야외":
        if intensity == "낮음":
            return (
                "빠르게 걷기",
                "약 150~250 kcal",
                "30분 이상 걸으면 효과가 좋습니다."
            )
        elif intensity == "보통":
            return (
                "조깅",
                "약 250~450 kcal",
                "자신의 페이스를 유지하세요."
            )
        else:
            return (
                "러닝 또는 언덕 달리기",
                "약 400~700 kcal",
                "무리하지 않는 범위에서 진행하세요."
            )

    return None

if st.button("운동 추천 받기"):

    if (
        time_available == "선택하세요"
        or place == "선택하세요"
        or intensity == "선택하세요"
    ):
        st.warning("모든 항목을 선택해주세요.")
    else:
        result = recommend_exercise(
            time_available,
            place,
            intensity,
            knee_condition
        )

        if result:
            exercise, calories, tip = result

            st.success("추천 결과")

            st.subheader("추천 운동")
            st.write(f"✅ {exercise}")

            st.subheader("예상 칼로리 소모")
            st.write(calories)

            st.subheader("운동 팁")
            st.info(tip)

            st.divider()

            if time_available == "10~20분":
                st.write("⏱ 추천 운동 시간: 15분")
            elif time_available == "20~40분":
                st.write("⏱ 추천 운동 시간: 30분")
            else:
                st.write("⏱ 추천 운동 시간: 45~60분")

            st.write("💧 운동 전후 충분한 수분 섭취를 권장합니다.")
