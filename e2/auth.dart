import 'package:google_sign_in/google_sign_in.dart';
import 'package:googleapis/fitness/v1.dart' as fitness;
import 'package:googleapis_auth/auth.dart';
import 'package:googleapis_auth/auth_io.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';


final _scopes = [
  'https://www.googleapis.com/auth/fitness.activity.read',
  'https://www.googleapis.com/auth/fitness.sleep.read'
];

Future<dynamic> authenticateAndFetchData(String dataType) async {
  final GoogleSignIn _googleSignIn = GoogleSignIn(scopes: _scopes);

  try {
    GoogleSignInAccount? account = await _googleSignIn.signIn();
    if (account != null) {
      GoogleSignInAuthentication auth = await account.authentication;

      final expiryDate = DateTime.now().add(
        Duration(seconds: 3600),  // Assuming a default of 1 hour
      ).toUtc();

      final credentials = AccessCredentials(
        AccessToken(
          'Bearer',  // Hard-coded token type
          auth.accessToken!,
          expiryDate,
        ),
        null,
        _scopes,
      );

      final client = authenticatedClient(http.Client(), credentials);
      switch (dataType) {
        case 'sleep':
          return fetchSleepData(client);
        case 'step':
          // fetch data from apple health that was loaded into Google Fit
          return fetchStepData(client, "derived:com.google.step_count.delta:com.google.ios.fit:appleinc.:iphone:2df7ed48:top_level");
        default:
          return null;
      }
    }
  } catch (error) {
    print(error);
  }
  return null;
}


Future<List<fitness.Session>> fetchSleepData(http.Client client) async {
  var data = await fitness.FitnessApi(client).users.sessions.list(
    'me',
    activityType: [72], // 72 corresponds to sleep in Google Fit
  );
  return data.session ?? [];
}

// find data source id
Future<void> listDataSources(http.Client client) async {
  try {
    var response = await fitness.FitnessApi(client).users.dataSources.list('me');
    for (var dataSource in response.dataSource!) {
      print('Data Source:');
      print('Data Stream ID: ${dataSource.dataStreamId}');
      print('Type: ${dataSource.type}');
      print('Name: ${dataSource.name}');
      print('Application: ${dataSource.application?.name}');
      print('---');
    }
  } catch (error) {
    print("Error listing data sources: $error");
  }
}

// fetch step data from specific data source
Future<Map<String, int>> fetchStepData(http.Client client, String dataSourceId) async {
  try {
    DateTime now = DateTime.now();
    DateTime startDate = DateTime(now.year, now.month, now.day).subtract(Duration(days: 7));
    DateTime endDate = DateTime(now.year, now.month, now.day).add(Duration(days: 1));

    String dataSetId = "${startDate.millisecondsSinceEpoch * 1000000}-${endDate.millisecondsSinceEpoch * 1000000}";

    var response = await fitness.FitnessApi(client).users.dataSources.datasets.get('me', dataSourceId, dataSetId);

    Map<String, int> stepData = {};
    if (response.point != null) {
      for (var point in response.point!) {
        if (point.startTimeNanos != null && point.endTimeNanos != null) {
          int startTimeNanos = int.tryParse(point.startTimeNanos!) ?? 0;
          DateTime startTime = DateTime.fromMillisecondsSinceEpoch(startTimeNanos ~/ 1000000);
          String date = DateFormat('yyyy-MM-dd').format(startTime);
          int steps = point.value![0].intVal ?? 0;
          stepData.update(date, (existing) => existing + steps, ifAbsent: () => steps);
        }
      }
    }
    return stepData;
  } catch (error) {
    print("Error fetching step data: $error");
    return {};
  }
}

