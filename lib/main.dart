import 'package:firebase_core/firebase_core.dart';
import 'package:fliprapp/dashboard.dart';
import 'package:fliprapp/dataService.dart';
import 'package:fliprapp/homepage.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  DataShareService dataService = DataShareService();
  checkLoginState() {
    if (dataService.getLoginStatus()) {
      return Dashboard();
    }
    return Homepage();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: checkLoginState(),
    );
  }
}
