import re
from flask.wrappers import Response
import pymongo
from pymongo import MongoClient
from bson import Code
import flask
from flask import request, json
from flask_cors import CORS
import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = flask.Flask(__name__)
CORS(app)

CONNECTION_STRING = "mongodb+srv://Keshav:ThisIsAPassword@studentrecordshackathon.jgtfv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app.secret_key = "backspace.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "721856902092-25u0oog9p8vdvqd0m4c5riuso5l8pqk0.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


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
    "sid": "sid",
    "password": "password",
    "courses": {
        "course_name": {
            "course_teacher": "teacheremail",
            "assignment": {"date": {"sumission": ["answers"], "marks": "NA"}},
            "quiz": {"date": {"sumission": ["answers"], "marks": "NA"}},
        }, }
}

returnCodes = {
    "notPresent": {"error": "user email not present in use", "status": "error"},
    "alreadyPresent": {"error": "user email already in use", "status": "error"},
    "success": {"response": "changes made successfully", "status": "success"},
    "invalid_user": {"error": "user email or password incorrect", "status": "error"},
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
    course = teacher_db.find_one({"email": teacherEmail.lower()})[
        "courses"][courseName]
    quiz = course["schedule"]["quiz"]
    schedule.append(quiz.keys())
    return json.jsonify(schedule)


def getAssignmentSchedule(teacherEmail, courseName):
    schedule = []
    teacher_db, student_db = connectDb()
    course = teacher_db.find_one({"email": teacherEmail.lower()})[
        "courses"][courseName]
    assignment = course["schedule"]["assignment"]
    schedule.append(assignment.keys())
    return json.jsonify(schedule)


def getCalendarSchedule(teacherEmail, courseName):
    schedule = []
    teacher_db, student_db = connectDb()
    course = teacher_db.find_one({"email": teacherEmail.lower()})[
        "courses"][courseName]
    calender = course["schedule"]["calender"]
    schedule.append(calender.keys())
    return json.jsonify(schedule)


@app.route("/createNewTeacher", methods=["POST"])
def newTeacher():
    args = request.args
    password = args["password"]
    teacherEmail = args["teacherEmail"].lower()
    teacher_db, student_db = connectDb()
    if teacher_db.find_one({"email": teacherEmail}) != None:  # here
        return returnCodes["alreadyPresent"]
    else:
        teacher_db.insert_one(
            {"password": password, "email": teacherEmail})  # here
        return returnCodes["success"]


@app.route("/createNewStudent", methods=["POST", "GET"])
def newStudent():
    teacher_db, student_db = connectDb()
    args = request.args
    password = args["password"]
    studentEmail = args["studentEmail"].lower()
    if student_db.find_one({"email": studentEmail}) != None:
        return returnCodes["alreadyPresent"]
    else:
        student_db.insert_one({"email": studentEmail, "password": password})
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
            {"$set": {"courses.{}".format(courseName): {
                "course_teacher": teacherEmail}}},
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
        {"$set": {"courses.{}".format(courseName): {
            "course_teacher": teacherEmail}}},
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
    teacherEmail = args["email"].lower()
    teacher_db, student_db = connectDb()
    result = teacher_db.find_one({"email": teacherEmail})
    return json.jsonify(result["courses"].keys())


@app.route("/getCoursesStudent", methods=["GET"])
def getCoursesStudent():
    args = request.args
    studentEmail = args["email"].lower()
    teacher_db, student_db = connectDb()
    result = student_db.find_one({"email": studentEmail})
    answer = []
    for key in result["courses"].keys():
        answer.append(key)
    return json.jsonify(answer)


@app.route("/getScheduleStudent", methods=["GET"])
def getScheduleStudent():
    args = request.args
    studentEmail = args["studentEmail"].lower()
    teacher_db, student_db = connectDb()
    result = student_db.find_one({"email": studentEmail})["courses"]
    courses = result.keys()
    schedule = {}
    for course in courses:
        schedule[course]["assignment"] = getAssignmentSchedule(
            result[course]["course_teacher"], course)
        schedule[course]["quiz"] = getTestSchedule(
            result[course]["course_teacher"], course)
        schedule[course]["calendar"] = getCalendarSchedule(
            result[course]["course_teacher"], course)
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
        schedule[course]["assignment"] = getAssignmentSchedule(
            result[course]["course_teacher"], course)
        schedule[course]["quiz"] = getTestSchedule(
            result[course]["course_teacher"], course)
        schedule[course]["calendar"] = getCalendarSchedule(
            result[course]["course_teacher"], course)
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
                "courses.{}.schedule.{}".format(courseName, taskName): {time: data}
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


@app.route("/logInTeacher", methods=["GET"])
def loginTeacher():
    args = request.args
    password = args["password"]
    teacherEmail = args["teacherEmail"].lower()
    teacher_db, student_db = connectDb()
    teacher = teacher_db.find_one({"email": teacherEmail})
    if teacher == None:  # here
        return returnCodes["notPresent"]
    else:
        if (teacher["password"] == password):
            return returnCodes["success"]
        else:
            return returnCodes["invalid_user"]


@app.route("/logInStudent", methods=["GET"])
def loginStudent():
    args = request.args
    password = args["password"]
    studentEmail = args["studentEmail"].lower()
    teacher_db, student_db = connectDb()
    student = student_db.find_one({"email": studentEmail})
    if student == None:  # here
        return returnCodes["notPresent"]
    else:
        if (student["password"] == password):
            return returnCodes["success"]
        else:
            return returnCodes["invalid_user"]

# deploy comment
# app.run()

# attempt answers
# show attempted answers
# grade questions
# login
# see grades


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    print(id_info)

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()


@app.route("/protected_area")
@login_is_required
def protected_area():

    return f"Hello {session['email']}! <br/> <a href='/logout'><button>Logout</button></a>"
