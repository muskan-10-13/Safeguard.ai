import 'dart:io';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:routebetweentwopoints/repository/repo.dart';
import 'google_map_screen.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> with WidgetsBindingObserver {
  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void initState() {
    WidgetsBinding.instance.addObserver(this);
    super.initState();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) async {
    super.didChangeAppLifecycleState(state);
    _onAppResumed(state);
  }

  void _onAppResumed(AppLifecycleState state) async {
    var locationPermission = await Geolocator.checkPermission();
    if (state == AppLifecycleState.resumed) {
      //**Refer to this link for permission handling: https://davidserrano.io/best-way-to-handle-permissions-in-your-flutter-app
      //** FOR IOS
      if (Platform.isIOS) {
        if (locationPermission == LocationPermission.always ||
            locationPermission == LocationPermission.whileInUse) {
        } else {
          await Geolocator.checkPermission();
        }
        //** FOR ANDROID
      } else if (Platform.isAndroid) {
        if (locationPermission == LocationPermission.always ||
            locationPermission == LocationPermission.whileInUse) {
        } else {}
      }
    }
  }

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
        providers: [
          ChangeNotifierProvider.value(
            value: DataProvider(),
          ),
        ],
        child: Consumer<DataProvider>(
            builder: (ctx, auth, _) => MaterialApp(
                  debugShowCheckedModeBanner: false,
                  title: 'MyShop',
                  theme: ThemeData(
                    primarySwatch: Colors.blue,
                    fontFamily: 'Poppins',
                  ),
                  home: const GoogleMapScreen(),
                )));
  }
}
