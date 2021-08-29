import os

import sqlite3
import csv
from datetime import datetime

import flask
from flask import request, json
import pathlib
from flask.wrappers import Response

from werkzeug.utils import secure_filename
from werkzeug.wrappers import response

app = flask.Flask(__name__)
Database = "DataBase.db"
returnCodes = {
    "success": {
        "status": 200,
    }
}


def readCsv(filename):
    with open(filename) as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile)
        data = []
        for row in spamreader:
            data.append(row)
    return data


def saveIncomingFile(request, name):
    # get institute code
    args = request.args
    instituteCode = args["instituteCode"]

    # name to save incoming file
    now = datetime.now()
    dt_string = now.strftime("'%d/%m/%Y %H:%M:%S'")

    file_dir = os.path.join("uploads", instituteCode)
    # create directory to save files
    pathlib.Path(file_dir).mkdir(exist_ok=True)
    fname = os.path.join(name + dt_string + ".csv")

    # get uploaded file and save it
    uploaded_file = request.files["file"]
    fname = secure_filename(fname)
    file_name = os.path.join(file_dir, fname)
    if uploaded_file.filename != "":
        uploaded_file.save(file_name)
    return instituteCode, file_name


@app.route("/addProfTable", methods=["POST"])
def addProfTable():

    instituteCode, file_name = saveIncomingFile(request, "addProf")
    # read the uploaded file
    data = readCsv(file_name)

    # create folder for database
    pathlib.Path(os.path.join("database", instituteCode)).mkdir(exist_ok=True)
    # handle sqlite
    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()

    sql_command = """CREATE TABLE {}teachingFaculty (
        ID varchar unique,
        Name varchar,
        Email varchar,
        PhotoLink VARCHAR
    );""".format(
        instituteCode
    )
    crsr.execute(sql_command)
    for prof in data:
        sql_command = """INSERT INTO {}teachingFaculty VALUES ('{}' , '{}' , '{}', 'NA' )""".format(
            instituteCode, prof[0], prof[1], prof[2]
        )
        crsr.execute(sql_command)
        sql_command = "CREATE TABLE {}teacher{}(courseName VARCHAR unique)".format(
            instituteCode, prof[0]
        )
        crsr.execute(sql_command)
        for j in range(len(prof) - 3):
            sql_command = "INSERT or IGNORE INTO {}teacher{} VALUES('{}')".format(
                instituteCode, prof[0], prof[j + 3]
            )
            crsr.execute(sql_command)

    database.commit()

    database.close()
    return returnCodes["success"]


@app.route("/updateProfTable", methods=["POST"])
def updateProfTable():
    instituteCode, file_name = saveIncomingFile(request, "updateProf")
    # read the uploaded file
    data = readCsv(file_name)

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()

    for prof in data:
        sql_command = """INSERT OR IGNORE INTO {}teachingFaculty VALUES ('{}' , '{}' , '{}', 'NA' )""".format(
            instituteCode, prof[0], prof[1], prof[2]
        )
        crsr.execute(sql_command)
        sql_command = (
            "CREATE TABLE IF NOT EXISTS {}teacher{}(courseName VARCHAR unique)".format(
                instituteCode, prof[0]
            )
        )
        crsr.execute(sql_command)
        for j in range(len(prof) - 3):
            sql_command = "INSERT or IGNORE INTO {}teacher{} VALUES('{}')".format(
                instituteCode, prof[0], prof[j + 3]
            )
            crsr.execute(sql_command)

    database.commit()
    database.close()
    return returnCodes["success"]


