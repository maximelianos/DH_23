import 'package:flutter/material.dart';

class StepDataScreen extends StatelessWidget {
  final Map<String, int> stepData;

  StepDataScreen({required this.stepData});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Step Data'),
      ),
      body: ListView.builder(
        itemCount: stepData.keys.length,
        itemBuilder: (context, index) {
          String date = stepData.keys.elementAt(index);
          int steps = stepData[date]!;
          return ListTile(
            title: Text("Date: $date"),
            subtitle: Text("Steps: $steps"),
          );
        },
      ),
    );
  }
}
