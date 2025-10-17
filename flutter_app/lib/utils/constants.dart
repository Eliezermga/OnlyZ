class ApiConstants {
  // Change this to your API URL
  static const String baseUrl = 'http://localhost:3000/api';
  
  // Auth endpoints
  static const String register = '$baseUrl/auth/register';
  static const String login = '$baseUrl/auth/login';
  
  // Profile endpoints
  static const String myProfile = '$baseUrl/profiles/me';
  static const String profiles = '$baseUrl/profiles';
  static const String uploadPicture = '$baseUrl/profiles/me/picture';
  
  // Likes endpoints
  static const String likes = '$baseUrl/likes';
  static const String likesGiven = '$baseUrl/likes/given';
  static const String likesReceived = '$baseUrl/likes/received';
  
  // Matches endpoints
  static const String matches = '$baseUrl/matches';
  
  // Messages endpoints
  static const String messages = '$baseUrl/messages';
  static const String conversations = '$baseUrl/messages/conversations';
}

class AppColors {
  static const primaryColor = Color(0xFFE91E63);
  static const secondaryColor = Color(0xFF9C27B0);
  static const accentColor = Color(0xFFFF4081);
  static const backgroundColor = Color(0xFFF5F5F5);
  static const cardColor = Color(0xFFFFFFFF);
  static const textPrimary = Color(0xFF212121);
  static const textSecondary = Color(0xFF757575);
}

class AppStrings {
  static const String appName = 'OnlyZ';
  static const String tagline = 'Find Your Perfect Match';
  
  // Auth
  static const String login = 'Login';
  static const String register = 'Register';
  static const String email = 'Email';
  static const String password = 'Password';
  static const String username = 'Username';
  static const String forgotPassword = 'Forgot Password?';
  static const String dontHaveAccount = "Don't have an account?";
  static const String alreadyHaveAccount = 'Already have an account?';
  
  // Profile
  static const String profile = 'Profile';
  static const String editProfile = 'Edit Profile';
  static const String firstName = 'First Name';
  static const String lastName = 'Last Name';
  static const String dateOfBirth = 'Date of Birth';
  static const String gender = 'Gender';
  static const String lookingFor = 'Looking For';
  static const String bio = 'Bio';
  static const String city = 'City';
  static const String country = 'Country';
  
  // Browse
  static const String browse = 'Browse';
  static const String discover = 'Discover';
  static const String filters = 'Filters';
  
  // Matches
  static const String matches = 'Matches';
  static const String itsAMatch = "It's a Match!";
  
  // Messages
  static const String messages = 'Messages';
  static const String typeMessage = 'Type a message...';
  static const String send = 'Send';
  
  // Actions
  static const String like = 'Like';
  static const String pass = 'Pass';
  static const String save = 'Save';
  static const String cancel = 'Cancel';
  static const String logout = 'Logout';
}

import 'package:flutter/material.dart';