from realsense import realsense
import cv2

while True:
    frame = realsense.Get_RGB_Frame()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("realsense", frame)
    cv2.waitKey(1)