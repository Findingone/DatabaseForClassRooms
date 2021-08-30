import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class CoursesTeacher extends StatefulWidget {
  const CoursesTeacher({Key? key}) : super(key: key);

  @override
  _CoursesTeacherState createState() => _CoursesTeacherState();
}

class _CoursesTeacherState extends State<CoursesTeacher> {

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
                      width: 300,
                      child: Center(
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.dashboard, color: Colors.white, size: 30,),
                              SizedBox(width: 10,),
                              Text("Courses", style: TextStyle(fontSize: 25, color: Colors.white),),
                            ],
                          )
                      )
                  ),
                  SizedBox(height: 20,),


                  SizedBox(height: 200,),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}