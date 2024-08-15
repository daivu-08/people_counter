import cv2
import dlib
import numpy as np
from datetime import datetime
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('people_count.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS individuals
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              first_seen TEXT, 
              last_seen TEXT)''')
conn.commit()

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize variables
known_face_encodings = []
known_face_ids = []
tolerance = 0.6

def get_face_encoding(frame, face):
    landmarks = predictor(frame, face)
    return np.array(face_rec_model.compute_face_descriptor(frame, landmarks))

def compare_faces(known_encodings, face_encoding):
    if len(known_encodings) == 0:
        return []
    return list(np.linalg.norm(np.array(known_encodings) - face_encoding, axis=1) <= tolerance)

frame_count = 0
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 3 != 0:  # Process every 3rd frame
        continue

    # Convert the image from BGR color (which OpenCV uses) to RGB color
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = detector(rgb_frame)

    current_faces = []
    for face in faces:
        # Get facial landmarks and compute face encoding
        face_encoding = get_face_encoding(rgb_frame, face)

        # Compare with known faces
        matches = compare_faces(known_face_encodings, face_encoding)

        if len(matches) > 0 and True in matches:
            # Update last seen time for known face
            match_index = matches.index(True)
            face_id = known_face_ids[match_index]
            c.execute("UPDATE individuals SET last_seen = ? WHERE id = ?",
                      (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), face_id))
            conn.commit()
        else:
            # New face
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO individuals (first_seen, last_seen) VALUES (?, ?)",
                      (current_time, current_time))
            conn.commit()
            face_id = c.lastrowid
            known_face_encodings.append(face_encoding)
            known_face_ids.append(face_id)

        current_faces.append(face_id)

        # Draw a rectangle around the face
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {face_id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the people count
    cv2.putText(frame, f'People Count: {len(current_faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
conn.close()