import streamlit as st
import cv2
import tempfile
import numpy as np

st.set_page_config(page_title="AI Video Detector", layout="centered")

st.title("🎥 AI 영상 판별 앱")
st.write("업로드한 영상이 AI 생성 영상인지 간단히 분석합니다.")

uploaded_file = st.file_uploader(
    "영상 파일 업로드",
    type=["mp4", "mov", "avi"]
)

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    brightness_values = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 10프레임마다 분석
        if frame_count % 10 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            brightness_values.append(brightness)

        frame_count += 1

    cap.release()

    if len(brightness_values) == 0:
        return "분석 실패", 0

    std_value = np.std(brightness_values)

    # 아주 단순한 기준
    if std_value < 8:
        result = "AI 생성 영상 의심"
        score = 78
    else:
        result = "실제 영상 가능성 높음"
        score = 22

    return result, score

if uploaded_file is not None:

    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_video_path = tmp_file.name

    with st.spinner("영상 분석 중..."):
        result, score = analyze_video(temp_video_path)

    st.subheader("분석 결과")
    st.write(f"결과: **{result}**")
    st.progress(score)

    st.write(f"AI 의심 확률: {score}%")
