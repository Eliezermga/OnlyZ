import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';
import '../models/message.dart';
import 'auth_service.dart';

class MessageService {
  final AuthService _authService = AuthService();

  // Get conversations list
  Future<List<Conversation>> getConversations() async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.get(
        Uri.parse(ApiConstants.conversations),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Conversation.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error getting conversations: $e');
      return [];
    }
  }

  // Get messages with specific user
  Future<List<Message>> getMessages(int userId, {int limit = 50, int offset = 0}) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final uri = Uri.parse('${ApiConstants.messages}/$userId').replace(
        queryParameters: {
          'limit': limit.toString(),
          'offset': offset.toString(),
        },
      );

      final response = await http.get(uri, headers: headers);

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Message.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print('Error getting messages: $e');
      return [];
    }
  }

  // Send message
  Future<Message?> sendMessage(int userId, String content) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.post(
        Uri.parse('${ApiConstants.messages}/$userId'),
        headers: headers,
        body: jsonEncode({'content': content}),
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        return Message.fromJson(data);
      }
      return null;
    } catch (e) {
      print('Error sending message: $e');
      return null;
    }
  }

  // Mark messages as read
  Future<bool> markAsRead(int userId) async {
    try {
      final headers = await _authService.getAuthHeaders();
      final response = await http.put(
        Uri.parse('${ApiConstants.messages}/$userId/read'),
        headers: headers,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error marking messages as read: $e');
      return false;
    }
  }
}