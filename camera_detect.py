import cv2

cap1 = None
cap2 = None

for i in range(100):
    temp = cv2.VideoCapture(i)

    if temp.isOpened() and cap1 is not None:
        cap2 = cv2.VideoCapture(1)
        print(f"cap2: {i}")

    if temp.isOpened() and cap1 is None:
        cap1 = cv2.VideoCapture(i)
        print(f"cap1: {i}")

    if cap1 is not None and cap2 is not None:
        break

while True:
    _, frame1 = cap1.read()
    _, frame2 = cap2.read()

    if cap1.isOpened():
        cv2.imshow("cam1", frame1)
    if cap2.isOpened():
        cv2.imshow("cam2", frame2)

    key = cv2.waitKey(5) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()
cap1.release()
cap2.release()
