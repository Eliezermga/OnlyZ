# Onlyz - Site de Rencontre Moderne

Onlyz est un site de rencontre complet développé en Python avec Flask, offrant toutes les fonctionnalités modernes d'une plateforme de rencontre sécurisée et performante.

## 🎯 Fonctionnalités

### Gestion des Utilisateurs
- ✅ Inscription avec email, pseudo et mot de passe sécurisé (hashé avec bcrypt)
- ✅ Connexion et déconnexion
- ✅ Vérification d'email à l'inscription
- ✅ Réinitialisation du mot de passe par email
- ✅ Suppression de compte

### Profils Utilisateurs
- ✅ Upload de photos de profil (JPG, PNG, GIF)
- ✅ Bio / description personnalisée
- ✅ Genre et orientation sexuelle (qui je recherche)
- ✅ Âge / date de naissance (restriction +18 ans)
- ✅ Localisation (ville, pays) avec géolocalisation automatique

### Système de Matching
- ✅ Parcourir les profils avec filtres (âge, genre, distance)
- ✅ Système de "like" intuitif
- ✅ Système de "match" mutuel (notification instantanée)
- ✅ Affichage des matchs

### Messagerie en Temps Réel
- ✅ Chat privé entre utilisateurs matchés
- ✅ Notifications en temps réel avec Flask-SocketIO
- ✅ Historique des conversations
- ✅ Blocage et signalement d'utilisateurs

### Recherche Avancée
- ✅ Recherche par âge (min/max)
- ✅ Recherche par genre
- ✅ Recherche par distance géographique (calcul avec geopy)
- ✅ Recherche par mots-clés dans la bio

### Algorithme de Recommandation Intelligent
L'algorithme propose des profils en priorité selon :
- Proximité géographique (<10km = +50 points, <50km = +30 points, <100km = +10 points)
- Compatibilité genre/orientation
- Différence d'âge (<5 ans = +30 points, <10 ans = +15 points)
- Intérêts communs (+10 points par intérêt partagé)

### Sécurité
- ✅ Mots de passe hashés avec Werkzeug/bcrypt
- ✅ Protection CSRF avec Flask-WTF
- ✅ Validation complète des formulaires
- ✅ Upload sécurisé des fichiers
- ✅ Limitation de taille des fichiers (16 MB max)

### Notifications
- ✅ Email de confirmation d'inscription
- ✅ Email de nouveau match
- ✅ Email de nouveau message
- ✅ Notifications in-app en temps réel

### Interface Utilisateur
- ✅ Design moderne et responsive avec TailwindCSS
- ✅ Interface intuitive et attractive
- ✅ Expérience utilisateur optimisée

## 🛠 Technologies Utilisées

### Backend
- **Flask** - Framework web Python
- **Flask-Login** - Gestion d'authentification
- **Flask-SQLAlchemy** - ORM pour la base de données
- **Flask-Migrate** - Migrations de base de données
- **Flask-WTF** - Formulaires et protection CSRF
- **Flask-SocketIO** - Communication en temps réel
- **Flask-Mail** - Envoi d'emails
- **PostgreSQL** - Base de données relationnelle
- **Bcrypt** - Hashage sécurisé des mots de passe
- **Pillow** - Traitement d'images
- **Geopy** - Géolocalisation et calcul de distances

### Frontend
- **TailwindCSS** - Framework CSS moderne
- **Socket.IO Client** - WebSockets côté client
- **JavaScript Vanilla** - Interactions dynamiques

## 📋 Prérequis

- Python 3.11 ou supérieur
- PostgreSQL 12 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation Locale

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd onlyz
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install flask flask-login flask-sqlalchemy flask-migrate flask-wtf flask-socketio flask-mail bcrypt pillow python-dotenv email-validator geopy werkzeug psycopg2-binary python-socketio
```

### 4. Configurer la base de données

Créez une base de données PostgreSQL :

```bash
createdb onlyz
```

### 5. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql://username:password@localhost:5432/onlyz
SESSION_SECRET=votre_cle_secrete_aleatoire

# Configuration email (optionnel)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre_email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_app
MAIL_DEFAULT_SENDER=noreply@onlyz.com
```

**Note pour Gmail** : Si vous utilisez Gmail, vous devez générer un "mot de passe d'application" dans les paramètres de sécurité de votre compte Google.

### 6. Initialiser la base de données

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

Ou avec Flask-Migrate :

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur http://localhost:5000

## 📁 Structure du Projet

```
onlyz/
├── app.py                          # Application principale Flask
├── models.py                       # Modèles de base de données
├── forms.py                        # Formulaires Flask-WTF
├── .env                           # Variables d'environnement (ne pas commiter)
├── .env.example                   # Exemple de configuration
├── requirements.txt               # Dépendances Python (optionnel)
├── app/
│   ├── templates/                 # Templates Jinja2
│   │   ├── base.html             # Template de base
│   │   ├── index.html            # Page d'accueil
│   │   ├── register.html         # Inscription
│   │   ├── login.html            # Connexion
│   │   ├── profile_form.html     # Création/Édition profil
│   │   ├── profile.html          # Affichage profil
│   │   ├── my_profile.html       # Mon profil
│   │   ├── browse.html           # Parcourir les profils
│   │   ├── recommendations.html  # Suggestions personnalisées
│   │   ├── search.html           # Recherche avancée
│   │   ├── matches.html          # Mes matchs
│   │   ├── chat.html             # Messagerie
│   │   └── notifications.html    # Notifications
│   └── static/
│       └── uploads/
│           └── profiles/         # Photos de profil
└── migrations/                    # Migrations de base de données
```

