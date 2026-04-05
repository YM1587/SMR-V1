import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ReportsScreen extends StatefulWidget {
  final int farmerId;
  const ReportsScreen({super.key, required this.farmerId});

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  Map<String, dynamic>? _financialSummary;
  Map<String, dynamic>? _mortalityRate;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final finance = await ApiService.getFinancialSummary(widget.farmerId);
      final mortality = await ApiService.getMortalityRate(widget.farmerId);
      setState(() {
        _financialSummary = finance;
        _mortalityRate = mortality;
        _isLoading = false;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading reports: $e')),
      );
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Farm Analytics & Reports'),
        elevation: 0,
        backgroundColor: Colors.green.shade700,
        foregroundColor: Colors.white,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildSectionTitle('Herd Performance'),
                  _buildMortalityCard(),
                  const SizedBox(height: 24),
                  _buildSectionTitle('Financial Performance'),
                  _buildFinancialSummaryCard(),
                  const SizedBox(height: 24),
                  _buildSectionTitle('Batch Efficiency (FCR)'),
                  const Text(
                    'Select a pen to view the Feed Conversion Ratio (FCR).',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 8),
                  _buildFCRSelector(),
                ],
              ),
            ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Text(
        title,
        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.green),
      ),
    );
  }

  Widget _buildMortalityCard() {
    final rate = _mortalityRate?['mortality_rate'] ?? 0.0;
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.red.shade50,
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.trending_down, color: Colors.red.shade700, size: 40),
            ),
            const SizedBox(width: 20),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Overall Mortality Rate', style: TextStyle(fontSize: 16, color: Colors.grey)),
                Text(
                  '$rate%',
                  style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFinancialSummaryCard() {
    final total = _financialSummary?['total_expenses'] ?? 0.0;
    final categories = _financialSummary?['categories'] as Map<String, dynamic>? ?? {};

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Total Net Expenses', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                Text(
                  'Ksh ${total.toStringAsFixed(2)}',
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.red),
                ),
              ],
            ),
            const Divider(height: 32),
            ...categories.entries.map((e) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(e.key),
                      Text('Ksh ${e.value.toStringAsFixed(2)}', style: const TextStyle(fontWeight: FontWeight.w600)),
                    ],
                  ),
                )),
          ],
        ),
      ),
    );
  }

  Widget _buildFCRSelector() {
    // This would typically involve a dropdown of Pens. For now, a simple placeholder.
    return InkWell(
      onTap: () {
        // Navigate to a sub-screen or show a dialog to pick a pen
      },
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          border: Border.all(color: Colors.green.shade200),
          borderRadius: BorderRadius.circular(12),
          color: Colors.green.shade50,
        ),
        child: const Row(
          children: [
            Icon(Icons.scale, color: Colors.green),
            SizedBox(width: 12),
            Text('View Pen-wise Feed Conversion Ratio', style: TextStyle(fontWeight: FontWeight.bold)),
            Spacer(),
            Icon(Icons.chevron_right),
          ],
        ),
      ),
    );
  }
}
