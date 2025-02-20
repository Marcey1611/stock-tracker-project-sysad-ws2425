import 'package:flutter/foundation.dart';

class ApiConfig {
  static String getBaseUrl() {
    if (kIsWeb) {
      // for web
      return 'http://192.168.1.192:40105/api/update_app';
    } else {
      // for the Emulator
      return 'http://192.168.1.192:40105/api/update_app';
    }
  }
}
