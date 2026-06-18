import 'package:flutter/material.dart';

class AppTheme {
  static const _primary = Color(0xFF0D6E6E);

  static ThemeData get light => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: _primary, brightness: Brightness.light),
        appBarTheme: const AppBarTheme(centerTitle: true, elevation: 0),
      );

  static ThemeData get dark => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: _primary, brightness: Brightness.dark),
        appBarTheme: const AppBarTheme(centerTitle: true, elevation: 0),
      );
}
