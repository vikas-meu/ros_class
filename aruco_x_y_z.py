import cv2
import cv2.aruco as aruco
import numpy as np
 
camera_matrix = np.array([
    [640, 0, 320],
    [0, 640, 240],
    [0, 0, 1]
], dtype=np.float32)

dist_coeffs = np.zeros((5, 1))

 
MARKER_SIZE = 0.05  # meters (5 cm)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
    )

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
            corners, MARKER_SIZE, camera_matrix, dist_coeffs
        )

        for i in range(len(ids)):
            rvec, tvec = rvecs[i], tvecs[i]

            x, y, z = tvec[0]
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.03)

            cv2.putText(
                frame,
                f"X:{x:.2f} Y:{y:.2f} Z:{z:.2f} m",
                (10, 30 + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            print(f"Marker {ids[i][0]} -> X:{x:.3f} Y:{y:.3f} Z:{z:.3f}")

    cv2.imshow("Aruco XYZ Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
