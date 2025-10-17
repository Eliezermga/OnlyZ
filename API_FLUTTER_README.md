# 📱 OnlyZ - API REST & Application Flutter

## 🎯 Vue d'ensemble

Ce projet comprend deux composants principaux :
1. **API REST** - Backend Node.js/Express avec SQLite
2. **Application Flutter** - Application mobile multiplateforme

L'API fournit tous les endpoints nécessaires pour gérer l'authentification, les profils, les likes, les matchs et la messagerie. L'application Flutter consomme cette API pour offrir une expérience utilisateur complète.

---

## 📁 Structure du Projet

```
onlyz-repo/
├── api/                          # Backend API REST
│   ├── routes/                   # Routes de l'API
│   │   ├── auth.js              # Authentification (register, login)
│   │   ├── profiles.js          # Gestion des profils
│   │   ├── likes.js             # Système de likes
│   │   ├── matches.js           # Gestion des matchs
│   │   └── messages.js          # Messagerie
│   ├── middleware/
│   │   └── auth.js              # Middleware d'authentification JWT
│   ├── database.js              # Configuration SQLite
│   ├── index.js                 # Point d'entrée de l'API
│   ├── .env                     # Variables d'environnement
│   ├── .env.example             # Exemple de configuration
│   └── package.json             # Dépendances Node.js
│
├── flutter_app/                 # Application Flutter
│   ├── lib/
│   │   ├── models/              # Modèles de données
│   │   │   ├── user.dart
│   │   │   └── message.dart
│   │   ├── services/            # Services API
│   │   │   ├── auth_service.dart
│   │   │   ├── profile_service.dart
│   │   │   ├── match_service.dart
│   │   │   └── message_service.dart
│   │   ├── screens/             # Écrans de l'application
│   │   │   ├── login_screen.dart
│   │   │   ├── register_screen.dart
│   │   │   ├── profile_setup_screen.dart
│   │   │   ├── home_screen.dart
│   │   │   ├── browse_screen.dart
│   │   │   ├── matches_screen.dart
│   │   │   ├── messages_screen.dart
│   │   │   ├── chat_screen.dart
│   │   │   └── profile_screen.dart
│   │   ├── widgets/             # Widgets réutilisables
│   │   │   └── profile_card.dart
│   │   ├── utils/               # Utilitaires
│   │   │   └── constants.dart
│   │   └── main.dart            # Point d'entrée Flutter
│   └── pubspec.yaml             # Dépendances Flutter
│
└── API_FLUTTER_README.md        # Ce fichier
```

---

## 🚀 Installation et Configuration

### Prérequis

