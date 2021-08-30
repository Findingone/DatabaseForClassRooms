from flask.wrappers import Response
import pymongo
from pymongo import MongoClient
from bson import Code
import flask
from flask import request, json
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
CONNECTION_STRING = "mongodb+srv://Keshav:ThisIsAPassword@studentrecordshackathon.jgtfv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

sample_teacher = {
    "name": "name",
    "email": "email",
    "password": "password",
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
    "password": "password",
    "courses":{
    "course_name": {
        "course_teacher": "teacheremail",
        "assignment": {"date": {"sumission": ["answers"], "marks": "NA"}},
        "quiz": {"date": {"sumission": ["answers"], "marks": "NA"}},
    },}
}

returnCodes = {
    "alreadyPresent": {"error": "user email already in use", "status": "error"},
    "success": {"response": "changes made successfully", "status": "success"},
}


def connectDb():
    client = MongoClient(CONNECTION_STRING)
    dbname = client["users"]
    teacher_db = dbname["teachers"]
    student_db = dbname["students"]
    return teacher_db, student_db

def getTestSchedule(teacherEmail, courseName):
    schedule = []
    teacher_db, student_db = connectDb()
    course = teacher_db.find_one({"email": teacherEmail.lower()})["courses"][courseName]
    quiz = course["schedule"]["quiz"]
    schedule.append(quiz.keys())
    return json.jsonify(schedule)

def getAssignmentSchedule(teacherEmail, courseName):
    schedule = []
    teacher_db, student_db = connectDb()
    course = teacher_db.find_one({"email": teacherEmail.lower()})["courses"][courseName]
    assignment = course["schedule"]["assignment"]
    schedule.append(assignment.keys())
    return json.jsonify(schedule)

def getCalendarSchedule(teacherEmail, courseName):
    schedule = []
    teacher_db, student_db = connectDb()
    course = teacher_db.find_one({"email": teacherEmail.lower()})["courses"][courseName]
    calender = course["schedule"]["calender"]
    schedule.append(calender.keys())
    return json.jsonify(schedule)    


@app.route("/createNewTeacher", methods=["POST"])
def newTeacher():
    args = request.args
    teacherName = args["teacherName"]
    teacherEmail = args["teacherEmail"].lower()
    teacher_db, student_db = connectDb()
    if teacher_db.find_one({"email": teacherEmail}) != None: #here
        return returnCodes["alreadyPresent"]
    else:
        teacher_db.insert_one({"name": teacherName, "email": teacherEmail})##here
        return returnCodes["success"]


@app.route("/createNewStudent", methods=["POST"])
def newStudent():
    teacher_db, student_db = connectDb()
    args = request.args
    studentName = args["studentName"]
    studentEmail = args["studentEmail"].lower()
    if student_db.find_one({"email": studentEmail}) != None:
        return returnCodes["alreadyPresent"]
    else:
        student_db.insert_one({"name": studentName, "email": studentEmail})#here
        return returnCodes["success"]


@app.route("/createNewCourse", methods=["POST"])
def createNewCourse():
    args = request.args
    teacherEmail = args["teacherEmail"].lower()
    courseName = args["courseName"]
    data = request.get_json()
    schedule = data["schedule"]
    students = data["students"]
    teacher_db, student_db = connectDb() 
    if len(students) != 0:
        student_arr = []
        for student in students:
            student_arr.append(student.lower())
        students = student_arr
        student_db.update_many(
            {"email": {"$in": students}},
            {"$set": {"courses.{}".format(courseName): {"course_teacher": teacherEmail}}},
        )
    newSchedule = schedule  # LOTTTTT OF MODification here
    teacher_db.update_one(
        {"email": teacherEmail},
        {
            "$set": {
                "courses.{}".format(courseName): {
                        "schedule": {"calender": newSchedule},
                        "students": students,
                }
            }
        },
    )
    return returnCodes["success"]


@app.route("/addStudentToCourse", methods=["POST"])
def addStudentToCourse():
    args = request.args
    teacherEmail = args["teacherEmail"].lower()
    courseName = args["courseName"]
    studentEmail = args["studentEmail"].lower()
    teacher_db, student_db = connectDb()
    student_db.update_one(
        {"email": studentEmail},
        {"$set": {"courses.{}".format(courseName): {"course_teacher": teacherEmail}}},
    )
    teacher_db.update_one(
        {"email": teacherEmail},
        {
            "$push": {
                "courses.{}".format(courseName): {
                        "students": studentEmail,
                }
            }
        }
    )
    return returnCodes["success"]


@app.route("/getCoursesTeacher", methods=["GET"])
def getCoursesTeacher():
    args = request.args
    teacherEmail = args["teacherEmail"].lower()
    teacher_db, student_db = connectDb()
    result = teacher_db.find_one({"email": teacherEmail})
    return json.jsonify(result["courses"].keys())

@app.route("/getCoursesStudent", methods=["GET"])
def getCoursesStudent():
    args = request.args
    studentEmail = args["studentEmail"].lower()
    teacher_db, student_db = connectDb()
    result = student_db.find_one({"email": studentEmail})
    return json.jsonify(result["courses"].keys())


@app.route("/getScheduleStudent", methods=["GET"])
def getScheduleStudent():
    args = request.args
    studentEmail = args["studentEmail"].lower()
    teacher_db, student_db = connectDb()
    result = student_db.find_one({"email": studentEmail})["courses"]
    courses = result.keys()
    schedule = {}
    for course in courses:
        schedule[course]["assignment"] = getAssignmentSchedule(result[course]["course_teacher"], course)
        schedule[course]["quiz"] = getTestSchedule(result[course]["course_teacher"], course)
        schedule[course]["calendar"] = getCalendarSchedule(result[course]["course_teacher"], course)
    return schedule

@app.route("/getScheduleTeacher", methods=["GET"])
def getScheduleTeacher():
    args = request.args
    teacherEmail = args["teacherEmail"].lower()
    teacher_db, student_db = connectDb()
    result = teacher_db.find_one({"email": teacherEmail})["courses"]
    courses = result.keys()
    schedule = {}
    for course in courses:
        schedule[course]["assignment"] = getAssignmentSchedule(result[course]["course_teacher"], course)
        schedule[course]["quiz"] = getTestSchedule(result[course]["course_teacher"], course)
        schedule[course]["calendar"] = getCalendarSchedule(result[course]["course_teacher"], course)
    return schedule



@app.route("/addTask", methods=["POST"])
def addTask():
    # taskname can be quiz or assignment
    args = request.args
    teacherEmail = args["teacherEmail"].lower()
    courseName = args["courseName"]
    time = args["time"]
    taskName = args["taskName"]
    data = request.get_json()
    teacher_db, student_db = connectDb()
    teacher_db.update_one(
        {"email": teacherEmail},
        {
            "$set": {
                "courses.{}.schedule.{}".format(courseName,taskName): {time: data}
            }
        },
    )
    return returnCodes["success"]


@app.route("/getQuestions", methods=["POST"])
def getQuestions():
    args = request.args
    task = args["task"]
    date = args["date"]
    courseName = args["courseName"]
    courseTeacher = args["courseTeacher"]
    teacher_db, student_db = connectDb()
    data = teacher_db.find_one({"email": courseTeacher})
    questions = data["courses"][courseName]["schedule"][task][date]
    return json.jsonify(questions)



## deploy comment
# app.run()

# attempt answers
# show attempted answers
# grade questions
# login
# see grades