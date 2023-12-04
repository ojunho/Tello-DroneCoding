# 필요한 라이브러리 임포트
import time
import cv2
from djitellopy import Tello

# Tello 객체 생성
tello = Tello()

# Tello 드론 연결
tello.connect()

# 배터리 확인
print(f"battery: {tello.get_battery()}")

# 비디오 스트리밍 활성화
tello.streamon()

# OpenCV VideoWriter 설정 
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (960, 720))  # 적절한 해상도를 선택하세요


# 드론 이륙
tello.takeoff()

# 드론 전진 (20cm)
tello.move_forward(100)

# 5초 동안 대기
time.sleep(2)

# 드론 착륙
tello.land()

# 비디오 스트리밍을 통해 영상을 받아오는 동안
while True:
    # 비디오 프레임 받아오기
    frame = tello.get_frame_read().frame

    # 영상 출력
    cv2.imshow("Tello Video", frame)

    # 영상을 파일에 저장
    out.write(frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 스트리밍 종료
tello.streamoff()

# 연결 종료
tello.end()


# OpenCV 창 닫기
cv2.destroyAllWindows()
out.release()