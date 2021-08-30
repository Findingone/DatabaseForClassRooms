import 'package:fliprapp/signup/signupStudent.dart';
import 'package:fliprapp/signup/signupTeacher.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class SignUp extends StatefulWidget {
  const SignUp({Key? key}) : super(key: key);

  @override
  _SignUpState createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Container(
          decoration: BoxDecoration(
              image: DecorationImage(
                  image: NetworkImage(
                      "https://as1.ftcdn.net/v2/jpg/01/17/13/88/500_F_117138897_ZIZkt6PA1THNv59GRsKLdfvTahvL126R.jpg"),
                  fit: BoxFit.cover)),
          child: Center(
            child: Column(
              children: [
                SizedBox(
                  height: 200,
                ),
                Container(
                    padding: EdgeInsets.all(15),
                    color: Colors.black54,
                    height: 100,
                    width: 750,
                    child: Center(
                        child: Text(
                          "Welcome To BackSpace Classes",
                          style: TextStyle(fontSize: 40, color: Colors.white),
                        ))),
                SizedBox(
                  height: 25,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton.icon(
                        onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (
                              context) => SignUp_Teacher())
                          );
                        },
                        label: Text("Sign Up As A Teacher"),
                        icon: Icon(Icons.school),
                        style: ElevatedButton.styleFrom(
                            primary: Colors.blueGrey,
                            minimumSize: Size(100, 50))),
                    SizedBox(
                      width: 20,
                    ),
                    ElevatedButton.icon(
                        onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (
                              context) => SignUp_Student())
                          );
                        },
                        label: Text("Sign Up As A Student"),
                        icon: Icon(Icons.account_circle),
                        style: ElevatedButton.styleFrom(
                            primary: Colors.blueGrey,
                            minimumSize: Size(100, 50))),
                  ],
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}