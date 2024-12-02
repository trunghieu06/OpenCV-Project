import cv2
import time
import numpy as np
import os # Thư viên đường dẫn
import hand as htm # Thư viện chia các điểm trên bàn tay
import math # Thư viện tính khoảng cách 2 đầu ngón tay
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

if __name__ == "__main__":
    pTime = 0 # Thời điểm bắt đầu

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = htm.handDetector(detectionCon=1)
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange() # phạm vi âm lượng
    minVol, maxVol = volRange[0], volRange[1]
    
    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw=False) # Phát hiện vị trí
        # print(lmList)
        if len(lmList) != 0:
            # print(lmList[4], lmList[8])
            x1, y1, x2, y2 = lmList[4][1], lmList[4][2], lmList[8][1], lmList[8][2]
            cv2.circle(frame, (x1, y1), 10, (255, 255, 0), -1)
            cv2.circle(frame, (x2, y2), 10, (255, 255, 0), -1)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)
            cv2.circle(frame, ((x1 + x2) // 2, (y1 + y2) // 2), 10, (255, 255, 0), -1)
            
            length = math.hypot(x1 - x2, y1 - y2)
            minLen, maxLen = 25, 180
            if length < minLen:
                cv2.circle(frame, ((x1 + x2) // 2, (y1 + y2) // 2), 10, (255, 0, 255), -1)
            # print(length)
            vol = np.interp(length, [minLen, maxLen], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            
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
    