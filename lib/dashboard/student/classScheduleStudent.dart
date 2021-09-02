import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class ClassScheduleStudent extends StatefulWidget {
  const ClassScheduleStudent({Key? key}) : super(key: key);

  @override
  _ClassScheduleStudentState createState() => _ClassScheduleStudentState();
}

class _ClassScheduleStudentState extends State<ClassScheduleStudent> {

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

                  Container(
                    height: MediaQuery.of(context).size.height,
                    width: double.infinity,

                    child: GridView.count(
                      childAspectRatio: 5,
                      primary: false,
                      crossAxisSpacing: 10,
                      mainAxisSpacing: 10,
                      crossAxisCount: 8,
                      children: <Widget>[
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child: Text("       ")),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child: Text("Monday", style: TextStyle(color: Colors.white),)),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child:  Center(child: Text("Tuesday", style: TextStyle(color: Colors.white))),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child: Text("Wednesday", style: TextStyle(color: Colors.white))),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child: Text("Thursday", style: TextStyle(color: Colors.white))),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child: Text("Friday", style: TextStyle(color: Colors.white))),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child:  Text("Saturday", style: TextStyle(color: Colors.white))),
                          color: Colors.teal,
                        ),
                        Container(
                          height: 50,
                          width: 50,
                          child: Center(child: Text("Sunday", style: TextStyle(color: Colors.white))),
                          color: Colors.teal,
                        ),
                      ],
                    ),
                  ),

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