- **Node.js** 18+ et npm
- **Flutter** 3.0+ (pour l'application mobile)
- **Git**

### 1️⃣ Installation de l'API

#### Étape 1 : Naviguer vers le dossier API

```bash
cd api
```

#### Étape 2 : Installer les dépendances

```bash
npm install
```

#### Étape 3 : Configurer les variables d'environnement

Créez un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
```

Modifiez le fichier `.env` selon vos besoins :

```env
# Server Configuration
PORT=3000
NODE_ENV=development

# JWT Secret (IMPORTANT: Changez ceci en production!)
JWT_SECRET=votre_cle_secrete_super_securisee_ici

# Database
DB_PATH=./database.sqlite

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
```

⚠️ **IMPORTANT** : Changez `JWT_SECRET` en production avec une clé aléatoire sécurisée !

#### Étape 4 : Créer le dossier uploads

```bash
mkdir uploads
```

#### Étape 5 : Lancer l'API

```bash
npm start
```

L'API sera accessible sur `http://localhost:3000`

Pour le développement avec rechargement automatique :

```bash
npm run dev
```

---

### 2️⃣ Installation de l'Application Flutter

#### Étape 1 : Naviguer vers le dossier Flutter

```bash
cd flutter_app
```

#### Étape 2 : Installer les dépendances Flutter

```bash
flutter pub get
```

#### Étape 3 : Configurer l'URL de l'API

Ouvrez `lib/utils/constants.dart` et modifiez l'URL de base :

```dart
class ApiConstants {
  // Pour émulateur Android
  static const String baseUrl = 'http://10.0.2.2:3000/api';
  
  // Pour émulateur iOS ou appareil physique sur le même réseau
  // static const String baseUrl = 'http://192.168.1.X:3000/api';
  
  // Pour production
  // static const String baseUrl = 'https://votre-domaine.com/api';
}
```

**Notes importantes :**
- **Émulateur Android** : Utilisez `10.0.2.2` au lieu de `localhost`
- **Émulateur iOS** : Utilisez `localhost` ou l'IP de votre machine
- **Appareil physique** : Utilisez l'IP locale de votre machine (ex: `192.168.1.10`)

#### Étape 4 : Lancer l'application

```bash
flutter run
```

Ou pour un appareil/émulateur spécifique :

```bash
# Android
flutter run -d android

# iOS
flutter run -d ios

# Chrome (web)
flutter run -d chrome
```

---

## 📡 Documentation de l'API

### Base URL

```
http://localhost:3000/api
```

### Authentification

Toutes les routes protégées nécessitent un token JWT dans le header :

```
Authorization: Bearer <votre_token_jwt>
```

---

### 🔐 Endpoints d'Authentification

#### 1. Inscription

**POST** `/api/auth/register`

**Body :**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Réponse (201) :**
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### 2. Connexion

**POST** `/api/auth/login`

**Body :**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Réponse (200) :**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

---

### 👤 Endpoints de Profil

#### 1. Obtenir mon profil

**GET** `/api/profiles/me`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
{
  "id": 1,
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1995-05-15",
  "gender": "man",
  "looking_for": "woman",
  "bio": "Passionate about travel and photography",
  "profile_picture": "profile-1234567890.jpg",
  "city": "Paris",
  "country": "France",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "age": 28,
  "username": "johndoe",
  "email": "john@example.com"
}
```

#### 2. Créer/Mettre à jour mon profil

**POST** `/api/profiles/me`

**Headers :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1995-05-15",
  "gender": "man",
  "looking_for": "woman",
  "bio": "Passionate about travel and photography",
  "city": "Paris",
  "country": "France",
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

**Réponse (200) :**
```json
{
  "message": "Profile updated successfully"
}
```

#### 3. Upload photo de profil

**POST** `/api/profiles/me/picture`

**Headers :** `Authorization: Bearer <token>`

**Body :** `multipart/form-data`
- `picture`: fichier image (JPG, PNG, GIF)

**Réponse (200) :**
```json
{
  "message": "Profile picture updated successfully",
  "filename": "profile-1234567890.jpg",
  "url": "/uploads/profile-1234567890.jpg"
}
```

#### 4. Parcourir les profils

**GET** `/api/profiles?gender=woman&min_age=25&max_age=35&city=Paris&limit=20&offset=0`

**Headers :** `Authorization: Bearer <token>`

**Query Parameters :**
- `gender` (optionnel) : "man", "woman", "other"
- `min_age` (optionnel) : âge minimum
- `max_age` (optionnel) : âge maximum
- `city` (optionnel) : ville
- `limit` (optionnel, défaut: 20) : nombre de résultats
- `offset` (optionnel, défaut: 0) : pagination

**Réponse (200) :**
```json
[
  {
    "id": 2,
    "user_id": 2,
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1997-08-20",
    "gender": "woman",
    "looking_for": "man",
    "bio": "Love hiking and cooking",
    "profile_picture": "profile-9876543210.jpg",
    "city": "Paris",
    "country": "France",
    "age": 26,
    "username": "janesmith"
  }
]
```

#### 5. Obtenir un profil spécifique

**GET** `/api/profiles/:userId`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :** Même format que "Obtenir mon profil"

---

### ❤️ Endpoints de Likes

#### 1. Liker un utilisateur

**POST** `/api/likes/:userId`

**Headers :** `Authorization: Bearer <token>`

**Réponse (201) :**
```json
{
  "message": "Like created successfully",
  "isMatch": true
}
```

**Note :** `isMatch` est `true` si l'autre utilisateur vous a également liké (match mutuel)

#### 2. Unliker un utilisateur

**DELETE** `/api/likes/:userId`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
{
  "message": "Like removed successfully"
}
```

#### 3. Obtenir les likes donnés

**GET** `/api/likes/given`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
[
  {
    "user_id": 2,
    "username": "janesmith",
    "first_name": "Jane",
    "profile_picture": "profile-9876543210.jpg",
    "age": 26,
    "liked_at": "2024-01-15T10:30:00.000Z"
  }
]
```

#### 4. Obtenir les likes reçus

**GET** `/api/likes/received`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :** Même format que "likes donnés"

---

### 💕 Endpoints de Matchs

#### 1. Obtenir tous mes matchs

**GET** `/api/matches`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
[
  {
    "matched_user_id": 2,
    "user_id": 2,
    "username": "janesmith",
    "first_name": "Jane",
    "last_name": "Smith",
    "profile_picture": "profile-9876543210.jpg",
    "age": 26,
    "city": "Paris",
    "bio": "Love hiking and cooking",
    "matched_at": "2024-01-15T10:30:00.000Z"
  }
]
```

#### 2. Vérifier si matché avec un utilisateur

**GET** `/api/matches/:userId`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
{
  "isMatch": true,
  "matchedAt": "2024-01-15T10:30:00.000Z"
}
```

---

### 💬 Endpoints de Messages

#### 1. Obtenir la liste des conversations

**GET** `/api/messages/conversations`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
[
  {
    "other_user_id": 2,
    "username": "janesmith",
    "profile_picture": "profile-9876543210.jpg",
    "first_name": "Jane",
    "last_name": "Smith",
    "last_message": "Hey! How are you?",
    "last_message_at": "2024-01-15T14:30:00.000Z",
    "unread_count": 2
  }
]
```

#### 2. Obtenir les messages avec un utilisateur

**GET** `/api/messages/:userId?limit=50&offset=0`

**Headers :** `Authorization: Bearer <token>`

**Query Parameters :**
- `limit` (optionnel, défaut: 50)
- `offset` (optionnel, défaut: 0)

**Réponse (200) :**
```json
[
  {
    "id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "content": "Hello!",
    "is_read": true,
    "created_at": "2024-01-15T14:25:00.000Z",
    "sender_username": "johndoe"
  },
  {
    "id": 2,
    "sender_id": 2,
    "receiver_id": 1,
    "content": "Hey! How are you?",
    "is_read": true,
    "created_at": "2024-01-15T14:30:00.000Z",
    "sender_username": "janesmith"
  }
]
```

#### 3. Envoyer un message

**POST** `/api/messages/:userId`

**Headers :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "content": "Hello! Nice to match with you!"
}
```

**Réponse (201) :**
```json
{
  "id": 3,
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Hello! Nice to match with you!",
  "is_read": 0,
  "created_at": "2024-01-15T14:35:00.000Z"
}
```

#### 4. Marquer les messages comme lus

**PUT** `/api/messages/:userId/read`

**Headers :** `Authorization: Bearer <token>`

**Réponse (200) :**
```json
{
  "message": "Messages marked as read",
  "count": 2
}
```

---

## 🎨 Architecture de l'Application Flutter

### Modèles de Données

#### User
```dart
class User {
  final int id;
  final String username;
  final String email;
}
```

#### Profile
```dart
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
}
```

#### Message
```dart
class Message {
  final int id;
  final int senderId;
  final int receiverId;
  final String content;
  final bool isRead;
  final String createdAt;
  final String? senderUsername;
}
```

#### Conversation
```dart
class Conversation {
  final int otherUserId;
  final String username;
  final String? profilePicture;
  final String? firstName;
  final String? lastName;
  final String? lastMessage;
  final String? lastMessageAt;
  final int unreadCount;
}
```

---

### Services

#### AuthService
Gère l'authentification et le stockage du token JWT.

**Méthodes principales :**
- `register()` - Inscription
- `login()` - Connexion
- `logout()` - Déconnexion
- `getToken()` - Récupérer le token
- `getUser()` - Récupérer l'utilisateur
- `isLoggedIn()` - Vérifier si connecté

#### ProfileService
Gère les profils utilisateurs.

**Méthodes principales :**
- `getMyProfile()` - Obtenir mon profil
- `getProfile(userId)` - Obtenir un profil
- `updateProfile(profile)` - Mettre à jour le profil
- `uploadProfilePicture(imageFile)` - Upload photo
- `browseProfiles()` - Parcourir les profils

#### MatchService
Gère les likes et matchs.

**Méthodes principales :**
- `likeUser(userId)` - Liker un utilisateur
- `unlikeUser(userId)` - Unliker
- `getLikesGiven()` - Likes donnés
- `getLikesReceived()` - Likes reçus
- `getMatches()` - Obtenir les matchs
- `isMatched(userId)` - Vérifier un match

#### MessageService
Gère la messagerie.

**Méthodes principales :**
- `getConversations()` - Liste des conversations
- `getMessages(userId)` - Messages avec un utilisateur
- `sendMessage(userId, content)` - Envoyer un message
- `markAsRead(userId)` - Marquer comme lu

---

### Écrans Principaux

#### 1. LoginScreen
- Formulaire de connexion
- Validation des champs
- Navigation vers RegisterScreen
- Redirection vers HomeScreen après connexion

#### 2. RegisterScreen
- Formulaire d'inscription
- Validation des champs (email, mot de passe, etc.)
- Navigation vers ProfileSetupScreen après inscription

#### 3. ProfileSetupScreen
- Configuration initiale du profil
- Champs : nom, prénom, date de naissance, genre, etc.
- Navigation vers HomeScreen après configuration

#### 4. HomeScreen
- Navigation par onglets (Bottom Navigation)
- 4 onglets : Browse, Matches, Messages, Profile

#### 5. BrowseScreen
- Affichage des profils sous forme de cartes
- Boutons Like/Pass
- Détection de match avec dialogue
- Chargement automatique de nouveaux profils

#### 6. MatchesScreen
- Grille de tous les matchs
- Affichage des photos de profil
- Clic pour voir les détails

#### 7. MessagesScreen
- Liste des conversations
- Affichage du dernier message
- Badge de messages non lus
- Navigation vers ChatScreen

#### 8. ChatScreen
- Interface de chat en temps réel
- Affichage des messages
- Envoi de messages
- Marquage automatique comme lu

#### 9. ProfileScreen
- Affichage du profil utilisateur
- Informations personnelles
- Bouton de déconnexion
- Bouton d'édition (à implémenter)

---

## 🔧 Configuration Avancée

### Changer le Port de l'API

Modifiez le fichier `.env` :

```env
PORT=8080
```

### Utiliser PostgreSQL au lieu de SQLite

1. Installer PostgreSQL :
```bash
npm install pg
```

2. Modifier `database.js` pour utiliser PostgreSQL

3. Mettre à jour `.env` :
```env
DATABASE_URL=postgresql://user:password@localhost:5432/onlyz
```

### Activer HTTPS en Production

1. Obtenir un certificat SSL (Let's Encrypt)
2. Configurer un reverse proxy (Nginx)
3. Mettre à jour l'URL dans l'app Flutter

---

## 🧪 Tests

### Tester l'API avec cURL

#### Inscription
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Connexion
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Obtenir mon profil
```bash
curl -X GET http://localhost:3000/api/profiles/me \
  -H "Authorization: Bearer <votre_token>"
