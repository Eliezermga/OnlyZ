import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';
import '../models/user.dart';
import 'auth_service.dart';

class MatchService {
  final AuthService _authService = AuthService();

  // Like a user
  Future<Map<String, dynamic>> likeUser(int userId) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.post(
        Uri.parse('${ApiConstants.likes}/$userId'),
        headers: headers,
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'isMatch': data['isMatch'] ?? false,
        };
      }
      return {'success': false, 'isMatch': false};
    } catch (e) {
      print('Error liking user: $e');
      return {'success': false, 'isMatch': false};
    }
  }

  // Unlike a user
  Future<bool> unlikeUser(int userId) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.delete(
        Uri.parse('${ApiConstants.likes}/$userId'),
        headers: headers,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error unliking user: $e');
      return false;
    }
  }

  // Get likes given
  Future<List<Profile>> getLikesGiven() async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse(ApiConstants.likesGiven),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Profile.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error getting likes given: $e');
      return [];
    }
  }

  // Get likes received
  Future<List<Profile>> getLikesReceived() async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse(ApiConstants.likesReceived),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Profile.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error getting likes received: $e');
      return [];
    }
  }

  // Get all matches
  Future<List<Profile>> getMatches() async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse(ApiConstants.matches),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Profile.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error getting matches: $e');
      return [];
    }
  }

  // Check if matched with specific user
  Future<bool> isMatched(int userId) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse('${ApiConstants.matches}/$userId'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['isMatch'] ?? false;
      }
      return false;
    } catch (e) {
      print('Error checking match: $e');
      return false;
    }
  }
}