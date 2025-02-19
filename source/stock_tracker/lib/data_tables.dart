import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'api_config.dart';
import 'package:logger/logger.dart';

final Logger logger = Logger();

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

  final ScrollController _verticalScrollController = ScrollController();
  final ScrollController _horizontalScrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _fetchStockData();
    _startTimerNew();
  }

  void _startTimerNew() {
    _timer = Timer.periodic(const Duration(seconds: 30), (timer) {
      _fetchStockData();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _verticalScrollController.dispose();
    _horizontalScrollController.dispose();
    super.dispose();
  }

  Future<void> _fetchStockData() async {
    try {
      final apiUrl = ApiConfig.getBaseUrl();
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        String responseBody = utf8.decode(response.bodyBytes);
        final fetchedData = jsonDecode(responseBody);

        setState(() {
          overallPicture = fetchedData['overall_picture'];

          try {
            Uint8List decodedImage = base64Decode(overallPicture!);
            overallPicture = decodedImage;
          } catch (e) {
            overallPicture = null;
          }
          stockData = (fetchedData['products'] as Map).values.map((product) {
            dynamic picture = product["picture"];

            if (picture != null) {
              try {
                Uint8List decodedImage = base64Decode(picture);
                picture = decodedImage;
              } catch (e) {
                picture = null;
              }
            }
            return {
              "name": product["name"] ?? "Unknown",
              "amount": int.tryParse(product["amount"].toString().trim()) ?? 0,
              "picture": picture
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
      logger.e('Error fetching stock data: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    double fontSize = screenWidth * 0.02;

    return Scaffold(
      body: Container(
        width: screenWidth,
        height: screenHeight,
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            if (overallPicture != null)
              overallPicture is Uint8List
                  ? Image.memory(
                      overallPicture!,
                      height: screenHeight * 0.3,
                      fit: BoxFit.contain,
                    )
                  : Column(
                      children: [
                        Text(
                          overallPicture!,
                          style: TextStyle(
                              fontSize: fontSize, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 10),
                        Image.asset(
                          'assets/images/regal.png',
                          height: screenHeight * 0.15,
                          fit: BoxFit.contain,
                        ),
                      ],
                    ),
            const SizedBox(height: 25),
            Expanded(
              child: Scrollbar(
                thumbVisibility: true,
                controller: _verticalScrollController,
                child: SingleChildScrollView(
                  controller: _verticalScrollController,
                  scrollDirection: Axis.vertical,
                  child: SingleChildScrollView(
                    controller: _horizontalScrollController,
                    scrollDirection: Axis.horizontal,
                    child: ConstrainedBox(
                      constraints: BoxConstraints(
                        minWidth: screenWidth * 0.95,
                      ),
                      child: Table(
                        columnWidths: {
                          0: const FlexColumnWidth(),
                          1: FixedColumnWidth(screenWidth * 0.2),
                          2: FixedColumnWidth(screenWidth * 0.3),
                        },
                        children: [
                          TableRow(
                            children: [
                              Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Text(
                                  'Name',
                                  style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: (fontSize * 0.8)),
                                ),
                              ),
                              Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Text(
                                  'Amount',
                                  style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: (fontSize * 0.8)),
                                ),
                              ),
                              Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Center(
                                  child: Text(
                                    'Product Picture',
                                    style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: (fontSize * 0.8)),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          TableRow(
                            children: [
                              Container(height: 3, color: Colors.black),
                              Container(height: 3, color: Colors.black),
                              Container(height: 3, color: Colors.black),
                            ],
                          ),
                          ...stockData.map(
                            (product) {
                              return TableRow(
                                decoration: const BoxDecoration(
                                  border: Border(
                                    bottom: BorderSide(
                                        color: Colors.black26, width: 2),
                                  ),
                                ),
                                children: [
                                  Padding(
                                    padding: const EdgeInsets.all(8.0),
                                    child: Text(
                                      product['name'] ?? 'Unknown',
                                      style:
                                          TextStyle(fontSize: fontSize * 0.7),
                                    ),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(8.0),
                                    child: Text(
                                      product['amount'].toString(),
                                      style:
                                          TextStyle(fontSize: fontSize * 0.7),
                                    ),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(8.0),
                                    child: Align(
                                      alignment: Alignment.center,
                                      child: product['picture'] != null
                                          ? Image.memory(
                                              product['picture'],
                                              height: screenHeight * 0.1,
                                              width: screenWidth * 0.15,
                                              fit: BoxFit.contain,
                                            )
                                          : Row(
                                              mainAxisSize: MainAxisSize.min,
                                              children: [
                                                Icon(Icons.no_photography,
                                                    size: (fontSize * 0.7),
                                                    color: Colors.red),
                                                const SizedBox(width: 5),
                                                Text(
                                                  'No Picture',
                                                  style: TextStyle(
                                                      fontSize:
                                                          (fontSize * 0.7),
                                                      fontWeight:
                                                          FontWeight.bold),
                                                ),
                                              ],
                                            ),
                                    ),
                                  ),
                                ],
                              );
                            },
                          ),
                        ],
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
