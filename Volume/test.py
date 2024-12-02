import cv2

img = cv2.imread('./image.png', 0)
cv2.imshow("anh", img)
cv2.waitKey()