import 'package:flutter/material.dart';
import '../services/profile_service.dart';
import '../services/match_service.dart';
import '../models/user.dart';
import '../utils/constants.dart';
import '../widgets/profile_card.dart';

class BrowseScreen extends StatefulWidget {
  const BrowseScreen({super.key});

  @override
  State<BrowseScreen> createState() => _BrowseScreenState();
}

class _BrowseScreenState extends State<BrowseScreen> {
  final _profileService = ProfileService();
  final _matchService = MatchService();
  
  List<Profile> _profiles = [];
  int _currentIndex = 0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProfiles();
  }

  Future<void> _loadProfiles() async {
    setState(() => _isLoading = true);
    final profiles = await _profileService.browseProfiles(limit: 20);
    setState(() {
      _profiles = profiles;
      _isLoading = false;
    });
  }

  Future<void> _likeProfile() async {
    if (_currentIndex >= _profiles.length) return;

    final profile = _profiles[_currentIndex];
    final result = await _matchService.likeUser(profile.userId);

    if (result['success'] && result['isMatch']) {
      if (!mounted) return;
      _showMatchDialog(profile);
    }

    _nextProfile();
  }

  void _passProfile() {
    _nextProfile();
  }

  void _nextProfile() {
    setState(() {
      if (_currentIndex < _profiles.length - 1) {
        _currentIndex++;
      } else {
        // Load more profiles
        _loadProfiles();
        _currentIndex = 0;
      }
    });
  }

  void _showMatchDialog(Profile profile) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.favorite, color: AppColors.primaryColor),
            const SizedBox(width: 8),
            const Text("It's a Match!"),
          ],
        ),
        content: Text(
          'You and ${profile.displayName} liked each other!',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Keep Browsing'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              // Navigate to messages
              setState(() => _currentIndex = 2);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryColor,
              foregroundColor: Colors.white,
            ),
            child: const Text('Send Message'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Discover'),
        backgroundColor: AppColors.primaryColor,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: () {
              // TODO: Show filters dialog
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _profiles.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.search_off,
                        size: 64,
                        color: AppColors.textSecondary,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No profiles found',
                        style: TextStyle(
                          fontSize: 18,
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: _loadProfiles,
                        child: const Text('Refresh'),
                      ),
                    ],
                  ),
                )
              : Column(
                  children: [
                    Expanded(
                      child: ProfileCard(
                        profile: _profiles[_currentIndex],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          // Pass button
                          FloatingActionButton(
                            onPressed: _passProfile,
                            backgroundColor: Colors.white,
                            child: Icon(
                              Icons.close,
                              color: Colors.red[400],
                              size: 32,
                            ),
                          ),
                          // Like button
                          FloatingActionButton(
                            onPressed: _likeProfile,
                            backgroundColor: AppColors.primaryColor,
                            child: const Icon(
                              Icons.favorite,
                              color: Colors.white,
                              size: 32,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
    );
  }
}