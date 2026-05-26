import streamlit as st

st.set_page_config(page_title="AI 영상 판별기")

st.title("🎥 AI 영상 판별기")

uploaded_file = st.file_uploader(
    "영상 업로드",
    type=["mp4", "mov", "avi"]
)

if uploaded_file is not None:

    # 영상 보여주기
    st.video(uploaded_file)

    # 파일 크기 기준 아주 간단한 테스트
    file_size_mb = len(uploaded_file.read()) / (1024 * 1024)

    st.write(f"파일 크기: {file_size_mb:.2f} MB")

    # 간단한 판별
    if file_size_mb < 5:
        result = "AI 생성 영상 의심"
        score = 70
    else:
        result = "실제 영상 가능성 높음"
        score = 30

    st.subheader("결과")
    st.write(result)
    st.progress(score)

    st.write(f"AI 의심 확률: {score}%")
