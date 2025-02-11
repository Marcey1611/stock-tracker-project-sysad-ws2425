import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'api_config.dart';

class StockDataTableWidget extends StatefulWidget {
  const StockDataTableWidget({super.key});

  @override
  StockDataTableWidgetState createState() => StockDataTableWidgetState();
}

class StockDataTableWidgetState extends State<StockDataTableWidget> {
  List<dynamic> stockData = [];
  bool isLoading = true;
  dynamic overallPicture;
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

  Future<void> _fetchStockData() async {
    try {
      final apiUrl = ApiConfig.getBaseUrl();
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        String responseBody = utf8.decode(response.bodyBytes);
        final fetchedData = jsonDecode(responseBody);
        print('Geladene Daten: $fetchedData\n');

        setState(() {
          overallPicture = fetchedData['overall_picture'];

          if (overallPicture != null && overallPicture!.contains('base64')) {
            overallPicture = base64Decode(
              overallPicture!.replaceAll('data:image/png;base64,', ''),
            );
          }
          stockData = (fetchedData['products'] as Map).values.map((product) {
            return {
              "name": product["name"] ?? "Unknown",
              "amount": int.tryParse(product["amount"].toString().trim()) ?? 0,
              "picture": product["picture"]
            };
          }).toList();
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
    return Scaffold(
      body: Container(
        width: double.infinity, // Volle Breite des Bildschirms nutzen
        height: MediaQuery.of(context)
            .size
            .height, // Dynamische Höhe basierend auf Bildschirmgröße
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            if (overallPicture != null)
              overallPicture is Uint8List
                  ? Image.memory(
                      overallPicture!,
                      
                      height: 200,
                      fit: BoxFit.contain,
                    )
                  : Column(
                      children: [
                        Text(
                          overallPicture!,
                          style: const TextStyle(
                              fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 10),
                        Image.asset(
                          'assets/images/regal.png',
                          height: 150,
                          fit: BoxFit.contain,
                        ),
                      ],
                    ),
            const SizedBox(height: 16),
            Expanded(
              child: Scrollbar(
                thumbVisibility: true,
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: ConstrainedBox(
                    constraints: BoxConstraints(
                      minWidth: MediaQuery.of(context)
                          .size
                          .width, // Dynamische Breite basierend auf dem Bildschirm
                    ),
                    child: SingleChildScrollView(
                      scrollDirection: Axis.vertical,
                      child: DataTable(
                        columns: const [
                          DataColumn(label: Text('Name')),
                          DataColumn(label: Text('Amount')),
                          DataColumn(label: Text('Product Picture')),
                        ],
                        rows: stockData.map((product) {
                          return DataRow(cells: [
                            DataCell(Text(product['name'] ?? 'Unknown')),
                            DataCell(Text(product['amount'].toString())),
                            DataCell(product['picture'] != null
                                ? Image.network(
                                    product['picture'],
                                    height: 50,
                                    width: 50,
                                    fit: BoxFit.cover,
                                    errorBuilder: (context, error, stackTrace) {
                                      return Row(
                                        children: [
                                          const Icon(Icons.no_photography,
                                              size: 24),
                                          const SizedBox(width: 10),
                                          Text(
                                            product['picture'] ?? 'No Picture',
                                            style: const TextStyle(
                                                fontSize: 12,
                                                color: Color.fromARGB(
                                                    255, 77, 69, 69)),
                                          ),
                                        ],
                                      );
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
        ),
      ),
    );
  }
}
