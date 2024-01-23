import cv2
from landmark import aruco

id = 4
resolution = 200

aruco_5x5_100 = aruco.Aruco(aruco.ARUCO_DICT().DICT_5X5_100, id, resolution)

cv2.imwrite(str(id) + "_" + str(resolution) + ".png", aruco_5x5_100.tag)
#cv2.imshow("ArUCo Tag", aruco_5x5_100.tag)
#cv2.waitKey(0)