import 'package:fliprapp/dashboard/teacher/classScheduleTeacher.dart';
import 'package:fliprapp/dashboard/teacher/coursesTeacher.dart';
import 'package:fliprapp/dataService.dart';
import 'package:fliprapp/main.dart';
import 'package:fliprapp/dashboard/student/classScheduleStudent.dart';
import 'package:fliprapp/dashboard/student/coursesStudent.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class Dashboard extends StatefulWidget {
  const Dashboard({Key? key}) : super(key: key);

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  DataShareService dataShareService = DataShareService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          child: Container(
            decoration: BoxDecoration(
                image: DecorationImage(
                    image: NetworkImage(
                        "https://as1.ftcdn.net/v2/jpg/01/17/13/88/500_F_117138897_ZIZkt6PA1THNv59GRsKLdfvTahvL126R.jpg"),
                    fit: BoxFit.cover)),
            //color: Colors.white,
            child: Center(
              child: Column(
                children: [
                  SizedBox(
                    height: 200,
                  ),

                  // Container(
                  //     padding: EdgeInsets.all(15),
                  //     color: Colors.black54,
                  //     height: 100,
                  //     width: 750,
                  //     child: Center(
                  //         child: Text("Welcome To BackSpace Classes", style: TextStyle(fontSize: 40, color: Colors.white),))
                  // ),
                  //
                  // SizedBox(height: 25),

                  Container(
                      padding: EdgeInsets.all(15),
                      color: Colors.black54,
                      height: 75,
                      width: 250,
                      child: Center(
                          child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.dashboard,
                            color: Colors.white,
                            size: 30,
                          ),
                          SizedBox(
                            width: 10,
                          ),
                          Text(
                            "Dashboard",
                            style: TextStyle(fontSize: 25, color: Colors.white),
                          ),
                        ],
                      ))),
                  SizedBox(height: 25),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton.icon(
                          onPressed: () {
                            if(dataShareService.getUserDetail() == "student"){
                              Navigator.push(context, MaterialPageRoute(builder: (context) => ClassScheduleStudent()));
                            }

                            else if(dataShareService.getUserDetail() == "teacher"){
                              Navigator.push(context, MaterialPageRoute(builder: (context) => ClassScheduleTeacher()));
                            }
                          },
                          label: Text(
                            "Class Schedules",
                            style: TextStyle(fontSize: 18),
                          ),
                          icon: Icon(Icons.schedule),
                          style: ElevatedButton.styleFrom(
                              primary: Colors.green,
                              minimumSize: Size(200, 200))),
                      SizedBox(
                        width: 20,
                      ),
                      ElevatedButton.icon(
                          onPressed: () {
                            if(dataShareService.getUserDetail() == "student"){
                              Navigator.push(context, MaterialPageRoute(builder: (context) => CoursesStudent()));
                            }

                            else if(dataShareService.getUserDetail() == "teacher"){
                              Navigator.push(context, MaterialPageRoute(builder: (context) => CoursesTeacher()));
                            }
                          },
                          label: Text(
                            "Courses",
                            style: TextStyle(fontSize: 18),
                          ),
                          icon: Icon(Icons.note),
                          style: ElevatedButton.styleFrom(
                              primary: Colors.blue,
                              minimumSize: Size(200, 200))),
                    ],
                  ),
                  SizedBox(height: 25),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton.icon(
                          onPressed: () {
                            // Navigator.push(context, MaterialPageRoute(builder: (
                            //     context) => SignUp())
                            // );
                          },
                          label: Text(
                            "Assessments",
                            style: TextStyle(fontSize: 18),
                          ),
                          icon: Icon(Icons.assessment),
                          style: ElevatedButton.styleFrom(
                              primary: Colors.yellow,
                              minimumSize: Size(200, 200))),
                      SizedBox(
                        width: 20,
                      ),
                      ElevatedButton.icon(
                          onPressed: () {
                            // Navigator.push(context, MaterialPageRoute(builder: (
                            //     context) => SignUp())
                            // );
                          },
                          label: Text(
                            "Tests/Quizzes",
                            style: TextStyle(fontSize: 18),
                          ),
                          icon: Icon(Icons.quiz),
                          style: ElevatedButton.styleFrom(
                              primary: Colors.red,
                              minimumSize: Size(200, 200))),
                    ],
                  ),
                  SizedBox(
                    height: 40,
                  ),
                  ElevatedButton.icon(
                      onPressed: () {
                        dataShareService.logout();
                        Navigator.push(context,
                            MaterialPageRoute(builder: (context) => MyApp()));
                      },
                      label: Text("Sign Out"),
                      icon: Icon(Icons.logout),
                      style: ElevatedButton.styleFrom(
                          primary: Colors.teal, minimumSize: Size(100, 50))),
                  SizedBox(
                    height: 200,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
