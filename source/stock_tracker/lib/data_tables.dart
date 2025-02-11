import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'api_config.dart';
//für LifeCycle -> muss flutter pub add widgets_binding_observer im Terminal hinzugefügt werden, bzw dann
//auch in der compose.yml datei

class StockDataTableWidget extends StatefulWidget {
  const StockDataTableWidget({super.key});

  @override
  StockDataTableWidgetState createState() => StockDataTableWidgetState();
}

class StockDataTableWidgetState extends State<StockDataTableWidget> {
  List<dynamic> stockData = [];
  bool isLoading = true;
  String? overallPicture;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _fetchStockData();
    _startTimerNew();
  }

  void _startTimerNew() {
    _timer = Timer.periodic(const Duration(seconds: 30), (timer) {
      print("Daten werden alle 30sec aktualisiert");
      _fetchStockData();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
//sollte das mit dem Timer nicht funktionieren dann diesen LifeCycle versuchen, sodass IOS auch keine probleme hat
  /*@override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused) {
      // App wird in den Hintergrund verschoben -> Timer stoppen
      print("App pausiert, Timer gestoppt.");
      _timer?.cancel();
    } else if (state == AppLifecycleState.resumed) {
      // App kehrt zurück -> Timer neu starten
      print("App wieder im Vordergrund, Timer neu gestartet.");
      _startTimer();
    }
  }*/

  Future<void> _fetchStockData() async {
    try {
      final apiUrl = ApiConfig.getBaseUrl();
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        final fetchedData = jsonDecode(response.body);
        print('Geladene Daten: $fetchedData');
        print('Erhaltene Daten: ${response.body}'); // Debug-Ausgabe
        // Konvertiere die Schlüssel-Wert-Paare in eine Liste
        setState(() {
          overallPicture = fetchedData['overall_picture']; // Bild-URL auslesen
          stockData = (fetchedData['products'] as Map).values.map((product) {
          return {
            //"id": int.tryParse(product["id"].toString().trim()) ?? 0,
            "name": product["name"] ?? "Unknown",
            "amount": int.tryParse(product["amount"].toString().trim()) ?? 0,
            "picture": product["picture"]
          };
           }).toList(); // JSON korrekt als Liste verarbeiten
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load data');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      print('Error fetching stock data: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (stockData.isEmpty) {
      return const Center(child: Text('Keine Daten verfügbar.'));
    }

    return Column(
      children: [
        if (overallPicture != null)
          (overallPicture!.startsWith('http') ||
                  overallPicture!.startsWith('data:image'))
              ? (overallPicture!.startsWith('http')
                  ? Image.network(
                      overallPicture!,
                      height: 200,
                      fit: BoxFit.contain,
                    )
                  : Image.memory(
                      base64Decode(overallPicture!
                          .replaceAll('data:image/png;base64,', '')),
                      height: 200,
                      fit: BoxFit.contain,
                    ))
              : Column(
                children: [
                  Text(
                      overallPicture!,
                      style: const TextStyle(
                          fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10,),
                    Image.asset('assets/images/regal.png',
                    height: 150,
                    fit: BoxFit.contain,
                    ),
                ],
              ),
        Expanded(
          child: Scrollbar(
            thumbVisibility: true,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Scrollbar(
                thumbVisibility: true,
                thickness: 5,
                child: SingleChildScrollView(
                  scrollDirection: Axis.vertical,
                  child: DataTable(
                    columns: const [
                      //DataColumn(label: Text('ID')),
                      DataColumn(label: Text('Name')),
                      DataColumn(label: Text('Amount')),
                      DataColumn(label: Text('Product Picture')),
                    ],
                    rows: stockData.map((product) {
                      print('Produktdaten: $product');
                      return DataRow(cells: [
                        //DataCell(Text(product['id'].toString())),
                        DataCell(Text(product['name'] ?? 'Unknown')),
                        DataCell(Text(product['amount'].toString())),
                        DataCell(product['picture'] != null
                            ? Image.network(
                                product['picture'],
                                height: 50,
                                width: 50,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) {
                                  return const Icon(Icons.broken_image);
                                },
                              )
                            : const Text('No Picture')),
                      ]);
                    }).toList(),
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
