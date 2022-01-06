import os
import face_recognition

from milvus_helpers import MilvusHelper
from mysql_helpers import MySQLHelper
from config import DEFAULT_TABLE



MILVUS_CLI = MilvusHelper()
MYSQL_CLI = MySQLHelper()

def extract_features():
    images = os.listdir('images')

    known_face_encodings = []
    known_face_names = []

    for image in images:
        current_image = face_recognition.load_image_file("images/" + image)
        current_image_encoded = face_recognition.face_encodings(current_image)
        name_person = image.split('.')[0]
        if len(current_image_encoded) > 0:
            known_face_encodings.append(list(current_image_encoded[0]))
            known_face_names.append(name_person)
        else:
            print(f'{name_person} não incluso.')
    return known_face_encodings, known_face_names


def format_data(ids, names):
    data = []
    for i in range(len(ids)):
        value = (str(ids[i]), names[i])
        data.append(value)
    return data


def do_load(milvus_client, mysql_cli):
    table_name = DEFAULT_TABLE

    vectors, names = extract_features()
    ids = milvus_client.insert(table_name, vectors)
    mysql_cli.create_mysql_table(table_name)
    mysql_cli.load_data_to_mysql(table_name, format_data(ids, names))


do_load(MILVUS_CLI, MYSQL_CLI)
