import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_migrate import Migrate
from flask_mail import Mail, Message as EmailMessage
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import os
from dotenv import load_dotenv

from models import db, User, Profile, Like, Message, Report, Block, Notification, Interest
from forms import (RegistrationForm, LoginForm, ProfileForm, SearchForm, 
                      MessageForm, ReportForm, ResetPasswordRequestForm, ResetPasswordForm)

load_dotenv()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', os.urandom(24).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {
        'sslmode': 'require',
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5
    }
}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'app/static/uploads/profiles'

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@onlyz.com')

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))
    return render_template('index.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            accepted_terms=True
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            
            if not user.profile:
                return redirect(url_for('create_profile'))
            
            return redirect(next_page) if next_page else redirect(url_for('browse'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if not admin_password:
            flash('Configuration admin manquante. Contactez l\'administrateur système.', 'danger')
            return redirect(url_for('index'))
        
        if password and password == admin_password:
            admin_user = User.query.filter_by(username='admin').first()
            
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@onlyz.com',
                    accepted_terms=True,
                    is_admin=True
                )
                admin_user.set_password(admin_password)
                db.session.add(admin_user)
                db.session.commit()
            else:
                admin_user.is_admin = True
                admin_user.set_password(admin_password)
                db.session.commit()
            
            login_user(admin_user)
            flash('Bienvenue dans l\'espace administrateur', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Mot de passe administrateur incorrect', 'danger')
    
    return render_template('admin_login.html')


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Accès refusé. Cette page est réservée aux administrateurs.', 'danger')
        return redirect(url_for('index'))
    
    total_users = User.query.count()
    total_profiles = Profile.query.count()
    total_matches = Like.query.count()
    total_messages = Message.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_reports = Report.query.order_by(Report.created_at.desc()).limit(10).all()
    
    return render_template('admin.html', 
                         total_users=total_users,
                         total_profiles=total_profiles,
                         total_matches=total_matches,
                         total_messages=total_messages,
                         recent_users=recent_users,
                         recent_reports=recent_reports)


@app.route('/profile/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    if current_user.profile:
        return redirect(url_for('edit_profile'))
    
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile(
            user_id=current_user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            looking_for=form.looking_for.data,
            bio=form.bio.data,
            city=form.city.data,
            country=form.country.data
        )
        
        if form.city.data and form.country.data:
            try:
                geolocator = Nominatim(user_agent="onlyz_app")
                location = geolocator.geocode(f"{form.city.data}, {form.country.data}")
                if location:
                    profile.latitude = location.latitude
                    profile.longitude = location.longitude
            except:
                pass
        
        if form.profile_picture.data:
            file = form.profile_picture.data
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                profile.profile_picture = f"uploads/profiles/{filename}"
        
        db.session.add(profile)
        db.session.commit()
        
        flash('Profil créé avec succès !', 'success')
        return redirect(url_for('browse'))
    
    return render_template('profile_form.html', form=form, title='Créer mon profil')


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if not current_user.profile:
        return redirect(url_for('create_profile'))
    
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.date_of_birth = form.date_of_birth.data
        current_user.profile.gender = form.gender.data
        current_user.profile.looking_for = form.looking_for.data
        current_user.profile.bio = form.bio.data
        current_user.profile.city = form.city.data
        current_user.profile.country = form.country.data
        
        if form.city.data and form.country.data:
            try:
                geolocator = Nominatim(user_agent="onlyz_app")
                location = geolocator.geocode(f"{form.city.data}, {form.country.data}")
                if location:
                    current_user.profile.latitude = location.latitude
                    current_user.profile.longitude = location.longitude
            except:
                pass
        
        if form.profile_picture.data:
            file = form.profile_picture.data
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                current_user.profile.profile_picture = f"uploads/profiles/{filename}"
        
        db.session.commit()
        flash('Profil mis à jour !', 'success')
        return redirect(url_for('my_profile'))
    
    elif request.method == 'GET':
        form.first_name.data = current_user.profile.first_name
        form.last_name.data = current_user.profile.last_name
        form.date_of_birth.data = current_user.profile.date_of_birth
        form.gender.data = current_user.profile.gender
        form.looking_for.data = current_user.profile.looking_for
        form.bio.data = current_user.profile.bio
        form.city.data = current_user.profile.city
        form.country.data = current_user.profile.country
    
    return render_template('profile_form.html', form=form, title='Éditer mon profil')


@app.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    if not user.profile:
        flash('Ce profil n\'existe pas', 'danger')
        return redirect(url_for('browse'))
    
    if current_user.has_blocked(user_id) or current_user.is_blocked_by(user_id):
        flash('Vous ne pouvez pas voir ce profil', 'danger')
        return redirect(url_for('browse'))
    
    has_liked = current_user.has_liked(user_id)
    is_matched = current_user.is_matched(user_id)
    distance = None
    
    if current_user.profile and user.profile:
        distance = current_user.profile.get_distance(user.profile)
    
    return render_template('profile.html', user=user, has_liked=has_liked, 
                         is_matched=is_matched, distance=distance)


@app.route('/profile/me')
@login_required
def my_profile():
    if not current_user.profile:
        return redirect(url_for('create_profile'))
    return render_template('my_profile.html', user=current_user)


@app.route('/browse')
@login_required
def browse():
    if not current_user.profile:
        return redirect(url_for('create_profile'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    blocked_users = [block.blocked_id for block in current_user.blocks_made.all()]
    blocked_by = [block.blocker_id for block in current_user.blocks_received.all()]
    all_blocked = list(set(blocked_users + blocked_by + [current_user.id]))
    
    query = User.query.join(Profile).filter(
        User.id.notin_(all_blocked),
        Profile.looking_for.in_([current_user.profile.gender, 'tous'])
    )
    
    if current_user.profile.looking_for != 'tous':
        query = query.filter(Profile.gender == current_user.profile.looking_for)
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('browse.html', users=users)


@app.route('/recommendations')
@login_required
def recommendations():
    if not current_user.profile:
        return redirect(url_for('create_profile'))
    
    recommended_users = get_recommendations(current_user)
    return render_template('recommendations.html', users=recommended_users)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if not current_user.profile:
        return redirect(url_for('create_profile'))
    
    form = SearchForm()
    results = []
    
    if form.validate_on_submit() or request.method == 'GET':
        blocked_users = [block.blocked_id for block in current_user.blocks_made.all()]
        blocked_by = [block.blocker_id for block in current_user.blocks_received.all()]
        all_blocked = list(set(blocked_users + blocked_by + [current_user.id]))
        
        query = User.query.join(Profile).filter(User.id.notin_(all_blocked))
        
        if form.gender.data:
            query = query.filter(Profile.gender == form.gender.data)
        
        if form.min_age.data:
            max_birth_date = datetime.utcnow().date() - timedelta(days=form.min_age.data * 365)
            query = query.filter(Profile.date_of_birth <= max_birth_date)
        
        if form.max_age.data:
            min_birth_date = datetime.utcnow().date() - timedelta(days=form.max_age.data * 365)
            query = query.filter(Profile.date_of_birth >= min_birth_date)
        
        if form.keywords.data:
            query = query.filter(Profile.bio.ilike(f"%{form.keywords.data}%"))
        
        results = query.all()
        
        if form.max_distance.data and current_user.profile.latitude and current_user.profile.longitude:
            filtered_results = []
            for user in results:
                if user.profile.latitude and user.profile.longitude:
                    distance = current_user.profile.get_distance(user.profile)
                    if distance and distance <= form.max_distance.data:
                        filtered_results.append(user)
            results = filtered_results
    
    return render_template('search.html', form=form, results=results)


@app.route('/like/<int:user_id>', methods=['POST'])
@login_required
def like_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user_id == current_user.id:
        return jsonify({'error': 'Vous ne pouvez pas vous liker vous-même'}), 400
    
    if current_user.has_blocked(user_id) or current_user.is_blocked_by(user_id):
        return jsonify({'error': 'Action impossible'}), 400
    
    existing_like = Like.query.filter_by(liker_id=current_user.id, liked_id=user_id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'is_match': False})
    
    like = Like(liker_id=current_user.id, liked_id=user_id)
    db.session.add(like)
    db.session.commit()
    
    is_match = like.is_match()
    
    if is_match:
        notif1 = Notification(
            user_id=current_user.id,
            type='match',
            content=f'Vous avez un nouveau match avec {user.username} !',
            related_user_id=user_id
        )
        notif2 = Notification(
            user_id=user_id,
            type='match',
            content=f'Vous avez un nouveau match avec {current_user.username} !',
            related_user_id=current_user.id
        )
        db.session.add(notif1)
        db.session.add(notif2)
        db.session.commit()
        
        send_match_email(current_user, user)
        send_match_email(user, current_user)
    
    return jsonify({'status': 'liked', 'is_match': is_match})


@app.route('/matches')
@login_required
def matches():
    if not current_user.profile:
        return redirect(url_for('create_profile'))
    
    matched_users = current_user.get_matches()
    return render_template('matches.html', users=matched_users)


@app.route('/chat/<int:user_id>')
@login_required
def chat(user_id):
    user = User.query.get_or_404(user_id)
    
    if not current_user.is_matched(user_id):
        flash('Vous devez d\'abord matcher avec cette personne', 'warning')
        return redirect(url_for('matches'))
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    Message.query.filter_by(sender_id=user_id, receiver_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    
    return render_template('chat.html', other_user=user, messages=messages)


@app.route('/report/<int:user_id>', methods=['POST'])
@login_required
def report_user(user_id):
    user = User.query.get_or_404(user_id)
    reason = request.form.get('reason', '')
    
    if not reason:
        flash('Veuillez indiquer une raison', 'danger')
        return redirect(url_for('view_profile', user_id=user_id))
    
    existing_report = Report.query.filter_by(reporter_id=current_user.id, reported_id=user_id).first()
    
    if existing_report:
        flash('Vous avez déjà signalé cet utilisateur', 'warning')
    else:
        report = Report(reporter_id=current_user.id, reported_id=user_id, reason=reason)
        db.session.add(report)
        db.session.commit()
        flash('Utilisateur signalé', 'success')
    
    return redirect(url_for('browse'))


@app.route('/block/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    
    existing_block = Block.query.filter_by(blocker_id=current_user.id, blocked_id=user_id).first()
    
    if existing_block:
        flash('Vous avez déjà bloqué cet utilisateur', 'warning')
    else:
        block = Block(blocker_id=current_user.id, blocked_id=user_id)
        db.session.add(block)
        db.session.commit()
        flash('Utilisateur bloqué', 'success')
    
    return redirect(url_for('browse'))


@app.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(50).all()
    
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    
    return render_template('notifications.html', notifications=notifs)


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{current_user.username} a rejoint la conversation'}, room=room)


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{current_user.username} a quitté la conversation'}, room=room)


@socketio.on('send_message')
def handle_message(data):
    receiver_id = data['receiver_id']
    content = data['content']
    
    if not current_user.is_matched(receiver_id):
        emit('error', {'msg': 'Vous n\'êtes pas matchés'})
        return
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    notif = Notification(
        user_id=receiver_id,
        type='message',
        content=f'Nouveau message de {current_user.username}',
        related_user_id=current_user.id
    )
    db.session.add(notif)
    db.session.commit()
    
    room = f"chat_{min(current_user.id, receiver_id)}_{max(current_user.id, receiver_id)}"
    emit('receive_message', {
        'sender_id': current_user.id,
        'sender_username': current_user.username,
        'content': content,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }, room=room)
    
    send_message_email(current_user, User.query.get(receiver_id))


def get_recommendations(user):
    if not user.profile:
        return []
    
    blocked_users = [block.blocked_id for block in user.blocks_made.all()]
    blocked_by = [block.blocker_id for block in user.blocks_received.all()]
    liked_users = [like.liked_id for like in user.likes_given.all()]
    all_excluded = list(set(blocked_users + blocked_by + liked_users + [user.id]))
    
    candidates = User.query.join(Profile).filter(
        User.id.notin_(all_excluded),
        Profile.looking_for.in_([user.profile.gender, 'tous'])
    ).all()
    
    if user.profile.looking_for != 'tous':
        candidates = [c for c in candidates if c.profile.gender == user.profile.looking_for]
    
    scored_candidates = []
    for candidate in candidates:
        score = 0
        
        if user.profile.latitude and user.profile.longitude and candidate.profile.latitude and candidate.profile.longitude:
            distance = user.profile.get_distance(candidate.profile)
            if distance:
                if distance < 10:
                    score += 50
                elif distance < 50:
                    score += 30
                elif distance < 100:
                    score += 10
        
        age_diff = abs(user.profile.get_age() - candidate.profile.get_age())
        if age_diff < 5:
            score += 30
        elif age_diff < 10:
            score += 15
        
        user_interests = set([i.id for i in user.profile.interests])
        candidate_interests = set([i.id for i in candidate.profile.interests])
        common_interests = len(user_interests & candidate_interests)
        score += common_interests * 10
        
        scored_candidates.append((candidate, score))
    
    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    return [c[0] for c in scored_candidates[:12]]


def send_match_email(user1, user2):
    if not app.config['MAIL_USERNAME']:
        return
    
    try:
        msg = EmailMessage(
            subject='Nouveau match sur Onlyz !',
            recipients=[user1.email]
        )
        msg.body = f'''Félicitations {user1.username} !

Vous avez un nouveau match avec {user2.username} !

Connectez-vous maintenant pour commencer à discuter :
{url_for('chat', user_id=user2.id, _external=True)}

L'équipe Onlyz
'''
        mail.send(msg)
    except:
        pass


def send_message_email(sender, receiver):
    if not app.config['MAIL_USERNAME']:
        return
    
    try:
        msg = EmailMessage(
            subject='Nouveau message sur Onlyz',
            recipients=[receiver.email]
        )
        msg.body = f'''Bonjour {receiver.username},

Vous avez reçu un nouveau message de {sender.username} !

Connectez-vous pour le lire :
{url_for('chat', user_id=sender.id, _external=True)}

L'équipe Onlyz
'''
        mail.send(msg)
    except:
        pass


if __name__ == '__main__':
    with app.app_context():
        # S'assurer que toutes les tables sont créées
        db.create_all()
        
        # Optionnel : créer quelques données de test si nécessaire
        if not User.query.first():
            print("Création des tables...")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)