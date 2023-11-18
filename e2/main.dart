import 'package:flutter/material.dart';
import 'auth.dart';
import 'sleep_data_screen.dart';
import 'step_data_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Google Fit Data',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Google Fit Data')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              child: Text("Fetch and Show Sleep Data"),
              onPressed: () async {
                List<dynamic>? fetchedSessions = await authenticateAndFetchData("sleep");
                if (fetchedSessions != null) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => SleepDataScreen(sleepSessions: fetchedSessions)),
                  );
                }
              },
            ),
            SizedBox(height: 20),
            ElevatedButton(
              child: Text("Fetch and Show Step Data"),
              onPressed: () async {
                Map<String, int>? fetchedStepData = await authenticateAndFetchData("step");
                if (fetchedStepData != null) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => StepDataScreen(stepData: fetchedStepData)),
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}