```

### Tester avec Postman

1. Importer la collection Postman (à créer)
2. Configurer l'environnement avec l'URL de base
3. Tester tous les endpoints

---

## 🐛 Dépannage

### L'API ne démarre pas

**Problème :** Port déjà utilisé
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution :**
```bash
# Trouver le processus
lsof -i :3000

# Tuer le processus
kill -9 <PID>

# Ou changer le port dans .env
PORT=3001
```

### L'application Flutter ne se connecte pas à l'API

**Problème :** Erreur de connexion réseau

**Solutions :**
1. Vérifier que l'API est bien lancée
2. Vérifier l'URL dans `constants.dart`
3. Pour Android émulateur, utiliser `10.0.2.2` au lieu de `localhost`
4. Pour appareil physique, utiliser l'IP locale de votre machine
5. Vérifier le firewall

### Erreur "Invalid token"

**Problème :** Token JWT expiré ou invalide

**Solution :**
1. Se reconnecter pour obtenir un nouveau token
2. Vérifier que `JWT_SECRET` est le même partout
3. Vérifier la date d'expiration du token (7 jours par défaut)

### Images ne s'affichent pas

**Problème :** Chemin d'upload incorrect

**Solution :**
1. Vérifier que le dossier `uploads` existe
2. Vérifier les permissions du dossier
3. Vérifier l'URL complète de l'image dans l'app

---

## 🚀 Déploiement en Production

### Déployer l'API

#### Option 1 : Heroku

```bash
# Installer Heroku CLI
heroku login

