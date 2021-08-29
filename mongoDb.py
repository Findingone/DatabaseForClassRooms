import pymongo
from pymongo import MongoClient
from bson import Code

CONNECTION_STRING = "mongodb+srv://Keshav:ThisIsAPassword@studentrecordshackathon.jgtfv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# def getCourseLink():
# def uploadAssignment():
# def uploadTest():
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
        }
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


def connectDb():
    client = MongoClient(CONNECTION_STRING)
    dbname = client["users"]
    teacher_db = dbname["teachers"]
    student_db = dbname["students"]
    return teacher_db, student_db


def newTeacher(teacherName, teacherEmail):
    teacher_db, student_db = connectDb()
    check = teacher_db.find_one({"email":teacherEmail})
    if(check == None):
        teacher_db.insert_one({"name": teacherName, "email": teacherEmail})
        return teacher_db.find_one({"email": teacherEmail})["_id"]
    else:
        return "AlreadyPresent" 

    

def newStudent(studentName, studentEmail):
    teacher_db, student_db = connectDb()
    check = student_db.find_one({"email":studentEmail})
    if(check == None):
        student_db.insert_one({"name": studentName, "email": studentEmail})
        return student_db.find_one({"email": studentEmail})["_id"]
    else:
        return "AlreadyPresent"
    

def getTeacherId(teacherEmail):
    teacher_db, student_db = connectDb()
    return teacher_db.find_one({"email": teacherEmail})["_id"]


def getStudentId(studentEmail):
    teacher_db, student_db = connectDb()
    return student_db.find_one({"email": studentEmail})["_id"]


def createNewCourse(teacherId, courseName, schedule, students):
    teacher_db, student_db = connectDb()
    if len(students) != 0:
        student_arr = []
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


def addTask(teacherId, course, time, questions, taskName):
    # taskname can be quiz or assignment
    teacher_db, student_db = connectDb()
    teacher_db.update_one(
        {"_id": teacherId},
        {"$set": {"courses": {course: {"schedule": {taskName: {time: questions}}}}}},
    )


def addStudentToCourse(teacherId, courseName, studentId):
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


def getCoursesList(teacherId):
    teacher_db, student_db = connectDb()
    map = Code("function() { for (var key in this) { emit(key, null); } }")
    reduce = Code("function(key, stuff) { return null; }")
    result = teacher_db.find_one({"_id": teacherId})["courses"].map_reduce(
        map, reduce, "myresults"
    )
    return result.distinct("_id")


# def addStudentsCourse(emailId):
#     teacher_db, student_db = connectDb()
#     student_id = student_db.find_one({"email": emailId})["_id"]


teacher_id = newTeacher("keshav", "example")
createNewCourse(teacher_id, "hindi", "schedule", [])
courses = getCoursesList(teacher_id)
print(courses)
