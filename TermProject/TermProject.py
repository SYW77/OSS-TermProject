import cv2
import numpy as np
import os


cap = cv2.VideoCapture(0)

# 카메라가 정상적으로 열렸는지 확인
if not cap.isOpened():
    print("Error: fail to open the camera")
    exit()

# 카메라 속성 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임을 성공적으로 읽었는지 확인
    if not ret:
        print("Error: fail to load frame")
        os.exit()

    # 프레임 좌우 반전
    frame = cv2.flip(frame, 1)

    # 프레임 표시
    cv2.imshow("Camera", frame)

    # '스페이스바'를 누르면 이미지 저장 및 불러오기
    if cv2.waitKey(1) & 0xFF == ord(' '):
        # 이미지 저장
        cv2.imwrite("captured_image.jpg", frame)
        print("success to save image")

        # 저장된 이미지 불러오기
        src = cv2.imread("captured_image.jpg")
        if src is None :
            print("Error: fail to load image")
            os.exit()


        #그레이 스케일
        #가우시안 블러
        #사물이나 인물 외에 것들을 찾지않게 하기 위해서 가우시안 블러를 사용합니다.
        blur = cv2.GaussianBlur(src, ksize=(5,5), sigmaX=0)
        ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        cv2.imshow("test",blur)
        dst = cv2.Canny(src,100,150)
        #canny는 모서리를 찾을 때 사용되는 알고리즘입니다.
        #canny Canny(src,최소값,최대값)
        #저 값을 조정해서 모서리 찾기를 조절합니다.
        cv2.destroyAllWindows
        ratio = 700.0 / src.shape[1]
        dim = (700, int(src.shape[0] * ratio))



        #이미지 병합하기 + 편지지 붙여넣기
        #여기서 출력할 이미지를 편지지 처럼 만들 수 있습니다.
        size_image= np.shape(dst)
        blank_image = np.zeros((size_image[0],size_image[1]), np.uint8)
        i = 150
        cv2.line(blank_image, (50, i-60), (size_image[1]-50, i-60), (255, 255, 255))
        while size_image[0]>i:
            cv2.line(blank_image, (20, i), (size_image[1]-20, i), (255, 255, 255))
            i=i+50

        #이미지의 가로크기, 세로크기를 확인, 합칠 방향 결정
        #여기서 출력할 이미지를 검은색으로 할 것인지,흰색으로 할 것인지 정할 수 있습니다. #여기선 둘다 구현해놓았습니다.
        if src.shape[0]>src.shape[1]:
            black = np.hstack((dst, blank_image))
        else:
            black = np.vstack((dst, blank_image))
        white = cv2.bitwise_not(black)
        #이미지 보여주기 + 저장

        cv2.imshow('black_version', black)
        cv2.imwrite("black_version_PostCard.jpg", black)
        cv2.imshow('white_version', white)
        cv2.imwrite("white_version_PostCard.jpg", white)

    # 'q' 눌러서 프로그램 종료q
    elif cv2.waitKey(1)&0xFF == ord('q'):
        os.exit()