@app.route("/addStudentsAndCourses", methods=["POST"])
def addStudentsAndCourses():
    instituteCode, file_name = saveIncomingFile(request, "addStudents")
    # read the uploaded file
    data = readCsv(file_name)

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()
    sql_command = "CREATE TABLE {}courses (courseName VARCHAR unique)".format(
        instituteCode
    )
    crsr.execute(sql_command)
    for student in data:
        for i in range(7):
            course = student[i + 3]
            if course != "":
                sql_command = "CREATE TABLE IF NOT EXISTS {}{} (RollNo VARCHAR unique, Name VARCHAR, BATCH VARCHAR) ".format(
                    instituteCode, course
                )
                crsr.execute(sql_command)

                sql_command = "INSERT INTO {}{} VALUES ({}, '{}', '{}')".format(
                    instituteCode, course, student[0], student[1], student[2]
                )
                crsr.execute(sql_command)

                sql_command = "INSERT or IGNORE INTO {}courses VALUES ('{}')".format(
                    instituteCode, course
                )
                crsr.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS {}students (RollNo varchar unique, Name varchar,batch varchar, FaceData BOOL )""".format(
            instituteCode
        )
        crsr.execute(sql_command)
        sql_command = "INSERT INTO {}students VALUES ({}, '{}' , '{}', 0)".format(
            instituteCode, student[0], student[1], student[2]
        )
        crsr.execute(sql_command)

        sql_command = "CREATE TABLE IF NOT EXISTS {}{} ( Course varchar, Active Bool, Attendance varchar) ".format(
            instituteCode, student[0]
        )
        crsr.execute(sql_command)

        for j in range(7):
            studyCourse = student[j + 3]
            if studyCourse != "":
                sql_command = "INSERT INTO {}{} VALUES('{}', 1, 'NA')".format(
                    instituteCode, student[0], studyCourse
                )
                crsr.execute(sql_command)

    database.commit()

    database.close()
    return returnCodes["success"]


@app.route("/markAttendance", methods=["POST"])
def markAttendance():
    args = request.args
    instituteCode = args["instituteCode"]
    course = args["course"]
    data = request.get_json()
    students = data["students"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()
    sql_command = "Create table temp(RollNo varchar)"
    crsr.execute(sql_command)
    for student in students:
        sql_command = "INSERT INTO temp VALUES('{}')".format(student)
        crsr.execute(sql_command)

    now = datetime.now()
    dt_string = now.strftime("'%d/%m/%Y %H:%M:%S'")

    sql_command = "Alter Table {}{} Add {} Bool Default '0'".format(
        instituteCode, course, dt_string
    )
    crsr.execute(sql_command)

    sql_command = "update {}{} set {} = 1 where RollNo in temp".format(
        instituteCode, course, dt_string
    )
    crsr.execute(sql_command)

    sql_command = "DROP TABLE temp"
    crsr.execute(sql_command)

    # time.sleep(1)

    database.commit()
    database.close()
    return returnCodes["success"]


@app.route("/addStudentCourse", methods=["POST"])
def addStudentCourse():
    args = request.args
    instituteCode = args["instituteCode"]
    studentId = args["studentId"]
    courseName = args["courseName"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()

    sql_command = "INSERT INTO {}{} VALUES('{}', '1' , 'NA')".format(
        instituteCode, studentId, courseName
    )
    crsr.execute(sql_command)
    sql_command = "select Name,batch from {}students where RollNo = '{}'".format(
        instituteCode, studentId
    )
    crsr.execute(sql_command)
    ans = crsr.fetchall()
    ans = ans[0]
    sql_command = "INSERT INTO {}{} VALUES('{}', '{}' , '{}')".format(
        instituteCode, courseName, studentId, ans[0], ans[1]
    )
    crsr.execute(sql_command)

    database.commit()
    database.close()
    return returnCodes["success"]


@app.route("/removeProf", methods=["POST"])
def removeProf():
    args = request.args
    instituteCode = args["instituteCode"]
    profId = args["profId"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()

    sql_command = "Delete from {}teachingFaculty where ID={}".format(
        instituteCode, profId
    )
    crsr.execute(sql_command)
    sql_command = "Drop table {}teacher{}".format(instituteCode, profId)
    crsr.execute(sql_command)
    database.commit()
    database.close()
    return returnCodes["success"]


@app.route("/getStudentAttendance", methods=["GET"])
def getStudentAttendance():
    args = request.args
    instituteCode = args["instituteCode"]
    rollNo = args["rollNo"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()

    sql_command = "select * from {}{} ".format(instituteCode, rollNo)
    crsr.execute(sql_command)
    courses = crsr.fetchall()
    data = []
    for course in courses:
        if course[1] == 0:
            print(course[2])
        else:
            sql_command = "select * from {}{} where RollNo = '{}'".format(
                instituteCode, course[0], rollNo
            )
            crsr.execute(sql_command)
            attendanceRecord = crsr.fetchall()
            attendanceRecord = attendanceRecord[0]
            attendance = 0
            for j in range(len(attendanceRecord) - 3):
                attendance += attendanceRecord[j + 3]
            if len(attendanceRecord) > 3:
                data.append(
                    course[0]
                    + ": "
                    + str(attendance / (len(attendanceRecord) - 3) * 100)
                    + "%"
                )
    database.close()
    return app.response_class(
        response=json.dumps(data),
        status=200,
    )


@app.route("/profAddCourse", methods=["POST"])
def profAddCourse():
    args = request.args
    instituteCode = args["instituteCode"]
    profId = args["profId"]
    courseName = args["courseName"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()
    sql_command = "INSERT INTO {}teacher{} VALUES('{}')".format(
        instituteCode, profId, courseName
    )
    crsr.execute(sql_command)

    database.commit()
    database.close()
    return returnCodes["success"]


@app.route("/profRemoveCourse", methods=["POST"])
def profRemoveCourse():
    args = request.args
    instituteCode = args["instituteCode"]
    profId = args["profId"]
    courseName = args["courseName"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()
    sql_command = "DELETE from {}teacher{} where courseName = '{}'".format(
        instituteCode, profId, courseName
    )
    crsr.execute(sql_command)

    database.commit()
    database.close()
    return returnCodes["success"]


@app.route("/updateSemester", methods=["POST"])
def updateSemester():
    args = request.args
    instituteCode = args["instituteCode"]

    database = sqlite3.connect(os.path.join("database", instituteCode, Database))
    crsr = database.cursor()

    sql_command = "select RollNo from {}students".format(instituteCode)
    crsr.execute(sql_command)
    rollNumbers = crsr.fetchall()
    for i in rollNumbers:
        rollNumber = i[0]
        sql_command = "select course from {}{} where active = 1".format(
            instituteCode, rollNumber
        )
        crsr.execute(sql_command)
        courses = crsr.fetchall()
        for course in courses:
            sql_command = "select * from {}{} where RollNo = '{}'".format(
                instituteCode, course[0], rollNumber
            )
            crsr.execute(sql_command)
            details = crsr.fetchall()
            attendance = 0
            for i in range(len(details[0]) - 3):
                attendance += details[0][i + 3]
            if len(details[0]) != 3:
                attendance = (attendance / (len(details[0]) - 3)) * 100
                sql_command = "update {}{} set Active = 0 , Attendance = {}".format(
                    instituteCode, rollNumber, attendance
                )
                crsr.execute(sql_command)
    sql_command = "select courseName from {}courses".format(instituteCode)
    crsr.execute(sql_command)
    courses = crsr.fetchall()
    for course in courses:
        sql_command = "DROP TABLE {}{}".format(instituteCode, course[0])
        crsr.execute(sql_command)

    sql_command = "DROP TABLE {}courses".format(instituteCode)
    crsr.execute(sql_command)

    sql_command = "select ID from {}teachingFaculty".format(instituteCode)
    crsr.execute(sql_command)
    professors = crsr.fetchall()
    for professor in professors:
        sql_command = "DROP TABLE {}teacher{}".format(instituteCode, professor[0])
        crsr.execute(sql_command)

    database.commit()
    database.close()
    return returnCodes["success"]


app.run(port="5001", debug=True)
