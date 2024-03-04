from collections.abc import Sequence
from typing import Mapping
import sqlalchemy as sa
from app import db
from app.models import User
from flask_wtf import FlaskForm
from wtforms import (StringField, 
                     PasswordField, 
                     BooleanField, 
                     SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired,
                                ValidationError,
                                Email,
                                EqualTo,
                                Length)

class LoginForms(FlaskForm):   #A classe forms está herdando os atributos da class FlaskFrom
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #O Flask-WTF cuida automaticamente do processo de validação. Então assim que o formulário é submetido
    #As duas funções são chamadas e verificadas.
    #validate_ + o nome do campo da variável que foi criada a a ser validada
    def validate_username(self, username):
        user = db.session.scalar(
            sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Nome de usuário já existente. Escolha outro!')
        
    def validate_email(self, email):
        email = db.session.scalar(
            sa.select(User).where(User.email == email.data))
        if email is not None:
            raise ValidationError('Email já cadastrado. Escolha outro!')
        
class EditProfileForm(FlaskForm):
    username = StringField('Novo nome', validators=[DataRequired()])
    about_me = TextAreaField('Digite algo sobre você', validators=[Length(min=0, max=140)])
    submit = SubmitField('Enviar')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):    
        if username.data != self.original_username:   #Verifico se o nome é diferente do original
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data)) #Acesso ao db para verificar se o nome está disponível
            if user is not None:                      #Nome de usuário já existente
                raise ValidationError('Por favor, use um nome de usuário diferente')