# Créer une app
heroku create onlyz-api

# Déployer
git push heroku main

# Configurer les variables d'environnement
heroku config:set JWT_SECRET=votre_cle_secrete
heroku config:set NODE_ENV=production
```

#### Option 2 : VPS (DigitalOcean, AWS, etc.)

```bash
# Se connecter au VPS
ssh user@your-server-ip

# Cloner le projet
git clone <votre-repo>
cd onlyz-repo/api

# Installer les dépendances
npm install --production

# Installer PM2 pour gérer le processus
npm install -g pm2

# Lancer l'API
pm2 start index.js --name onlyz-api

# Configurer le démarrage automatique
pm2 startup
pm2 save
```

#### Option 3 : Docker

```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

```bash
# Build
docker build -t onlyz-api .

# Run
docker run -p 3000:3000 --env-file .env onlyz-api
```

### Déployer l'Application Flutter

#### Android (Google Play Store)

```bash
# Build APK
flutter build apk --release

# Build App Bundle (recommandé pour Play Store)
flutter build appbundle --release
```

#### iOS (App Store)

```bash
# Build iOS
flutter build ios --release

# Ouvrir Xcode pour soumettre
open ios/Runner.xcworkspace
```

#### Web

```bash
# Build web
flutter build web --release

# Déployer sur Firebase Hosting, Netlify, etc.
```

