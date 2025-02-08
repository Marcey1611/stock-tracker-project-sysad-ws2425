import 'package:flutter/material.dart';
import 'package:stock_tracker/data_tables.dart'; 

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  HomePageState createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  final List<Widget> _pages = [
    const StockDataTableWidget(), // Tabelle mit den Stock-Daten
    const Center(child: Text('Historie (noch nicht implementiert)')), // Platzhalter für Historie
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Image.asset('assets/images/stocktrackerLogo.png', height: 40),
            const SizedBox(width: 10),
            const Text('Stock Tracker'),
          ],
        ),
      ),
      body: _pages[_selectedIndex], // Aktive Seite basierend auf _selectedIndex
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.trending_up),
            label: 'Aktuell',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.history),
            label: 'Historie',
          ),
        ],
      ),
    );
  }
}
