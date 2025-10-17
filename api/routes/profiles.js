const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const authMiddleware = require('../middleware/auth');
const db = require('../database');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Configure multer for file uploads
const uploadDir = process.env.UPLOAD_DIR || './uploads';
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'profile-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: parseInt(process.env.MAX_FILE_SIZE) || 5242880 }, // 5MB default
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed!'));
    }
  }
});

// Get current user's profile
router.get('/me', authMiddleware, (req, res) => {
  db.get(
    `SELECT p.*, u.username, u.email 
     FROM profiles p 
     JOIN users u ON p.user_id = u.id 
     WHERE p.user_id = ?`,
    [req.userId],
    (err, profile) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }
      
      if (!profile) {
        return res.status(404).json({ error: 'Profile not found' });
      }

      // Calculate age
      if (profile.date_of_birth) {
        const birthDate = new Date(profile.date_of_birth);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        profile.age = age;
      }

      res.json(profile);
    }
  );
});

// Get profile by user ID
router.get('/:userId', authMiddleware, (req, res) => {
  const { userId } = req.params;

  db.get(
    `SELECT p.*, u.username 
     FROM profiles p 
     JOIN users u ON p.user_id = u.id 
     WHERE p.user_id = ?`,
    [userId],
    (err, profile) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }
      
      if (!profile) {
        return res.status(404).json({ error: 'Profile not found' });
      }

      // Calculate age
      if (profile.date_of_birth) {
        const birthDate = new Date(profile.date_of_birth);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        profile.age = age;
      }

      res.json(profile);
    }
  );
});

// Create or update profile
router.post('/me',
  authMiddleware,
  [
    body('date_of_birth').isISO8601().withMessage('Invalid date format'),
    body('gender').notEmpty().withMessage('Gender is required'),
    body('looking_for').notEmpty().withMessage('Looking for is required'),
    body('bio').optional().isLength({ max: 500 }).withMessage('Bio must be less than 500 characters')
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const {
      first_name,
      last_name,
      date_of_birth,
      gender,
      looking_for,
      bio,
      city,
      country,
      latitude,
      longitude
    } = req.body;

    // Check if profile exists
    db.get('SELECT id FROM profiles WHERE user_id = ?', [req.userId], (err, profile) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      if (profile) {
        // Update existing profile
        db.run(
          `UPDATE profiles SET 
           first_name = ?, last_name = ?, date_of_birth = ?, gender = ?, 
           looking_for = ?, bio = ?, city = ?, country = ?, latitude = ?, longitude = ?
           WHERE user_id = ?`,
          [first_name, last_name, date_of_birth, gender, looking_for, bio, city, country, latitude, longitude, req.userId],
          function(err) {
            if (err) {
              return res.status(500).json({ error: 'Error updating profile' });
            }
            res.json({ message: 'Profile updated successfully' });
          }
        );
      } else {
        // Create new profile
        db.run(
          `INSERT INTO profiles 
           (user_id, first_name, last_name, date_of_birth, gender, looking_for, bio, city, country, latitude, longitude)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [req.userId, first_name, last_name, date_of_birth, gender, looking_for, bio, city, country, latitude, longitude],
          function(err) {
            if (err) {
              return res.status(500).json({ error: 'Error creating profile' });
            }
            res.status(201).json({ message: 'Profile created successfully' });
          }
        );
      }
    });
  }
);

// Upload profile picture
router.post('/me/picture', authMiddleware, upload.single('picture'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const filename = req.file.filename;

  // Update profile with new picture
  db.run(
    'UPDATE profiles SET profile_picture = ? WHERE user_id = ?',
    [filename, req.userId],
    function(err) {
      if (err) {
        return res.status(500).json({ error: 'Error updating profile picture' });
      }

      if (this.changes === 0) {
        return res.status(404).json({ error: 'Profile not found' });
      }

      res.json({
        message: 'Profile picture updated successfully',
        filename: filename,
        url: `/uploads/${filename}`
      });
    }
  );
});

// Browse profiles with filters
router.get('/', authMiddleware, (req, res) => {
  const { gender, min_age, max_age, city, limit = 20, offset = 0 } = req.query;

  let query = `
    SELECT p.*, u.username 
    FROM profiles p 
    JOIN users u ON p.user_id = u.id 
    WHERE p.user_id != ?
  `;
  const params = [req.userId];

  // Add filters
  if (gender) {
    query += ' AND p.gender = ?';
    params.push(gender);
  }

  if (city) {
    query += ' AND p.city LIKE ?';
    params.push(`%${city}%`);
  }

  // Age filtering (calculated from date_of_birth)
  if (min_age) {
    const maxBirthDate = new Date();
    maxBirthDate.setFullYear(maxBirthDate.getFullYear() - parseInt(min_age));
    query += ' AND p.date_of_birth <= ?';
    params.push(maxBirthDate.toISOString().split('T')[0]);
  }

  if (max_age) {
    const minBirthDate = new Date();
    minBirthDate.setFullYear(minBirthDate.getFullYear() - parseInt(max_age) - 1);
    query += ' AND p.date_of_birth >= ?';
    params.push(minBirthDate.toISOString().split('T')[0]);
  }

  query += ' ORDER BY RANDOM() LIMIT ? OFFSET ?';
  params.push(parseInt(limit), parseInt(offset));

  db.all(query, params, (err, profiles) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }

    // Calculate ages
    profiles = profiles.map(profile => {
      if (profile.date_of_birth) {
        const birthDate = new Date(profile.date_of_birth);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        profile.age = age;
      }
      return profile;
    });

    res.json(profiles);
  });
});

module.exports = router;