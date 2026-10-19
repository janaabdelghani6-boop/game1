# import cv2
# # # Video Processing
# # cap = cv2.VideoCapture(0)  # Open default camera

# # while True:
# #     ret, frame = cap.read()  # Read frame from camera (frame is in BGR format)

# #     if not ret:
# #         break  # Break if frame is not read correctly

# #     frame = cv2.flip(frame, 1)
# #     # Process frame (e.g., display, save, etc.)
# #     cv2.imshow('Frame', frame)  # Display frame in a window

# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break  # Exit loop if 'q' is pressed


# # cap.release()  # Release the video capture object
# # cv2.destroyAllWindows()  # Close all OpenCV windows
# img = cv2.imread('images.png')
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# # mp.solutions.drawing_utils --> gives convenience functions to draw landmarks & connections.

# mp_hands = mp.solutions.hands
# # mp.solutions.hands --> is the Hands solution (the model + post-processing API).

# cap = cv2.VideoCapture(0)
# # opens the laptop camera and Returns a capture object you’ll read frames from.

# with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
#     # min_detection_confidence --> threshold to accept an initial hand detection.
#     # min_tracking_confidence --> threshold to keep tracking a hand across frames.
#     while cap.isOpened(): # Run a loop as long as the camera is open
#         ret, frame = cap.read() # ret is True if the cam reads, frame is a NumPy array (image) in BGR color (OpenCV default).

#         if not ret:
#             break  # the camera failed to operate or ended so will exit the loop.
        
#         frame = cv2.flip(frame, 1) # flip the camera to be like a mirror.
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # openCV returns BGR but we want RGB for mediapipe so we convert.
#         results = hands.process(image) # results --> is a list of 21 landmarks per detected hand.
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # returning back to BRG so openCV can display.

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
#         # if hand is detected draw the 21 landmarks(hand_landmarks) and connections (.HAND_CONNECTIONS)

#         cv2.imshow('Robotech', image) # open the window and display
#         if cv2.waitKey(5) & 0xFF == 27:
#             break

# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# # mp.solutions.drawing_utils --> gives convenience functions to draw landmarks & connections.
# mp_pose = mp.solutions.pose
# # mp.solutions.pose --> is the Pose solution (the model + post-processing API).

# cap = cv2.VideoCapture(0)
# # opens the laptop camera and Returns a capture object you'll read frames from.

# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     # min_detection_confidence --> threshold to accept an initial body detection.
#     # min_tracking_confidence --> threshold to keep tracking the body across frames.
#     while cap.isOpened():  # Run a loop as long as the camera is open
#         ret, frame = cap.read()  # ret is True if the cam reads, frame is a NumPy array (image) in BGR color (OpenCV default).

#         if not ret:
#             break  # the camera failed to operate or ended so will exit the loop.

#         frame = cv2.flip(frame, 1)  # flip the camera to be like a mirror.
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # openCV returns BGR but we want RGB for mediapipe so we convert.
#         results = pose.process(image)  # results --> contains 33 landmarks for the detected body pose.
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # returning back to BGR so openCV can display.

#         if results.pose_landmarks:
#             mp_drawing.draw_landmarks(
#                 image,
#                 results.pose_landmarks,          # the 33 body landmarks
#                 mp_pose.POSE_CONNECTIONS,         # skeleton connections between landmarks
#                 mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),   # landmark dots style
#                 mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)                     # connection lines style
#             )
#         # if body is detected draw the 33 landmarks and connections (.POSE_CONNECTIONS)

#         cv2.imshow('Robotech', image)  # open the window and display
#         if cv2.waitKey(5) & 0xFF == 27:
#             break

# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# # mp.solutions.drawing_utils --> gives convenience functions to draw landmarks & connections.
# mp_face_mesh = mp.solutions.face_mesh
# # mp.solutions.face_mesh --> is the FaceMesh solution (478 facial landmarks model + post-processing API).

# cap = cv2.VideoCapture(0)
# # opens the laptop camera and returns a capture object you'll read frames from.

# with mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
#     # max_num_faces --> maximum number of faces to detect and track in the frame.
#     # min_detection_confidence --> threshold to accept an initial face detection.
#     # min_tracking_confidence --> threshold to keep tracking the face across frames.

#     while cap.isOpened():  # Run a loop as long as the camera is open
#         ret, frame = cap.read()  # ret is True if the cam reads, frame is a NumPy array (image) in BGR color (OpenCV default).

#         if not ret:
#             break  # the camera failed to operate or ended so will exit the loop.

#         frame = cv2.flip(frame, 1)  # flip the camera to be like a mirror.
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # openCV returns BGR but we want RGB for mediapipe so we convert.
#         results = face_mesh.process(image)  # results --> contains 478 landmarks for each detected face.
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # returning back to BGR so openCV can display.

#         if results.multi_face_landmarks:
#             # multi_face_landmarks --> a list of landmark sets, one per detected face.
#             for face_landmarks in results.multi_face_landmarks:
#                 # iterate over each detected face (here max is 1).
#                 mp_drawing.draw_landmarks(
#                     image,
#                     landmark_list=face_landmarks,          # the 478 facial landmarks
#                     connections=mp_face_mesh.FACEMESH_TESSELATION,  # triangular mesh connections across the face
#                     #landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,255), thickness=1, circle_radius=1),  # landmark dots style (commented out = default/none)
#                     connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1)  # connection lines style
#                 )
#             # if face is detected, draw the 478 landmarks connected as a tessellation mesh.

#         cv2.imshow('Robotech', image)  # open the window and display
#         if cv2.waitKey(5) & 0xFF == 27:
#             break  # exit if ESC is pressed (ASCII 27).

# cap.release()
# cv2.destroyAllWindows()