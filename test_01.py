import cv2
import numpy as np

def filter_circles(circles, gray):
    filtered_circles = []
    for (x, y, r) in circles:
        # 원의 비율 및 주변 픽셀 값을 기준으로 필터링
        if 15 < r < 80:
            # 주변 픽셀 값을 기준으로 원이 아닌 것들을 필터링
            mask = np.zeros_like(gray)
            cv2.circle(mask, (x, y), r, 255, -1)
            mean_val = cv2.mean(gray, mask=mask)[0]
            if mean_val > 50:  # 주변 픽셀 평균값 기준 (조정 필요)
                filtered_circles.append((x, y, r))
    return filtered_circles

# USB 카메라 캡처 (디폴트 장치는 0)
cap = cv2.VideoCapture(1)

# 카메라가 열리지 않은 경우 종료
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 가우시안 블러 적용
    gray = cv2.GaussianBlur(gray, (15, 15), 2)
    
    # 이진화 적용
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # 허프 변환을 사용하여 원 검출
    circles = cv2.HoughCircles(binary, cv2.HOUGH_GRADIENT, dp=1.0, minDist=100,
                               param1=100, param2=30, minRadius=15, maxRadius=200)
    
    # 원이 검출된 경우
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        filtered_circles = filter_circles(circles, gray)
        
        for (x, y, r) in filtered_circles:
            # 원의 외곽선 그리기
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            # 원의 중심점 그리기
            cv2.circle(frame, (x, y), 2, (0, 128, 255), 3)
    
    # 결과 프레임 출력
    cv2.imshow("Circle Detection", frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
