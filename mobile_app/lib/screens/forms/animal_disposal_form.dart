import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../services/api_service.dart';
import '../../models/models.dart';

class AnimalDisposalForm extends StatefulWidget {
  final Animal animal;
  final int farmerId;

  const AnimalDisposalForm({super.key, required this.animal, required this.farmerId});

  @override
  _AnimalDisposalFormState createState() => _AnimalDisposalFormState();
}

class _AnimalDisposalFormState extends State<AnimalDisposalForm> {
  final _formKey = GlobalKey<FormState>();
  String _reason = 'Sold';
  final TextEditingController _dateController = TextEditingController(text: DateFormat('yyyy-MM-dd').format(DateTime.now()));
  final TextEditingController _valueController = TextEditingController();
  final TextEditingController _notesController = TextEditingController();
  bool _isSubmitting = false;

  final List<String> _reasons = ['Sold', 'Died', 'Culled', 'Donated', 'Other'];

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() => _isSubmitting = true);
    try {
      final data = {
        'disposal_reason': _reason,
        'disposal_date': _dateController.text,
        'disposal_value': _valueController.text.isNotEmpty ? double.parse(_valueController.text) : null,
        'notes': _notesController.text,
      };
      
      await ApiService.disposeAnimal(widget.animal.id, data);
      
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Animal disposed successfully')));
      Navigator.pop(context, true);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dispose Animal: ${widget.animal.tagNumber}')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              DropdownButtonFormField<String>(
                initialValue: _reason,
                decoration: const InputDecoration(labelText: 'Reason'),
                items: _reasons.map((r) => DropdownMenuItem(value: r, child: Text(r))).toList(),
                onChanged: (val) => setState(() => _reason = val!),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _dateController,
                decoration: const InputDecoration(labelText: 'Date (YYYY-MM-DD)', prefixIcon: Icon(Icons.calendar_today)),
                readOnly: true,
                onTap: () async {
                  final picked = await showDatePicker(
                    context: context,
                    initialDate: DateTime.now(),
                    firstDate: DateTime(2000),
                    lastDate: DateTime.now(),
                  );
                  if (picked != null) {
                    _dateController.text = DateFormat('yyyy-MM-dd').format(picked);
                  }
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _valueController,
                decoration: const InputDecoration(labelText: 'Value / Sale Price (Ksh, Optional)', prefixIcon: Icon(Icons.payments)),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _notesController,
                decoration: const InputDecoration(labelText: 'Notes'),
                maxLines: 3,
              ),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _isSubmitting ? null : _submit,
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
                  child: _isSubmitting ? const CircularProgressIndicator(color: Colors.white) : const Text('Confirm Disposal'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
