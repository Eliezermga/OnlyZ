# 🚀 Guide de Démarrage Rapide - OnlyZ

## ⚡ Démarrage en 5 minutes

### 1️⃣ Lancer l'API (Backend)

```bash
# Ouvrir un terminal
cd api

# Installer les dépendances
npm install

# Lancer l'API
npm start
```

✅ L'API sera accessible sur **http://localhost:3000**

---

### 2️⃣ Lancer l'Application Flutter (Frontend)

```bash
# Ouvrir un nouveau terminal
cd flutter_app

# Installer les dépendances
flutter pub get

# Lancer l'application
flutter run
```

✅ L'application se lancera sur votre émulateur/appareil

---

## 📱 Tester l'Application

### Créer un compte

1. Ouvrez l'application
2. Cliquez sur **"Register"**
3. Remplissez le formulaire :
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
4. Cliquez sur **"Register"**

### Configurer votre profil

1. Remplissez vos informations :
   - Prénom et nom
   - Date de naissance
   - Genre
   - Ce que vous recherchez
   - Bio
   - Ville et pays
2. Cliquez sur **"Complete Profile"**

### Explorer l'application

- **Browse** : Parcourez les profils et likez
- **Matches** : Voyez vos matchs
- **Messages** : Chattez avec vos matchs
- **Profile** : Gérez votre profil

---

## 🔧 Configuration Rapide

### Pour Émulateur Android

Dans `flutter_app/lib/utils/constants.dart`, utilisez :

```dart
static const String baseUrl = 'http://10.0.2.2:3000/api';
```

### Pour Émulateur iOS

Dans `flutter_app/lib/utils/constants.dart`, utilisez :

```dart
static const String baseUrl = 'http://localhost:3000/api';
```

### Pour Appareil Physique

1. Trouvez votre IP locale :
   ```bash
   # Sur Mac/Linux
   ifconfig | grep "inet "
   
   # Sur Windows
   ipconfig
   ```

2. Dans `flutter_app/lib/utils/constants.dart`, utilisez :
   ```dart
   static const String baseUrl = 'http://VOTRE_IP:3000/api';
   ```

---

## 🧪 Tester l'API avec cURL

### Inscription
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'
```

### Connexion
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

### Health Check
```bash
curl http://localhost:3000/api/health
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez **API_FLUTTER_README.md**

---

## ❓ Problèmes Courants

### L'API ne démarre pas

**Erreur :** `Port 3000 already in use`

**Solution :**
```bash
# Trouver le processus
lsof -i :3000

# Tuer le processus
kill -9 <PID>
```

### L'app Flutter ne se connecte pas

**Solution :**
1. Vérifiez que l'API est lancée
2. Vérifiez l'URL dans `constants.dart`
3. Pour Android émulateur, utilisez `10.0.2.2` au lieu de `localhost`

### Erreur "flutter: command not found"

**Solution :**
```bash
# Installer Flutter
# Suivez les instructions sur https://flutter.dev/docs/get-started/install
```

---

## 🎉 C'est tout !

Vous êtes prêt à utiliser OnlyZ ! 

Pour toute question, consultez la documentation complète dans **API_FLUTTER_README.md**