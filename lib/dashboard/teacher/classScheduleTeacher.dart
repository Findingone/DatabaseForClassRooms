import 'package:fliprapp/dataService.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class ClassScheduleTeacher extends StatefulWidget {
  const ClassScheduleTeacher({Key? key}) : super(key: key);

  @override
  _ClassScheduleTeacherState createState() => _ClassScheduleTeacherState();
}

class _ClassScheduleTeacherState extends State<ClassScheduleTeacher> {

  TextEditingController Day = TextEditingController();
  TextEditingController Time = TextEditingController();
  TextEditingController Subject = TextEditingController();

  String FDay = "";
  String FTime = "";
  String FSubject = "";

  final _formKey = GlobalKey<FormState>();

  DataShareService dss = new DataShareService();

  setClass(time, link) {
    dss.scheduleClass(time, link);
  }

  getClass() {
    return dss.getScheduleClassesTeacher();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Container(
              decoration: BoxDecoration(
                image: DecorationImage(
                    image: NetworkImage(
                        "https://as1.ftcdn.net/v2/jpg/01/17/13/88/500_F_117138897_ZIZkt6PA1THNv59GRsKLdfvTahvL126R.jpg"),
                    fit: BoxFit.cover),),
              child: Center(
                child: Column(
                  children: [
                    SizedBox(height: 200,),

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
                        width: 400,
                        child: Center(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.dashboard, color: Colors.white, size: 30,),
                                SizedBox(width: 10,),
                                Text("Class Schedules", style: TextStyle(fontSize: 25, color: Colors.white),),
                              ],
                            )
                        )
                    ),

                    SizedBox(height: 20,),

                    Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Container(
                            width: 500,
                            child: TextFormField(
                              style: TextStyle(color: Colors.black),
                              decoration: InputDecoration(
                                  fillColor: Colors.white,
                                  filled: true,
                                  border: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  focusedBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  enabledBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  errorBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  focusedErrorBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  icon: Icon(
                                    Icons.date_range,
                                    color: Colors.blueGrey,
                                  ),
                                  hintText: 'Day of Class',
                                  hintStyle: TextStyle(color: Colors.blueGrey)),
                              controller: Day,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Enter a Day';
                                }
                                return null;
                              },
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          Container(
                            width: 500,
                            child: TextFormField(
                              style: TextStyle(color: Colors.black),
                              decoration: InputDecoration(
                                  fillColor: Colors.white,
                                  filled: true,
                                  border: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  focusedBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  enabledBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  errorBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  focusedErrorBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  icon: Icon(
                                    Icons.access_time,
                                    color: Colors.blueGrey,
                                  ),
                                  hintText: 'Time Of Class',
                                  hintStyle: TextStyle(color: Colors.blueGrey)),
                              // obscureText: true,
                              controller: Time,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please Enter a Time';
                                }
                                return null;
                              },
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),

                          Container(
                            width: 500,
                            child: TextFormField(
                              style: TextStyle(color: Colors.black),
                              decoration: InputDecoration(
                                  fillColor: Colors.white,
                                  filled: true,
                                  border: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  focusedBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  enabledBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  errorBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  focusedErrorBorder: OutlineInputBorder(
                                      borderSide:
                                      BorderSide(color: Colors.blueGrey)),
                                  icon: Icon(
                                    Icons.subject,
                                    color: Colors.blueGrey,
                                  ),
                                  hintText: 'Name Of Subject',
                                  hintStyle: TextStyle(color: Colors.blueGrey)),
                              // obscureText: true,
                              controller: Subject,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please Enter a Subject';
                                }
                                return null;
                              },
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),

                          ElevatedButton.icon(
                              onPressed: () {
                                if (_formKey.currentState!.validate()) {
                                  print("successful");
                                  FDay = Day.toString();
                                  FTime = Time.toString();
                                  FSubject = Subject.toString();
                                }
                              },
                              label: Text("Add Classes"),
                              icon: Icon(Icons.add),
                              style: ElevatedButton.styleFrom(
                                  primary: Colors.blueGrey,
                                  minimumSize: Size(100, 50))),
                      ],
                    ),

                    SizedBox(height: 20,),

                    Container(

                    ),

                    SizedBox(height: 200,),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}