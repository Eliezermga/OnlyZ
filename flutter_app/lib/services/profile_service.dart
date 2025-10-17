import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';
import '../models/user.dart';
import 'auth_service.dart';

class ProfileService {
  final AuthService _authService = AuthService();

  // Get my profile
  Future<Profile?> getMyProfile() async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse(ApiConstants.myProfile),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Profile.fromJson(data);
      }
      return null;
    } catch (e) {
      print('Error getting profile: $e');
      return null;
    }
  }

  // Get profile by user ID
  Future<Profile?> getProfile(int userId) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse('${ApiConstants.profiles}/$userId'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Profile.fromJson(data);
      }
      return null;
    } catch (e) {
      print('Error getting profile: $e');
      return null;
    }
  }

  // Create or update profile
  Future<bool> updateProfile(Profile profile) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.post(
        Uri.parse(ApiConstants.myProfile),
        headers: headers,
        body: jsonEncode(profile.toJson()),
      );

      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('Error updating profile: $e');
      return false;
    }
  }

  // Upload profile picture
  Future<String?> uploadProfilePicture(File imageFile) async {
    try {
      final token = await _authService.getToken();
      final request = http.MultipartRequest(
        'POST',
        Uri.parse(ApiConstants.uploadPicture),
      );

      request.headers['Authorization'] = 'Bearer $token';
      request.files.add(
        await http.MultipartFile.fromPath('picture', imageFile.path),
      );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['filename'];
      }
      return null;
    } catch (e) {
      print('Error uploading picture: $e');
      return null;
    }
  }

  // Browse profiles with filters
  Future<List<Profile>> browseProfiles({
    String? gender,
    int? minAge,
    int? maxAge,
    String? city,
    int limit = 20,
    int offset = 0,
  }) async {
    try {
      final headers = await _authService.getAuthHeaders();
      
      // Build query parameters
      final queryParams = <String, String>{
        'limit': limit.toString(),
        'offset': offset.toString(),
      };
      
      if (gender != null) queryParams['gender'] = gender;
      if (minAge != null) queryParams['min_age'] = minAge.toString();
      if (maxAge != null) queryParams['max_age'] = maxAge.toString();
      if (city != null) queryParams['city'] = city;

      final uri = Uri.parse(ApiConstants.profiles).replace(
        queryParameters: queryParams,
      );

      final response = await http.get(uri, headers: headers);

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Profile.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error browsing profiles: $e');
      return [];
    }
  }
}