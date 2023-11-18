import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class SleepDataScreen extends StatelessWidget {
  final List<dynamic> sleepSessions;

  SleepDataScreen({required this.sleepSessions});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sleep Data'),
      ),
      body: ListView.builder(
        itemCount: sleepSessions.length,
        itemBuilder: (context, index) {
          var session = sleepSessions[index];
          final startDate = DateTime.fromMillisecondsSinceEpoch(int.parse(session.startTimeMillis!));
          final endDate = DateTime.fromMillisecondsSinceEpoch(int.parse(session.endTimeMillis!));
          final formattedStartDate = DateFormat('yyyy-MM-dd HH:mm:ss').format(startDate);
          final formattedEndDate = DateFormat('yyyy-MM-dd HH:mm:ss').format(endDate);

          return ListTile(
            title: Text("Sleep Session $index"),
            subtitle: Text("Sleep Time: $formattedStartDate\nWake-up Time: $formattedEndDate"),
          );
        },
      ),
    );
  }
}

