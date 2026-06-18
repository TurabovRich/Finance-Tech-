import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppShell extends StatelessWidget {
  const AppShell({super.key, required this.child});

  final Widget child;

  static const _tabs = [
    ('/home', Icons.insights_outlined, 'Insights'),
    ('/transactions', Icons.receipt_long_outlined, 'Activity'),
    ('/cards', Icons.credit_card_outlined, 'Cards'),
    ('/categories', Icons.category_outlined, 'Categories'),
    ('/profile', Icons.person_outline, 'Profile'),
  ];

  int _indexForLocation(String location) {
    final index = _tabs.indexWhere((tab) => location.startsWith(tab.$1));
    return index == -1 ? 0 : index;
  }

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).uri.toString();
    final currentIndex = _indexForLocation(location);

    return Scaffold(
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: currentIndex,
        onDestinationSelected: (index) => context.go(_tabs[index].$1),
        destinations: [
          for (final tab in _tabs)
            NavigationDestination(icon: Icon(tab.$2), label: tab.$3),
        ],
      ),
    );
  }
}
