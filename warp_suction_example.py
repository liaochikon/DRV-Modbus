from drv_modbus import send
from drv_modbus import request
from landmark import aruco
from realsense import realsense
from pymodbus.client import ModbusTcpClient
import numpy as np
import cv2
import time

def AOI(frame, lower_hsv = np.array([20, 20, 200]), upper_hsv = np.array([50, 255, 255]), min_area = 300, crop_size = 40):
    crop_frame = frame[crop_size:-crop_size, crop_size:-crop_size]
    blur = cv2.GaussianBlur(crop_frame, (3, 3), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    dst = cv2.inRange(hsv, lower_hsv,  upper_hsv)
    contours, _ = cv2.findContours(dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    AOI_points = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            AOI_points.append((cx + crop_size, cy + crop_size))
            cv2.drawContours(crop_frame,contours,-1,(0,0,255),1)  
            cv2.circle(crop_frame, (cx, cy), 3, (255, 255, 0), -1)
    cv2.imshow("dst", dst)
    #cv2.imshow("crop_frame", crop_frame)
    #cv2.waitKey(1)

    return AOI_points

def AOIcoor_2_Realcoor(AOI_points, o_point):
    real_points = []
    for ap in AOI_points:
        real_points.append((ap[1] + o_point[1], ap[0] + o_point[0]))
    return real_points

def Warp(frame, c_center_list, width, height):
    p1 = np.float32(c_center_list)
    p2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    m = cv2.getPerspectiveTransform(p1,p2)
    output = cv2.warpPerspective(frame, m, (width, height))
    return output, m

def Find_Suction_Object(lower_hsv, upper_hsv):
    frame = realsense.Get_RGB_Frame()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    ret, T_cam_to_aruco_result, T_aruco_to_cam_result, id_result, corner_result = aruco.Detect_Aruco(
                                                                                frame, 
                                                                                K, 
                                                                                D, 
                                                                                aruco_length, 
                                                                                aruco_5x5_100_id.aruco_dict, 
                                                                                aruco_5x5_100_id.aruco_params)
    if len(id_result) == 4:
        c_center_list = [(0, 0), (0, 0), (0, 0), (0, 0)]
        for id, c in zip(id_result, corner_result):
            c_center = aruco.Corners_Center(c)
            c_center = (int(c_center[0]), int(c_center[1]))
            c_center_list[id - 1] = c_center
        #cv2.line(frame, c_center_list[0], c_center_list[1], (0, 0, 255), 2)
        #cv2.line(frame, c_center_list[1], c_center_list[3], (0, 0, 255), 2)
        #cv2.line(frame, c_center_list[2], c_center_list[0], (0, 0, 255), 2)
        #cv2.line(frame, c_center_list[3], c_center_list[2], (0, 0, 255), 2)
        
        output, m = Warp(frame, c_center_list, int(real_width), int(real_height))
        AOI_points = AOI(output, lower_hsv, upper_hsv)
        real_points = AOIcoor_2_Realcoor(AOI_points, o_point)
        
        return output, real_points     
    return [], []

def Suction_Behave(real_points):
    if len(real_points) > 0:
        send.Go_Position(c, real_points[0][0], real_points[0][1], home[2], home[3], home[4], home[5], 50)
        send.Go_Position(c, real_points[0][0], real_points[0][1], z_height, home[3], home[4], home[5], 50)
        send.Suction_ON(c)
        send.Go_Position(c, real_points[0][0], real_points[0][1], home[2], home[3], home[4], home[5], 50)
        send.Go_Position(c, drop[0], drop[1], drop[2], home[3], home[4], home[5], 50)
        send.Go_Position(c, drop[0], drop[1], z_height, home[3], home[4], home[5], 50)
        send.Suction_OFF(c)
        send.Go_Position(c, drop[0], drop[1], drop[2], home[3], home[4], home[5], 50)
        send.Go_Position(c, home[0], home[1], home[2], home[3], home[4], home[5], 50)

def main():
    send.Go_Position(c, home[0], home[1], home[2], home[3], home[4], home[5], 50)
    for i in range(50):
        frame = realsense.Get_RGB_Frame()
    real_points = []
    while len(real_points) == 0:
    #while True:
        output, real_points = Find_Suction_Object(silver_plane_lower_hsv, silver_plane_upper_hsv)
    cv2.imshow("output", output)
    cv2.waitKey(1)
    print(real_points)
    Suction_Behave(real_points)
    print("Job done!!!")

yellow_brick_lower_hsv = np.array([20, 20, 200])
yellow_brick_upper_hsv = np.array([50, 255, 255])
silver_plane_lower_hsv = np.array([20, 5, 50])
silver_plane_upper_hsv = np.array([255, 255, 255])
copper_brick_lower_hsv = np.array([10, 100, 50])
copper_brick_upper_hsv = np.array([50, 200, 255])
        
aruco_5x5_100_id = aruco.Aruco(aruco.ARUCO_DICT().DICT_5X5_100, 1, 200)
aruco_length = 0.0525

#x : 388.442, y : -73.33200000000001, z : 325.693, rx: 179.987, ry: -0.004, rz: -106.121 id 1 tcp
#x : 637.4350000000001, y : 221.607, z : 322.593, rx: 179.987, ry: -0.004, rz: -106.121 id 4 tcp
o_point = (-73.332, 388.442)
e_point = (221.607, 637.435)
z_height = 324.796

real_width = e_point[0] - o_point[0]
real_height = e_point[1] - o_point[1]

K = realsense.Get_Color_K()
D = np.array([0.0,0.0,0.0,0.0,0.0,])

c = ModbusTcpClient(host="192.168.1.1", port=502, unit_id=2)
c.connect()

home = [353.208, -48.09, 680.0, 179.987, -0.004, -106.121]
drop =[479.442, 385.366, 521.66, 179.987, -0.004, -106.121]

if __name__ == "__main__":
    for i in range(3):
        main()
    