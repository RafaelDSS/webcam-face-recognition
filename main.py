import sys
import face_recognition
import cv2
import numpy as np
from numpy import linalg as LA


from milvus_helpers import MilvusHelper
from mysql_helpers import MySQLHelper

from config import DEFAULT_TABLE
from logs import LOGGER


MILVUS_CLI = MilvusHelper()
MYSQL_CLI = MySQLHelper()


def do_search(table_name, embedding, milvus_client, mysql_cli):
    embedding = list(embedding)

    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        vectors = milvus_client.search_vectors(table_name, [embedding], 1)

        vector = vectors[0]
        id = str(vector[0].id)
        distance = vector[0].distance
        person_name = mysql_cli.search_by_milvus_id(id, table_name)
        return person_name, distance
    except Exception as e:
        LOGGER.error(" Error with search : {}".format(e))
        sys.exit(1)


video_capture = cv2.VideoCapture(1)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            name = "Unknown"

            person_name, distance = do_search(DEFAULT_TABLE, face_encoding, MILVUS_CLI, MYSQL_CLI)
            if distance <= 0.39:
                name = person_name

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
