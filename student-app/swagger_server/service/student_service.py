import json
import os

from swagger_server.encoder import JSONEncoder

'''
from tinydb import TinyDB, Query

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)
'''

from pymongo import MongoClient

url = os.getenv("MONGO_URI")
mongo_client = MongoClient(url)
db = mongo_client["student_db"]
student_collection = db["students"]
idx = 0


def add(student=None):
    global idx

    if student.student_id is None:
        student.student_id = idx

    existing_id = student_collection.find_one({'student_id': student.student_id})
    existing_names = student_collection.find_one({'first_name': student.first_name, 'last_name': student.last_name})

    if existing_id is not None or existing_names is not None:
        return f"Already exists", 409
    else:
        print("Adding student...")
        insert_result = student_collection.insert_one(json.loads(json.dumps(student, cls=JSONEncoder)))
        idx += 1
        return f"{student.student_id}"


def get_by_id(student_id=None, subject=None):
    student = student_collection.find_one({'student_id': student_id})

    if student is None:
        return 'not found', 404

    del student["_id"]
    return json.loads(json.dumps(student, cls=JSONEncoder))


def delete(student_id=None):
    student = student_collection.find_one({'student_id': student_id})
    if student is None:
        return 'not found', 404

    result = student_collection.delete_one({'student_id': student_id})

    if result.deleted_count == 0:
        return 'not found', 404

    return student_id
