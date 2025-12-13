import cv2
import cv2.aruco as aruco

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
marker_id = 0
marker_size = 400

marker = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
cv2.imwrite("aruco_0.png", marker)