## 🗄 Modèle de Données

### Tables Principales

- **User** : Utilisateurs (id, username, email, password_hash, is_verified, etc.)
- **Profile** : Profils utilisateurs (bio, genre, looking_for, date_of_birth, localisation, etc.)
- **Like** : Likes entre utilisateurs
- **Message** : Messages entre utilisateurs matchés
- **Match** : Calculé automatiquement via les likes mutuels
- **Report** : Signalements d'utilisateurs
- **Block** : Blocages d'utilisateurs
- **Notification** : Notifications in-app
- **Interest** : Centres d'intérêt (extensible)

## 🌐 Déploiement en Production

### Recommandations Générales

1. **Ne jamais utiliser le serveur de développement Flask en production**
2. **Utiliser un serveur WSGI comme Gunicorn ou uWSGI**
3. **Activer HTTPS avec un certificat SSL**
4. **Configurer un reverse proxy (Nginx, Apache)**
5. **Utiliser un service de stockage cloud pour les images (AWS S3, Cloudinary)**
6. **Configurer des sauvegardes régulières de la base de données**


### Déploiement sur VPS (DigitalOcean, AWS, etc.)

```bash
# Installer les dépendances système
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# Cloner le projet
git clone <votre-repo>
cd onlyz

# Installer les dépendances Python
pip3 install -r requirements.txt
pip3 install gunicorn

# Configurer PostgreSQL
sudo -u postgres createuser onlyz
sudo -u postgres createdb onlyz
sudo -u postgres psql -c "ALTER USER onlyz WITH PASSWORD 'password';"

# Lancer avec Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# Configurer Nginx comme reverse proxy
# Créer /etc/nginx/sites-available/onlyz
server {
    listen 80;
    server_name votredomaine.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /chemin/vers/onlyz/app/static;
    }
}

# Activer le site
sudo ln -s /etc/nginx/sites-available/onlyz /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🔒 Sécurité

### Bonnes Pratiques Implémentées

- ✅ Mots de passe hashés (jamais stockés en clair)
- ✅ Protection CSRF sur tous les formulaires
- ✅ Validation des entrées utilisateur
- ✅ Upload sécurisé des fichiers avec vérification d'extension
- ✅ Sessions sécurisées avec clé secrète
- ✅ Vérification d'email avant activation du compte
- ✅ Limitation de taille des uploads (16 MB)

### Améliorations Recommandées pour la Production

- [ ] Authentification à deux facteurs (2FA)
- [ ] Captcha anti-bot à l'inscription (reCAPTCHA)
- [ ] Rate limiting sur les routes sensibles
- [ ] Logs de sécurité et monitoring
- [ ] Scan antivirus des fichiers uploadés
- [ ] Politique de mot de passe renforcée
- [ ] Headers de sécurité HTTP (CSP, HSTS, etc.)

## 📧 Configuration Email

### Gmail

1. Activez la vérification en 2 étapes sur votre compte Google
2. Générez un "mot de passe d'application" : https://myaccount.google.com/apppasswords
3. Utilisez ce mot de passe dans `MAIL_PASSWORD`

### SendGrid

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=votre_cle_api_sendgrid
```

### Mailgun

```env
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=postmaster@votre-domaine.mailgun.org
MAIL_PASSWORD=votre_mot_de_passe_mailgun
```

## 🧪 Tests

### Créer des utilisateurs de test

```python
from app import app, db
from models import User, Profile
from datetime import date

with app.app_context():
    # Créer un utilisateur
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    user.is_verified = True
    db.session.add(user)
    db.session.commit()
    
    # Créer un profil
    profile = Profile(
        user_id=user.id,
        date_of_birth=date(1995, 1, 1),
        gender='homme',
        looking_for='femme',
        bio='Utilisateur de test',
        city='Paris',
        country='France'
    )
    db.session.add(profile)
    db.session.commit()
```

## 🐛 Dépannage

### Erreur de connexion à la base de données

Vérifiez que :
- PostgreSQL est lancé : `sudo service postgresql status`
- La variable `DATABASE_URL` est correcte dans `.env`
- L'utilisateur PostgreSQL a les permissions nécessaires

### Les emails ne sont pas envoyés

- Vérifiez les variables d'environnement `MAIL_*`
- Si vous utilisez Gmail, vérifiez que vous utilisez un mot de passe d'application
- Vérifiez les logs pour voir les erreurs spécifiques

### Les images ne s'affichent pas

- Vérifiez que le dossier `app/static/uploads/profiles/` existe
- Vérifiez les permissions du dossier : `chmod 755 app/static/uploads/profiles/`

### Erreur "Module not found"

Assurez-vous d'avoir activé l'environnement virtuel et installé toutes les dépendances :
```bash
source venv/bin/activate
pip install -r requirements.txt
```


## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📞 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur le repository.

---

**Développé avec ❤️ en Python et Flask**
