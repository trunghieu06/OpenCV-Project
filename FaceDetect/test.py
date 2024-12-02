import cv2

print("[INFO] Initializing Camera ...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0: Camera mặc định, thay đổi nếu cần

if not cap.isOpened():
    print("[ERROR] Cannot access the camera.")
    exit()

while True:
    ret, img = cap.read()

    if not ret:
        print("[WARN] Cannot grab a frame from the camera.")
        break

    # Xử lý ảnh
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Frame", gray)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
