import cv2
import time
import os # Thư viên đường dẫn
import hand as htm # Thư viện chia các điểm trên bàn tay

if __name__ == "__main__":
    pTime = 0 # Thời điểm bắt đầu

    cap =cv2.VideoCapture(0, cv2.CAP_DSHOW)

    folderPath = "./Fingers"
    lst = os.listdir(folderPath)
    lst2 = []
    print("Các đường dẫn tới các mục nằm trong folderPath là:", lst)
    for i in lst:
        image = cv2.imread(f"{folderPath}/{i}") # Đường dẫn tới từng ảnh
        lst2.append(image) # Thêm các ma trận điểm ảnh vào lst2, mỗi cái chứa thông tin màu sắc,..
    #print(lst2[0].shape)


    detector = htm.handDetector(detectionCon=1) #
    fingerid = [4, 8, 12, 16, 20] # Tọa độ các đỉnh của từng ngón tay
    numberFingers = 0
    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw=False) # Phát hiện vị trí
        print(lmList)

        if len(lmList) != 0:
            numberFingers = 0

            # Đếm ngón cái:
            if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                numberFingers += 1

            # Đếm ngón dài
            for id in range(1, 5):
                if lmList[fingerid[id]][2] < lmList[fingerid[id] - 2][2]:
                    numberFingers += 1
            #print(fingers)


        h, w, c = lst2[numberFingers].shape
        frame[0: h, 0: w] = lst2[numberFingers] # copy khung ảnh

        # Vẽ hình chữ nhật đếm số ngón tay:s
        cv2.rectangle(frame, (0, 200), (150, 400), (20, 150, 50), -1)
        cv2.putText(frame, str(numberFingers), (25, 365), cv2.FONT_ITALIC, 5, (255, 20, 150), 5)

        # Viết FPS: frame per second, số khung hình trên giây
        cTime = time.time() # số giây, tính từ 0:0:0 ngày 1/1/1970
        fps = 1/(cTime - pTime)
        pTime = cTime

        # Hiển thị Fps
        cv2.putText(frame, f"FPS: {int(fps)}", (150, 80), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

        cv2.imshow("Fingers count", frame)
        if cv2.waitKey(10) == ord("s"):
            break
    cap.release() # giải phóng camera
    cv2.destroyAllWindows()  # Thoát tất cả các sửa sổ

    # cv2.destroyWindow("namewinning")
    