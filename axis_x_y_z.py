import cv2
import cv2.aruco as aruco
import numpy as np

 
camera_matrix = np.array([
    [640, 0, 320],
    [0, 640, 240],
    [0, 0, 1]
], dtype=np.float32)

dist_coeffs = np.zeros((5, 1))

 
MARKER_SIZE = 0.05  # meters

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

 
half = MARKER_SIZE / 2
obj_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float32)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

        for corner in corners:
            img_points = corner.reshape(4, 2)

            # ---- Pose estimation using solvePnP ----
            success, rvec, tvec = cv2.solvePnP(
                obj_points,
                img_points,
                camera_matrix,
                dist_coeffs,
                flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

            if success:
                cv2.drawFrameAxes(
                    frame, camera_matrix, dist_coeffs, rvec, tvec, 0.05
                )

                x, y, z = tvec.flatten()
                cv2.putText(
                    frame,
                    f"X:{x:.2f} Y:{y:.2f} Z:{z:.2f} m",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

    cv2.imshow("Aruco XYZ (NEW API)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

