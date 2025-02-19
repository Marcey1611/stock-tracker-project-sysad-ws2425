import 'package:flutter/foundation.dart';

class ApiConfig {
  static String getBaseUrl() {
    if (kIsWeb) {
      // for web
      return 'http://localhost:8081/api/update_app';
    } else {
      // for the Emulator
      return 'http://10.0.2.2:8081/api/update_app';
    }
  }
}
