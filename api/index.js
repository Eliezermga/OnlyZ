require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve uploaded files
app.use('/uploads', express.static(path.join(__dirname, process.env.UPLOAD_DIR || 'uploads')));

// Import routes
const authRoutes = require('./routes/auth');
const profileRoutes = require('./routes/profiles');
const likeRoutes = require('./routes/likes');
const matchRoutes = require('./routes/matches');
const messageRoutes = require('./routes/messages');

// Use routes
app.use('/api/auth', authRoutes);
app.use('/api/profiles', profileRoutes);
app.use('/api/likes', likeRoutes);
app.use('/api/matches', matchRoutes);
app.use('/api/messages', messageRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'OnlyZ API is running',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to OnlyZ API',
    version: '1.0.0',
    endpoints: {
      auth: {
        register: 'POST /api/auth/register',
        login: 'POST /api/auth/login'
      },
      profiles: {
        getMyProfile: 'GET /api/profiles/me',
        updateProfile: 'POST /api/profiles/me',
        uploadPicture: 'POST /api/profiles/me/picture',
        browseProfiles: 'GET /api/profiles',
        getProfile: 'GET /api/profiles/:userId'
      },
      likes: {
        likeUser: 'POST /api/likes/:userId',
        unlikeUser: 'DELETE /api/likes/:userId',
        getLikesGiven: 'GET /api/likes/given',
        getLikesReceived: 'GET /api/likes/received'
      },
      matches: {
        getMatches: 'GET /api/matches',
        checkMatch: 'GET /api/matches/:userId'
      },
      messages: {
        getConversations: 'GET /api/messages/conversations',
        getMessages: 'GET /api/messages/:userId',
        sendMessage: 'POST /api/messages/:userId',
        markAsRead: 'PUT /api/messages/:userId/read'
      }
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 OnlyZ API server running on port ${PORT}`);
  console.log(`📍 API URL: http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/api/health`);
});

module.exports = app;