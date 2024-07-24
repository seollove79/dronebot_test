import cv2
import numpy as np

# USB 카메라 장치 번호 (예: 0번 장치)
camera_device = 1

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(camera_device)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지 전처리
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Canny 엣지 검출
    edges = cv2.Canny(gray, 50, 150)
    
    # 허프 변환을 사용한 원 검출
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=50, param2=30, minRadius=100, maxRadius=150)

    # 원이 검출되면 표시
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

    # 결과 프레임 표시
    cv2.imshow("USB Camera", frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처 객체 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
