from flask.wrappers import Response
import pymongo
from pymongo import MongoClient
from bson import Code
import flask
from flask import request, json


app = flask.Flask(__name__)
CONNECTION_STRING = "mongodb+srv://Keshav:ThisIsAPassword@studentrecordshackathon.jgtfv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# def getCourseLink():
# def linkForLecture():
# def checkAssignment():
# def giveMarksAssignment():
# def checkTest():
# def giveMarksTest():

sample_teacher = {
    "name": "name",
    "email": "email",
    "courses": {
        "course_name": {
            "students": [],
            "schedule": {
                "assignment": {"date": ["questions"]},
                "quiz": {"date": ["questions"]},
                "calender": {"date": "link"},
            },
        },
    },
}
sample_student = {
    "name": "name",
    "email": "email",
    "course_name": {
        "course_teacher": "teacher_id",
        "assignment": {"date": {"sumission": ["answers"], "marks": "NA"}},
        "quiz": {"date": {"sumission": ["answers"], "marks": "NA"}},
    },
}

returnCodes = {
    "alreadyPresent": {"error": "user email already in use"},
    "success": {"response": "changes made successfully"},
}


def connectDb():
    client = MongoClient(CONNECTION_STRING)
    dbname = client["users"]
    teacher_db = dbname["teachers"]
    student_db = dbname["students"]
    return teacher_db, student_db


@app.route("/createNewTeacher", methods=["POST"])
def newTeacher():
    args = request.args
    teacherName = args["teacherName"]
    teacherEmail = args["teacherEmail"]
    teacher_db, student_db = connectDb()
    # Commented for testing
    # if teacher_db.find_one({"email": teacherEmail}) != None:
    #     return returnCodes["alreadyPresent"]
    # else:
    teacher_db.insert_one({"name": teacherName, "email": teacherEmail})
    return returnCodes["success"]


@app.route("/createNewStudent", methods=["POST"])
def newStudent():
    teacher_db, student_db = connectDb()
    args = request.args
    studentName = args["studentName"]
    studentEmail = args["studentEmail"]
    # Commented for testing
    # if student_db.find_one({"email": studentEmail}) != None:
    #     return returnCodes["alreadyPresent"]
    # else:
    student_db.insert_one({"name": studentName, "email": studentEmail})
    return returnCodes["success"]


@app.route("/getTeacherId", methods=["GET"])
def getTeacherId():
    args = request.args
    teacherEmail = args["teacherEmail"]

    teacher_db, student_db = connectDb()
    return returnCodes["success"]


@app.route("/getStudentId", methods=["GET"])
def getStudentId(studentEmail):
    args = request.args
    studentEmail = args["studentEmail"]
    teacher_db, student_db = connectDb()
    return returnCodes["success"]


@app.route("/createNewCourse", methods=["POST"])
def createNewCourse():
    args = request.args
    teacherId = args["teacherId"]
    courseName = args["courseName"]
    data = request.get_json()
    schedule = data["schedule"]
    students = data["students"]
    teacher_db, student_db = connectDb()
    student_arr = []
    if len(students) != 0:
        for student in students:
            student_id = student_db.find_one({"email": student})["_id"]
            student_arr.append(student_id)
        student_db.update_many(
            {"_id": {"$in": student_arr}},
            {"$set": {courseName: {"course_teacher": teacherId}}},
        )
    newSchedule = schedule  # LOTTTTT OF MODification here
    teacher_db.update_one(
        {"_id": teacherId},
        {
            "$set": {
                "courses": {
                    courseName: {
                        "schedule": {"calender": newSchedule},
                        "students": student_arr,
                    }
                }
            }
        },
    )
    return returnCodes["success"]


@app.route("/addStudentToCourse", methods=["POST"])
def addStudentToCourse():
    args = request.args
    teacherId = args["teacherId"]
    courseName = args["courseName"]
    studentId = args["studentId"]
    teacher_db, student_db = connectDb()
    student_db.update_one(
        {"_id": studentId},
        {"$set": {courseName: {"course_teacher": teacherId}}},
    )
    teacher_db.update_one(
        {"_id": teacherId},
        {
            "$push": {
                "courses": {
                    courseName: {
                        "students": studentId,
                    }
                }
            }
        },
    )
    return returnCodes["success"]


@app.route("/getCoursesList", methods=["GET"])
def getCoursesList():
    args = request.args
    teacherId = args["teacherId"]
    teacher_db, student_db = connectDb()
    result = teacher_db.find_one({"_id": teacherId})
    courses = []
    for course in result["courses"]:
        courses.append(course)
    return courses


@app.route("/addTask", methods=["POST"])
def addTask():
    # taskname can be quiz or assignment
    args = request.args
    teacherId = args["teacherId"]
    courseName = args["courseName"]
    time = args["time"]
    taskName = args["taskName"]
    data = request.get_json()
    questions = data
    teacher_db, student_db = connectDb()
    teacher_db.update_one(
        {"_id": teacherId},
        {
            "$set": {
                "courses": {courseName: {"schedule": {taskName: {time: questions}}}}
            }
        },
    )
    return returnCodes["success"]


# def addStudentsCourse(emailId):
#     teacher_db, student_db = connectDb()
#     student_id = student_db.find_one({"email": emailId})["_id"]


app.run(port="5001")
