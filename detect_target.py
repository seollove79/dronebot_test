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
    
    # 적응형 이진화 적용
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Canny 엣지 검출
    edges = cv2.Canny(adaptive_thresh, 50, 150)
    
    # 컨투어 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 가장 큰 컨투어 찾기
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        
        if radius > 10:  # 임의의 최소 반지름 값 설정
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 4)

    # 결과 프레임 표시
    cv2.imshow("USB Camera", frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처 객체 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
