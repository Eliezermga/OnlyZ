const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/auth');
const db = require('../database');

// Get all matches for current user
router.get('/', authMiddleware, (req, res) => {
  db.all(
    `SELECT DISTINCT
       CASE 
         WHEN m.user1_id = ? THEN m.user2_id
         ELSE m.user1_id
       END as matched_user_id,
       p.*,
       u.username,
       m.created_at as matched_at
     FROM matches m
     JOIN users u ON (
       CASE 
         WHEN m.user1_id = ? THEN m.user2_id = u.id
         ELSE m.user1_id = u.id
       END
     )
     LEFT JOIN profiles p ON u.id = p.user_id
     WHERE m.user1_id = ? OR m.user2_id = ?
     ORDER BY m.created_at DESC`,
    [req.userId, req.userId, req.userId, req.userId],
    (err, matches) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }

      // Calculate ages
      matches = matches.map(match => {
        if (match.date_of_birth) {
          const birthDate = new Date(match.date_of_birth);
          const today = new Date();
          let age = today.getFullYear() - birthDate.getFullYear();
          const monthDiff = today.getMonth() - birthDate.getMonth();
          if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
          }
          match.age = age;
        }
        return match;
      });

      res.json(matches);
    }
  );
});

// Check if matched with specific user
router.get('/:userId', authMiddleware, (req, res) => {
  const { userId } = req.params;
  const user1 = Math.min(req.userId, parseInt(userId));
  const user2 = Math.max(req.userId, parseInt(userId));

  db.get(
    'SELECT * FROM matches WHERE user1_id = ? AND user2_id = ?',
    [user1, user2],
    (err, match) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      res.json({
        isMatch: !!match,
        matchedAt: match ? match.created_at : null
      });
    }
  );
});

module.exports = router;