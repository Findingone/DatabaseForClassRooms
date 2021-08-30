import 'package:http/http.dart' as http;

class DataShareService {
  String url = "http://127.0.0.1:5000/";
  static bool loginState = false;
  Map<String, String> user = {"userId": "", "role": ""};
  static final DataShareService _instance = DataShareService._internal();
  Map<String, String> schedule = {};

  DataShareService._internal() {
    loginState = false;
  }
  factory DataShareService() {
    return _instance;
  }
  bool getLoginStatus() {
    return loginState;
  }

  logout() {
    loginState = false;
  }

  Future<bool> loginStudent(userName, password) async {
    final response = await http.post(Uri.parse(url + "/"));
    user["userId"] = userName;
    user["role"] = "student";
    loginState = true;
    return loginState;
  }

  bool loginTeacher(userName, password) {
    user["userId"] = userName;
    user["role"] = "teacher";
    loginState = true;
    return loginState;
  }

  signUpStudent(userName, password) async {
    String localUrl =
        url + "createNewStudent?studentName=Keshav&studentEmail=kesha";
    print(localUrl);
    final response = await http.get(Uri.parse(localUrl));
    print(response);
    user["userId"] = userName;
    user["role"] = "student";
    loginState = true;
    return loginState;
  }

  signUpTeacher(userName, password) {
    user["userId"] = userName;
    user["role"] = "teacher";
    loginState = true;
    return loginState;
  }

  scheduleClass(time, link) {
    this.schedule[time] = link;
  }

  getScheduleClassesTeacher() {
    return this.schedule;
  }

  getUserDetail() {
    return user["role"];
  }
}
