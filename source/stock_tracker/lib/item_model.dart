class Item {
  final int productId; //produktID
  final String productName; //produktName
  final String systemIN;

  Item({
    required this.productId,
    required this.productName,
    required this.systemIN,
  });

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      productId: json['productId'],
      productName: json['productName'],
      systemIN: json['SystemIN'],
    );
  }
}
