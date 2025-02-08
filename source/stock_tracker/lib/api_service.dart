

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_config.dart';

Future<List<dynamic>> getDataFromApi() async {
  final url = ApiConfig.getBaseUrl();
  try {
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['products'] ?? []; // Anpassung je nach API-Struktur
    } else {
      throw Exception('Fehler beim Laden der Daten: ${response.statusCode}');
    }
  } catch (e) {
    throw Exception('API-Aufruf fehlgeschlagen: $e');
  }
}
