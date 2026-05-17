import os
import sys
import cv2
import pickle
import numpy as np

FACE_DATA = os.path.expanduser("~") + "/FRIDAY/memory/face_data.pkl"

def register_face(name="Prantick"):
    try:
        import face_recognition
        cap = cv2.VideoCapture(0)
        print("Look at camera. Press SPACE to capture.")

        face_encodings = []
        captured = 0

        while captured < 5:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("FRIDAY Face Registration - Press SPACE", frame)
            key = cv2.waitKey(1)

            if key == 32:  # SPACE
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(rgb)
                if encodings:
                    face_encodings.append(encodings[0])
                    captured += 1
                    print(f"Captured {captured}/5")

            if key == 27:  # ESC
                break

        cap.release()
        cv2.destroyAllWindows()

        if face_encodings:
            data = {"name": name, "encodings": face_encodings}
            os.makedirs(os.path.dirname(FACE_DATA), exist_ok=True)
            with open(FACE_DATA, 'wb') as f:
                pickle.dump(data, f)
            return f"Face registered for {name}"
        return "No face detected"

    except Exception as e:
        return f"Registration error: {e}"

def verify_face():
    try:
        import face_recognition
        if not os.path.exists(FACE_DATA):
            return True  # No face data = skip auth

        with open(FACE_DATA, 'rb') as f:
            data = pickle.load(f)

        known_encodings = data["encodings"]
        name = data["name"]

        cap = cv2.VideoCapture(0)
        verified = False
        attempts = 0

        while attempts < 30:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)

            if encodings:
                matches = face_recognition.compare_faces(
                    known_encodings,
                    encodings[0],
                    tolerance=0.6
                )
                if True in matches:
                    verified = True
                    break

            cv2.imshow("FRIDAY Face Auth - Look at camera", frame)
            cv2.waitKey(1)
            attempts += 1

        cap.release()
        cv2.destroyAllWindows()
        return verified

    except Exception as e:
        print(f"Face auth error: {e}")
        return True  # Skip if error

def face_auth_enabled():
    return os.path.exists(FACE_DATA)