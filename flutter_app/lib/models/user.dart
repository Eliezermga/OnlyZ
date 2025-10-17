class User {
  final int id;
  final String username;
  final String email;

  User({
    required this.id,
    required this.username,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      email: json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
    };
  }
}

class Profile {
  final int? id;
  final int userId;
  final String? firstName;
  final String? lastName;
  final String dateOfBirth;
  final String gender;
  final String lookingFor;
  final String? bio;
  final String? profilePicture;
  final String? city;
  final String? country;
  final double? latitude;
  final double? longitude;
  final int? age;
  final String? username;

  Profile({
    this.id,
    required this.userId,
    this.firstName,
    this.lastName,
    required this.dateOfBirth,
    required this.gender,
    required this.lookingFor,
    this.bio,
    this.profilePicture,
    this.city,
    this.country,
    this.latitude,
    this.longitude,
    this.age,
    this.username,
  });

  factory Profile.fromJson(Map<String, dynamic> json) {
    return Profile(
      id: json['id'],
      userId: json['user_id'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      dateOfBirth: json['date_of_birth'],
      gender: json['gender'],
      lookingFor: json['looking_for'],
      bio: json['bio'],
      profilePicture: json['profile_picture'],
      city: json['city'],
      country: json['country'],
      latitude: json['latitude']?.toDouble(),
      longitude: json['longitude']?.toDouble(),
      age: json['age'],
      username: json['username'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'first_name': firstName,
      'last_name': lastName,
      'date_of_birth': dateOfBirth,
      'gender': gender,
      'looking_for': lookingFor,
      'bio': bio,
      'city': city,
      'country': country,
      'latitude': latitude,
      'longitude': longitude,
    };
  }

  String get displayName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    } else if (firstName != null) {
      return firstName!;
    } else if (username != null) {
      return username!;
    }
    return 'User $userId';
  }
}