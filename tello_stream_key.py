from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()

# 배터리 확인
print(f"battery: {me.get_battery()}")

global img
me.streamon()

# OpenCV VideoWriter 설정 
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (960, 720))  # 적절한 해상도를 선택하세요


def getKeyboardInput():

    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 50
    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"):ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"):yv = -speed
    elif kp.getKey("d"): yv = speed

    if kp.getKey("q"): me.land(); time.sleep(3)
    if kp.getKey("e"):  me.takeoff()

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]

while True:

    vals = getKeyboardInput()

    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = me.get_frame_read().frame

    #img = cv2.resize(img, (360, 240))

    cv2.imshow("Image", img)
    out.write(img)

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