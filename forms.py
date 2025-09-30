from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DateField, SelectField, SelectMultipleField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from datetime import datetime, timedelta
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(message='Le nom d\'utilisateur est requis'),
        Length(min=3, max=80, message='Le nom d\'utilisateur doit contenir entre 3 et 80 caractères')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Email(message='Email invalide')
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est requis'),
        Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(message='Veuillez confirmer votre mot de passe'),
        EqualTo('password', message='Les mots de passe ne correspondent pas')
    ])
    accept_terms = BooleanField('J\'accepte les conditions d\'utilisation et la politique de confidentialité', validators=[
        DataRequired(message='Vous devez accepter les conditions d\'utilisation et la politique de confidentialité')
    ])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà enregistré')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Email(message='Email invalide')
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est requis')
    ])
    remember_me = BooleanField('Se souvenir de moi')


class ProfileForm(FlaskForm):
    first_name = StringField('Prénom', validators=[Length(max=50)])
    last_name = StringField('Nom', validators=[Length(max=50)])
    date_of_birth = DateField('Date de naissance', validators=[DataRequired(message='La date de naissance est requise')])
    gender = SelectField('Genre', choices=[
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('non-binaire', 'Non-binaire'),
        ('autre', 'Autre')
    ], validators=[DataRequired(message='Le genre est requis')])
    looking_for = SelectField('Je recherche', choices=[
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('tous', 'Tous')
    ], validators=[DataRequired(message='Veuillez indiquer qui vous recherchez')])
    bio = TextAreaField('Bio', validators=[Length(max=500, message='La bio ne peut pas dépasser 500 caractères')])
    city = StringField('Ville', validators=[Length(max=100)])
    country = StringField('Pays', validators=[Length(max=100)])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    profile_picture = FileField('Photo de profil', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Seules les images sont autorisées')
    ])
    
    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth.data:
            age = (datetime.utcnow().date() - date_of_birth.data).days / 365.25
            if age < 18:
                raise ValidationError('Vous devez avoir au moins 18 ans pour vous inscrire')


class SearchForm(FlaskForm):
    min_age = IntegerField('Âge minimum', validators=[Optional()], default=18)
    max_age = IntegerField('Âge maximum', validators=[Optional()], default=99)
    gender = SelectField('Genre', choices=[
        ('', 'Tous'),
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('non-binaire', 'Non-binaire'),
        ('autre', 'Autre')
    ])
    max_distance = IntegerField('Distance maximum (km)', validators=[Optional()], default=100)
    keywords = StringField('Mots-clés dans la bio', validators=[Length(max=100)])


class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[
        DataRequired(message='Le message ne peut pas être vide'),
        Length(max=1000, message='Le message ne peut pas dépasser 1000 caractères')
    ])


class ReportForm(FlaskForm):
    reason = TextAreaField('Raison du signalement', validators=[
        DataRequired(message='Veuillez indiquer la raison du signalement'),
        Length(max=500, message='La raison ne peut pas dépasser 500 caractères')
    ])


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est requis'),
        Email(message='Email invalide')
    ])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[
        DataRequired(message='Le mot de passe est requis'),
        Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(message='Veuillez confirmer votre mot de passe'),
        EqualTo('password', message='Les mots de passe ne correspondent pas')
    ])
