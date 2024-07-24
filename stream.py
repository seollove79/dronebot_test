import cv2

# GStreamer 파이프라인 정의
rtsp_url = "rtsp://192.168.144.108:554/stream=1"
gstreamer_pipeline = (
    f"rtspsrc location={rtsp_url} latency=0 ! "
    "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
)

# OpenCV 비디오 캡처 객체 생성
cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

# 비디오 캡처 성공 여부 확인
if not cap.isOpened():
    print("RTSP 스트림을 열 수 없습니다.")
    exit()

# 비디오 프레임 읽기 및 표시
while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 프레임 표시
    cv2.imshow("RTSP Stream", frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
