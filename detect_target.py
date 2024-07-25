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
    
    # 사각형을 찾기 위해 모든 컨투어를 반복
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # 사각형은 꼭짓점이 4개여야 함
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.9 <= aspect_ratio <= 1.1:  # 사각형의 종횡비가 1에 가까워야 함
                # 사각형 내부 ROI 추출
                roi = frame[y:y+h, x:x+w]
                roi_gray = gray[y:y+h, x:x+w]
                

                # ROI에서 다시 적응형 이진화 적용
                roi_thresh = cv2.adaptiveThreshold(
                    roi_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
                )
                
                # ROI에서 Canny 엣지 검출
                roi_edges = cv2.Canny(roi_thresh, 50, 150)
                
                # ROI에서 원 검출
                roi_contours, _ = cv2.findContours(roi_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                found_circle = False
                for roi_contour in roi_contours:
                    ((cx, cy), radius) = cv2.minEnclosingCircle(roi_contour)
                    if (radius > 10 and
                        (x < cx - radius < x + w) and
                        (y < cy - radius < y + h) and
                        (x < cx + radius < x + w) and
                        (y < cy + radius < y + h)):  # 원이 완전히 사각형 내부에 있는지 확인
                        found_circle = True
                        cv2.circle(frame, (int(cx), int(cy)), int(radius), (0, 255, 0), 4)
                        break  # 원을 찾으면 더 이상 탐색하지 않음

                if found_circle:
                    cv2.drawContours(frame, [approx], -1, (255, 0, 0), 2)

    # 결과 프레임 표시
    cv2.imshow("USB Camera", frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처 객체 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
