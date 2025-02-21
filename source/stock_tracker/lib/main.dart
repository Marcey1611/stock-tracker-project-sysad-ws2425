import 'package:flutter/material.dart';
import 'package:stock_tracker/home_page.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    const ProviderScope(
      child: StockTrackerApp(),
    ),
  );
}

class StockTrackerApp extends StatelessWidget {
  const StockTrackerApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stock Tracker',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomePage(),
    );
  }
}
