import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'providers/api_provider.dart';
import 'screens/home_screen.dart';
import 'screens/content_screen.dart';
import 'screens/video_screen.dart';
import 'screens/library_screen.dart';

future main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: '.env');
  runApp(const AILearningApp());
}

class AILearningApp extends StatelessWidget {
  const AILearningApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => ApiProvider(
            backendUrl: dotenv.env['BACKEND_URL'] ?? 'http://localhost:5000',
          ),
        ),
      ],
      child: MaterialApp(
        title: 'AI Learning Platform',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primaryColor: Colors.blue.shade600,
          useMaterial3: true,
          appBarTheme: AppBarTheme(
            backgroundColor: Colors.blue.shade600,
            centerTitle: true,
            elevation: 0,
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue.shade600,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
        ),
        home: const MainScreen(),
        routes: {
          '/home': (context) => const HomeScreen(),
          '/content': (context) => const ContentScreen(),
          '/video': (context) => const VideoScreen(),
          '/library': (context) => const LibraryScreen(),
        },
      ),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({Key? key}) : super(key: key);

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeScreen(),
    ContentScreen(),
    VideoScreen(),
    LibraryScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.description),
            label: 'Content',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.videocam),
            label: 'Videos',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.library_books),
            label: 'Library',
          ),
        ],
      ),
    );
  }
}