---

## 📊 Base de Données

### Schéma SQLite

#### Table `users`
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Table `profiles`
```sql
CREATE TABLE profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER UNIQUE NOT NULL,
  first_name TEXT,
  last_name TEXT,
  date_of_birth DATE NOT NULL,
  gender TEXT NOT NULL,
  looking_for TEXT NOT NULL,
  bio TEXT,
  profile_picture TEXT,
  city TEXT,
  country TEXT,
  latitude REAL,
  longitude REAL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Table `likes`
```sql
CREATE TABLE likes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  liker_id INTEGER NOT NULL,
  liked_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (liker_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (liked_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE(liker_id, liked_id)
);
```

#### Table `matches`
```sql
CREATE TABLE matches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user1_id INTEGER NOT NULL,
  user2_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE(user1_id, user2_id)
);
```

#### Table `messages`
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  receiver_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  is_read INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Table `blocks`
```sql
CREATE TABLE blocks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  blocker_id INTEGER NOT NULL,
  blocked_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (blocker_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (blocked_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE(blocker_id, blocked_id)
);
```

---

## 🔒 Sécurité

### Bonnes Pratiques Implémentées

✅ Mots de passe hashés avec bcrypt
✅ Authentification JWT
✅ Validation des entrées utilisateur
✅ Protection contre les injections SQL (parameterized queries)
✅ Limitation de taille des fichiers uploadés
✅ CORS configuré

### Recommandations Supplémentaires

- [ ] Implémenter le rate limiting
- [ ] Ajouter la validation d'email
- [ ] Implémenter la réinitialisation de mot de passe
- [ ] Ajouter la vérification en deux étapes (2FA)
- [ ] Implémenter le refresh token
- [ ] Ajouter des logs de sécurité
- [ ] Configurer HTTPS en production
- [ ] Implémenter le blocage d'utilisateurs

---

## 📈 Améliorations Futures

### Fonctionnalités à Ajouter

- [ ] Notifications push
- [ ] Géolocalisation en temps réel
- [ ] Filtres avancés de recherche
- [ ] Vérification de profil (badge vérifié)
- [ ] Stories (comme Instagram)
- [ ] Appels vidéo
- [ ] Partage de photos dans le chat
- [ ] Traduction automatique des messages
- [ ] Mode sombre
- [ ] Statistiques de profil
- [ ] Abonnement premium
- [ ] Signalement et modération
- [ ] Algorithme de recommandation ML

### Optimisations Techniques

- [ ] Mise en cache avec Redis
- [ ] Pagination optimisée
- [ ] Compression des images
- [ ] CDN pour les assets
- [ ] WebSockets pour le chat en temps réel
- [ ] Tests unitaires et d'intégration
- [ ] CI/CD pipeline
- [ ] Monitoring et analytics

---

## 📝 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.

---

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📞 Support

Pour toute question ou problème :

- Ouvrir une issue sur GitHub
- Consulter la documentation
- Contacter l'équipe de développement

---

## 🎉 Remerciements

Merci d'utiliser OnlyZ ! Nous espérons que cette application vous aidera à créer des connexions significatives.

**Développé avec ❤️ par l'équipe OnlyZ**

---

## 📚 Ressources Supplémentaires

### Documentation

- [Node.js Documentation](https://nodejs.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [Flutter Documentation](https://docs.flutter.dev/)
- [JWT Introduction](https://jwt.io/introduction)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### Tutoriels

- [Building REST APIs with Node.js](https://nodejs.dev/learn)
- [Flutter for Beginners](https://flutter.dev/docs/get-started/codelab)
- [JWT Authentication Best Practices](https://auth0.com/blog/jwt-authentication-best-practices/)

### Outils Utiles

- [Postman](https://www.postman.com/) - Tester l'API
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Visualiser la base de données
- [Flutter DevTools](https://flutter.dev/docs/development/tools/devtools) - Déboguer l'app Flutter

---

**Version :** 1.0.0  
**Dernière mise à jour :** Janvier 2024