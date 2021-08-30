import 'package:fliprapp/dataService.dart';
import 'package:fliprapp/homepage.dart';
import 'package:fliprapp/main.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:ui';

class LogIn_Student extends StatefulWidget {
  const LogIn_Student({Key? key}) : super(key: key);

  @override
  _LogIn_StudentState createState() => _LogIn_StudentState();
}

class _LogIn_StudentState extends State<LogIn_Student> {
  final _formKey = GlobalKey<FormState>();
  TextEditingController password = TextEditingController();
  TextEditingController email = TextEditingController();
  DataShareService dataService = DataShareService();

  login() {
    bool loginState =
        dataService.loginStudent(email.text.trim(), password.text.trim());
    if (loginState) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => MyApp()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: SafeArea(
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
                        height: 75,
                        width: 500,
                        child: Center(
                            child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.account_circle,
                              color: Colors.white,
                              size: 40,
                            ),
                            SizedBox(
                              width: 15,
                            ),
                            Text(
                              "Log In As A Student",
                              style:
                                  TextStyle(fontSize: 30, color: Colors.white),
                            ),
                          ],
                        ))),
                    SizedBox(
                      height: 25,
                    ),
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
                                  Icons.email,
                                  color: Colors.blueGrey,
                                ),
                                hintText: 'What is your Email ID?',
                                hintStyle: TextStyle(color: Colors.blueGrey)),
                            controller: email,
                            validator: (value) {
                              if (value!.isEmpty) {
                                return 'Enter an Email';
                              }
                              if (!RegExp(
                                      "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+.[a-z]")
                                  .hasMatch(value)) {
                                return 'Enter a Valid Email';
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
                                  Icons.password,
                                  color: Colors.blueGrey,
                                ),
                                hintText: 'What is your Password?',
                                hintStyle: TextStyle(color: Colors.blueGrey)),
                            obscureText: true,
                            controller: password,
                            validator: (value) {
                              if (value!.length <= 6) {
                                return 'Please Enter a Password more than 6 characters long';
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
                              }
                              login();
                            },
                            label: Text("Log In"),
                            icon: Icon(Icons.app_registration),
                            style: ElevatedButton.styleFrom(
                                primary: Colors.blueGrey,
                                minimumSize: Size(100, 50))),
                        SizedBox(
                          height: 20,
                        ),
                        ElevatedButton.icon(
                            onPressed: () {},
                            label: Text("Sign In Using GOOGLE"),
                            icon: Icon(Icons.alternate_email),
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
      ),
    );
  }
}
