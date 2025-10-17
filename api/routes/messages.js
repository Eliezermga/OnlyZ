const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const authMiddleware = require('../middleware/auth');
const db = require('../database');

// Get conversations list
router.get('/conversations', authMiddleware, (req, res) => {
  db.all(
    `SELECT DISTINCT
       CASE 
         WHEN m.sender_id = ? THEN m.receiver_id
         ELSE m.sender_id
       END as other_user_id,
       u.username,
       p.profile_picture,
       p.first_name,
       p.last_name,
       (SELECT content FROM messages 
        WHERE (sender_id = ? AND receiver_id = other_user_id) 
           OR (sender_id = other_user_id AND receiver_id = ?)
        ORDER BY created_at DESC LIMIT 1) as last_message,
       (SELECT created_at FROM messages 
        WHERE (sender_id = ? AND receiver_id = other_user_id) 
           OR (sender_id = other_user_id AND receiver_id = ?)
        ORDER BY created_at DESC LIMIT 1) as last_message_at,
       (SELECT COUNT(*) FROM messages 
        WHERE sender_id = other_user_id AND receiver_id = ? AND is_read = 0) as unread_count
     FROM messages m
     JOIN users u ON (
       CASE 
         WHEN m.sender_id = ? THEN m.receiver_id = u.id
         ELSE m.sender_id = u.id
       END
     )
     LEFT JOIN profiles p ON u.id = p.user_id
     WHERE m.sender_id = ? OR m.receiver_id = ?
     ORDER BY last_message_at DESC`,
    [req.userId, req.userId, req.userId, req.userId, req.userId, req.userId, req.userId, req.userId, req.userId],
    (err, conversations) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }

      res.json(conversations);
    }
  );
});

// Get messages with specific user
router.get('/:userId', authMiddleware, (req, res) => {
  const { userId } = req.params;
  const { limit = 50, offset = 0 } = req.query;

  // Check if users are matched
  const user1 = Math.min(req.userId, parseInt(userId));
  const user2 = Math.max(req.userId, parseInt(userId));

  db.get(
    'SELECT id FROM matches WHERE user1_id = ? AND user2_id = ?',
    [user1, user2],
    (err, match) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      if (!match) {
        return res.status(403).json({ error: 'Not matched with this user' });
      }

      // Get messages
      db.all(
        `SELECT m.*, 
                u.username as sender_username
         FROM messages m
         JOIN users u ON m.sender_id = u.id
         WHERE (m.sender_id = ? AND m.receiver_id = ?) 
            OR (m.sender_id = ? AND m.receiver_id = ?)
         ORDER BY m.created_at DESC
         LIMIT ? OFFSET ?`,
        [req.userId, userId, userId, req.userId, parseInt(limit), parseInt(offset)],
        (err, messages) => {
          if (err) {
            return res.status(500).json({ error: 'Database error' });
          }

          // Mark messages as read
          db.run(
            'UPDATE messages SET is_read = 1 WHERE sender_id = ? AND receiver_id = ? AND is_read = 0',
            [userId, req.userId]
          );

          res.json(messages.reverse());
        }
      );
    }
  );
});

// Send message
router.post('/:userId',
  authMiddleware,
  [
    body('content').trim().notEmpty().withMessage('Message content is required')
      .isLength({ max: 1000 }).withMessage('Message must be less than 1000 characters')
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { userId } = req.params;
    const { content } = req.body;

    // Check if users are matched
    const user1 = Math.min(req.userId, parseInt(userId));
    const user2 = Math.max(req.userId, parseInt(userId));

    db.get(
      'SELECT id FROM matches WHERE user1_id = ? AND user2_id = ?',
      [user1, user2],
      (err, match) => {
        if (err) {
          return res.status(500).json({ error: 'Database error' });
        }

        if (!match) {
          return res.status(403).json({ error: 'Not matched with this user' });
        }

        // Insert message
        db.run(
          'INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)',
          [req.userId, userId, content],
          function(err) {
            if (err) {
              return res.status(500).json({ error: 'Error sending message' });
            }

            res.status(201).json({
              id: this.lastID,
              sender_id: req.userId,
              receiver_id: parseInt(userId),
              content: content,
              is_read: 0,
              created_at: new Date().toISOString()
            });
          }
        );
      }
    );
  }
);

// Mark messages as read
router.put('/:userId/read', authMiddleware, (req, res) => {
  const { userId } = req.params;

  db.run(
    'UPDATE messages SET is_read = 1 WHERE sender_id = ? AND receiver_id = ? AND is_read = 0',
    [userId, req.userId],
    function(err) {
      if (err) {
        return res.status(500).json({ error: 'Error marking messages as read' });
      }

      res.json({
        message: 'Messages marked as read',
        count: this.changes
      });
    }
  );
});

module.exports = router;