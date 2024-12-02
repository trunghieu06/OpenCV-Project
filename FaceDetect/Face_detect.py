import cv2
import os

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cam.isOpened():
    print('Camera dang khong duoc mo!')
cam.set(3, 640)
cam.set(4, 480)


# face_detector = cv2.CascadeClassifier('C:/HK1/GT-nganh-TTNT/OpenCV/FaceDetect/haarcascade_frontalface_default.xml')
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

face_id = input("\n Nhap ID khuon mat <return> ==> ")

print("\n [INFO] Khoi tao Camera ...")
count = 0

while True:
    ret, img = cam.read()
    #img = cv2.flip(img, -1) # flip video img vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0 ,0), 2)
        count += 1
        print(count)
        cv2.imwrite("./dataset/user." + str(face_id) + '.' + str(count) + ".jpg", gray[y: y + h, x: x + w])
        cv2.imshow('image', img)


    k = cv2.waitKey(100)
    if k == ord('s'):
        break
    elif count >= 30:
        break

print("\n [INFO] Thoat")
cam.release()
cv2.destroyAllWindows()
