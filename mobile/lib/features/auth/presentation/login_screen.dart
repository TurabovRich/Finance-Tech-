import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              Text('Clarity', style: Theme.of(context).textTheme.headlineLarge),
              const SizedBox(height: 8),
              Text(
                'Educational fintech simulation — no real payments.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 32),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Phone number',
                  hintText: '+998901234567',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.phone,
              ),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: () => context.go('/home'),
                child: const Text('Continue (simulated)'),
              ),
              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }
}
