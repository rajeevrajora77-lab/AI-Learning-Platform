import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'dart:convert';

class ApiProvider extends ChangeNotifier {
  final String backendUrl;
  late Dio _dio;
  bool isLoading = false;
  String? errorMessage;

  ApiProvider({required this.backendUrl}) {
    _dio = Dio(
      BaseOptions(
        baseUrl: backendUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {'Content-Type': 'application/json'},
      ),
    );
  }

  Future<Map<String, dynamic>?> generateContent(String topic, {String language = 'en', String depth = 'intermediate'}) async {
    try {
      isLoading = true;
      errorMessage = null;
      notifyListeners();

      final response = await _dio.post(
        '/api/generate-content',
        data: {
          'topic': topic,
          'language': language,
          'depth': depth,
        },
      );

      if (response.statusCode == 200) {
        isLoading = false;
        notifyListeners();
        return response.data as Map<String, dynamic>;
      }
    } on DioException catch (e) {
      errorMessage = e.message ?? 'Failed to generate content';
      isLoading = false;
      notifyListeners();
    }
    return null;
  }

  Future<Map<String, dynamic>?> generateVideo(String contentId, {String style = 'experimental'}) async {
    try {
      isLoading = true;
      errorMessage = null;
      notifyListeners();

      final response = await _dio.post(
        '/api/generate-video',
        data: {
          'content_id': contentId,
          'style': style,
        },
      );

      if (response.statusCode == 200) {
        isLoading = false;
        notifyListeners();
        return response.data as Map<String, dynamic>;
      }
    } on DioException catch (e) {
      errorMessage = e.message ?? 'Failed to generate video';
      isLoading = false;
      notifyListeners();
    }
    return null;
  }

  Future<Map<String, dynamic>?> getContent(String id) async {
    try {
      isLoading = true;
      errorMessage = null;
      notifyListeners();

      final response = await _dio.get('/api/content/$id');

      if (response.statusCode == 200) {
        isLoading = false;
        notifyListeners();
        return response.data as Map<String, dynamic>;
      }
    } on DioException catch (e) {
      errorMessage = e.message ?? 'Failed to fetch content';
      isLoading = false;
      notifyListeners();
    }
    return null;
  }

  Future<Map<String, dynamic>?> getVideo(String id) async {
    try {
      isLoading = true;
      errorMessage = null;
      notifyListeners();

      final response = await _dio.get('/api/video/$id');

      if (response.statusCode == 200) {
        isLoading = false;
        notifyListeners();
        return response.data as Map<String, dynamic>;
      }
    } on DioException catch (e) {
      errorMessage = e.message ?? 'Failed to fetch video';
      isLoading = false;
      notifyListeners();
    }
    return null;
  }
}
