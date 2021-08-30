class DataShareService {
  static bool loginState = false;
  Map<String, String> user = {"userId": "", "role": ""};
  static final DataShareService _instance = DataShareService._internal();

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

  bool loginStudent(userName, password) {
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

  signUpStudent(userName, password) {
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
}
