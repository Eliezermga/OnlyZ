class Message {
  final int id;
  final int senderId;
  final int receiverId;
  final String content;
  final bool isRead;
  final String createdAt;
  final String? senderUsername;

  Message({
    required this.id,
    required this.senderId,
    required this.receiverId,
    required this.content,
    required this.isRead,
    required this.createdAt,
    this.senderUsername,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      senderId: json['sender_id'],
      receiverId: json['receiver_id'],
      content: json['content'],
      isRead: json['is_read'] == 1 || json['is_read'] == true,
      createdAt: json['created_at'],
      senderUsername: json['sender_username'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'sender_id': senderId,
      'receiver_id': receiverId,
      'content': content,
      'is_read': isRead,
      'created_at': createdAt,
      'sender_username': senderUsername,
    };
  }
}

class Conversation {
  final int otherUserId;
  final String username;
  final String? profilePicture;
  final String? firstName;
  final String? lastName;
  final String? lastMessage;
  final String? lastMessageAt;
  final int unreadCount;

  Conversation({
    required this.otherUserId,
    required this.username,
    this.profilePicture,
    this.firstName,
    this.lastName,
    this.lastMessage,
    this.lastMessageAt,
    required this.unreadCount,
  });

  factory Conversation.fromJson(Map<String, dynamic> json) {
    return Conversation(
      otherUserId: json['other_user_id'],
      username: json['username'],
      profilePicture: json['profile_picture'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      lastMessage: json['last_message'],
      lastMessageAt: json['last_message_at'],
      unreadCount: json['unread_count'] ?? 0,
    );
  }

  String get displayName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    } else if (firstName != null) {
      return firstName!;
    }
    return username;
  }
}