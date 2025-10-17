const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/auth');
const db = require('../database');

// Like a user
router.post('/:userId', authMiddleware, (req, res) => {
  const { userId } = req.params;
  const likerId = req.userId;

  // Can't like yourself
  if (parseInt(userId) === likerId) {
    return res.status(400).json({ error: 'Cannot like yourself' });
  }

  // Check if user exists
  db.get('SELECT id FROM users WHERE id = ?', [userId], (err, user) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Insert like
    db.run(
      'INSERT INTO likes (liker_id, liked_id) VALUES (?, ?)',
      [likerId, userId],
      function(err) {
        if (err) {
          if (err.message.includes('UNIQUE constraint failed')) {
            return res.status(400).json({ error: 'Already liked this user' });
          }
          return res.status(500).json({ error: 'Error creating like' });
        }

        // Check if it's a match (mutual like)
        db.get(
          'SELECT id FROM likes WHERE liker_id = ? AND liked_id = ?',
          [userId, likerId],
          (err, reverseLike) => {
            if (err) {
              return res.status(500).json({ error: 'Database error' });
            }

            const isMatch = !!reverseLike;

            if (isMatch) {
              // Create match record
              const user1 = Math.min(likerId, parseInt(userId));
              const user2 = Math.max(likerId, parseInt(userId));
              
              db.run(
                'INSERT OR IGNORE INTO matches (user1_id, user2_id) VALUES (?, ?)',
                [user1, user2]
              );
            }

            res.status(201).json({
              message: 'Like created successfully',
              isMatch: isMatch
            });
          }
        );
      }
    );
  });
});

// Unlike a user
router.delete('/:userId', authMiddleware, (req, res) => {
  const { userId } = req.params;
  const likerId = req.userId;

  db.run(
    'DELETE FROM likes WHERE liker_id = ? AND liked_id = ?',
    [likerId, userId],
    function(err) {
      if (err) {
        return res.status(500).json({ error: 'Error removing like' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'Like not found' });
      }

      // Remove match if it exists
      const user1 = Math.min(likerId, parseInt(userId));
      const user2 = Math.max(likerId, parseInt(userId));
      
      db.run(
        'DELETE FROM matches WHERE user1_id = ? AND user2_id = ?',
        [user1, user2]
      );

      res.json({ message: 'Like removed successfully' });
    }
  );
});

// Get users I've liked
router.get('/given', authMiddleware, (req, res) => {
  db.all(
    `SELECT p.*, u.username, l.created_at as liked_at
     FROM likes l
     JOIN users u ON l.liked_id = u.id
     LEFT JOIN profiles p ON u.id = p.user_id
     WHERE l.liker_id = ?
     ORDER BY l.created_at DESC`,
    [req.userId],
    (err, likes) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      // Calculate ages
      likes = likes.map(like => {
        if (like.date_of_birth) {
          const birthDate = new Date(like.date_of_birth);
          const today = new Date();
          let age = today.getFullYear() - birthDate.getFullYear();
          const monthDiff = today.getMonth() - birthDate.getMonth();
          if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
          }
          like.age = age;
        }
        return like;
      });

      res.json(likes);
    }
  );
});

// Get users who liked me
router.get('/received', authMiddleware, (req, res) => {
  db.all(
    `SELECT p.*, u.username, l.created_at as liked_at
     FROM likes l
     JOIN users u ON l.liker_id = u.id
     LEFT JOIN profiles p ON u.id = p.user_id
     WHERE l.liked_id = ?
     ORDER BY l.created_at DESC`,
    [req.userId],
    (err, likes) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      // Calculate ages
      likes = likes.map(like => {
        if (like.date_of_birth) {
          const birthDate = new Date(like.date_of_birth);
          const today = new Date();
          let age = today.getFullYear() - birthDate.getFullYear();
          const monthDiff = today.getMonth() - birthDate.getMonth();
          if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
          }
          like.age = age;
        }
        return like;
      });

      res.json(likes);
    }
  );
});

module.exports = router;