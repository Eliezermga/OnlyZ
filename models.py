from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()

# Table d’association Many-to-Many entre profils et intérêts
profile_interests = db.Table(
    'profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = "users"  # ⚠️ éviter "user" (mot réservé PostgreSQL)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_terms = db.Column(db.Boolean, default=False, nullable=False)

    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")
    sent_messages = db.relationship("Message", foreign_keys="Message.sender_id", backref="sender", lazy="dynamic", cascade="all, delete-orphan")
    received_messages = db.relationship("Message", foreign_keys="Message.receiver_id", backref="receiver", lazy="dynamic", cascade="all, delete-orphan")
    likes_given = db.relationship("Like", foreign_keys="Like.liker_id", backref="liker", lazy="dynamic", cascade="all, delete-orphan")
    likes_received = db.relationship("Like", foreign_keys="Like.liked_id", backref="liked", lazy="dynamic", cascade="all, delete-orphan")
    reports_made = db.relationship("Report", foreign_keys="Report.reporter_id", backref="reporter", lazy="dynamic", cascade="all, delete-orphan")
    reports_received = db.relationship("Report", foreign_keys="Report.reported_id", backref="reported_user", lazy="dynamic", cascade="all, delete-orphan")
    blocks_made = db.relationship("Block", foreign_keys="Block.blocker_id", backref="blocker", lazy="dynamic", cascade="all, delete-orphan")
    blocks_received = db.relationship("Block", foreign_keys="Block.blocked_id", backref="blocked_user", lazy="dynamic", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def get_matches(self):
        likes_i_gave = [like.liked_id for like in self.likes_given.all()]
        likes_i_received = [like.liker_id for like in self.likes_received.all()]
        matches = list(set(likes_i_gave) & set(likes_i_received))
        return User.query.filter(User.id.in_(matches)).all()

    def has_liked(self, user_id):
        return self.likes_given.filter_by(liked_id=user_id).first() is not None

    def is_matched(self, user_id):
        return (
            self.has_liked(user_id)
            and Like.query.filter_by(liker_id=user_id, liked_id=self.id).first() is not None
        )

    def has_blocked(self, user_id):
        return self.blocks_made.filter_by(blocked_id=user_id).first() is not None

    def is_blocked_by(self, user_id):
        return Block.query.filter_by(blocker_id=user_id, blocked_id=self.id).first() is not None


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    looking_for = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)

    profile_picture = db.Column(db.String(255))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    interests = db.relationship("Interest", secondary=profile_interests, backref="profiles")

    def get_age(self):
        if self.date_of_birth:
            today = datetime.utcnow().date()
            age = today.year - self.date_of_birth.year
            if (
                today.month < self.date_of_birth.month
                or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day)
            ):
                age -= 1
            return age
        return None

    def get_distance(self, other_profile):
        if self.latitude and self.longitude and other_profile.latitude and other_profile.longitude:
            from geopy.distance import geodesic

            coords_1 = (self.latitude, self.longitude)
            coords_2 = (other_profile.latitude, other_profile.longitude)
            return geodesic(coords_1, coords_2).kilometers
        return None


class Interest(db.Model):
    __tablename__ = "interests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Interest {self.name}>"


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    liked_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("liker_id", "liked_id", name="unique_like"),)

    def is_match(self):
        reverse_like = Like.query.filter_by(liker_id=self.liked_id, liked_id=self.liker_id).first()
        return reverse_like is not None


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Message from {self.sender_id} to {self.receiver_id}>"


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reported_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")

    __table_args__ = (db.UniqueConstraint("reporter_id", "reported_id", name="unique_report"),)


class Block(db.Model):
    __tablename__ = "blocks"

    id = db.Column(db.Integer, primary_key=True)
    blocker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    blocked_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("blocker_id", "blocked_id", name="unique_block"),)


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    related_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship("User", foreign_keys=[user_id], backref="notifications")
    related_user = db.relationship("User", foreign_keys=[related_user_id])
