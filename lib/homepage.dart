import 'package:fliprapp/login/login.dart';
import 'package:fliprapp/signup/signup.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class Homepage extends StatefulWidget {
  const Homepage({Key? key}) : super(key: key);

  @override
  _HomepageState createState() => _HomepageState();
}

class _HomepageState extends State<Homepage> {


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
                          child: Text("Welcome To BackSpace Classes", style: TextStyle(fontSize: 40, color: Colors.white),))),
                  SizedBox(
                    height: 25,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton.icon(
                          onPressed: () {
                            Navigator.push(context, MaterialPageRoute(builder: (
                                context) => SignUp())
                            );
                          },
                          label: Text("Sign Up"),
                          icon: Icon(Icons.app_registration),
                          style: ElevatedButton.styleFrom(
                              primary: Colors.blueGrey,
                              minimumSize: Size(100, 50))
                      ),

                      SizedBox(width: 20,),

                      ElevatedButton.icon(
                          onPressed: () {
                            Navigator.push(context, MaterialPageRoute(builder: (
                                context) => LogIn())
                            );
                          },
                          label: Text("Log In"),
                          icon: Icon(Icons.login),
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
      ),
    );
  }
}