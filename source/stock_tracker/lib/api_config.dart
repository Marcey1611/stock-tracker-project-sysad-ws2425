import 'package:flutter/foundation.dart';

class ApiConfig {
  static String getBaseUrl() {
    if (kIsWeb) {
      // Korrekte URL verwenden (z. B. über Nginx oder direkt)
      return 'http://localhost:8081/api/update_app';
    } else {
      // Für den Emulator: Zugriff auf den Host
      return 'http://10.0.2.2:8081/api/update_app';
    }
  }
}
