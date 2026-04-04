import 'package:flutter/material.dart';
import '../services/api_service.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({Key? key}) : super(key: key);

  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _fullNameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _farmNameController = TextEditingController();
  final _locationController = TextEditingController();
  String _farmType = 'Dairy';

  bool _isLoading = false;

  Future<void> _submitForm() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);

      final data = {
        'username': _usernameController.text,
        'password': _passwordController.text,
        'full_name': _fullNameController.text,
        'phone_number': _phoneController.text,
        'farm_name': _farmNameController.text,
        'location': _locationController.text,
        'farm_type': _farmType,
      };

      try {
        await ApiService.createFarmer(data);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Registration successful! Please login.')),
        );
        Navigator.pop(context); // Go back to login
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Registration failed: $e')),
        );
      } finally {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Join Smart Ranch'),
        backgroundColor: Colors.green.shade700,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Create Your Account',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.green),
              ),
              const SizedBox(height: 8),
              const Text('Secure your farm records today.', style: TextStyle(color: Colors.grey)),
              const SizedBox(height: 24),
              _buildTextField(_usernameController, 'Username', Icons.person),
              const SizedBox(height: 16),
              _buildTextField(_passwordController, 'Password', Icons.lock, obscureText: true),
              const SizedBox(height: 16),
              _buildTextField(_fullNameController, 'Full Name', Icons.badge),
              const SizedBox(height: 16),
              _buildTextField(_phoneController, 'Phone Number', Icons.phone),
              const SizedBox(height: 16),
              _buildTextField(_farmNameController, 'Farm Name', Icons.agriculture),
              const SizedBox(height: 16),
              _buildTextField(_locationController, 'Location', Icons.location_on),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: _farmType,
                decoration: InputDecoration(
                  labelText: 'Farm Type',
                  prefixIcon: const Icon(Icons.category),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                items: ['Dairy', 'Beef', 'Mixed']
                    .map((type) => DropdownMenuItem(value: type, child: Text(type)))
                    .toList(),
                onChanged: (value) => setState(() => _farmType = value!),
              ),
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: _isLoading ? null : _submitForm,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green.shade700,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: _isLoading 
                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                    : const Text('REGISTER NOW', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, IconData icon, {bool obscureText = false}) {
    return TextFormField(
      controller: controller,
      obscureText: obscureText,
      decoration: InputDecoration(
        labelText: label,
        prefixIcon: Icon(icon),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
      validator: (value) => value!.isEmpty ? '$label is required' : null,
    );
  }
}
