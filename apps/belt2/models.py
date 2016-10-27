from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date, time
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class RegisterManager(models.Manager):
    def register(self, name, username, email, password, password_confirmation):
        message = []
        if  EMAIL_REGEX.match(email):
            print "email"
        else:
            message.append("Email is not valid")
        if len(name)>3:
            print "name"
        else:
            message.append("Please enter a valid first name")
        if len(username)>3:
            print "username"
        else:
            message.append("Please enter a valid last name")
        if len(password)>=8 and password == password_confirmation:
            print "password"
        else:
            message.append("Please enter a password containing at least 8 characters and/or make sure password matches the password confirmation.")
        if len(message)==0:
            pw_hash = bcrypt.hashpw(str(password), bcrypt.gensalt())
            registration = Users.registerManager.create(name=name, username=username,email=email, password=pw_hash)
            registration.save()
            print registration.id
            return (True, registration, registration.id)
        else:
            return (False, message)

class LoginManager(models.Manager):
    def login(self, email, password):
        login_message = []
        if len(email)==0:
            login_message.append("Email invalid.")
        elif not EMAIL_REGEX.match(email):
            login_message.append("Email invalid.")
        elif len(password) < 8:
            login_message.append("Password invalid.")
        if len(login_message)==0:
            login = Users.loginManager.filter(email=email)
            if len(login)<1:
                login_message.append("Email and/or Password invalid.")
            elif (bcrypt.checkpw(str(password), str(login[0].password))):
                return (True, login, login[0].id)
            else:
                login_message.append("Password invalid.")
            return (False, login_message)
        else:
            login_message.append("Email and/or Password invalid.")
            return (False, login_message)

class QuoteManager(models.Manager):
    def addquote(self, creator, message, user_id):
        quote_message = []
        if len(creator)<3:
            quote_message.append("Invalid quote creator!")
        elif len(message)<10:
            quote_message.append("Quote must be longer than 10 characters!")
        if len(quote_message)==0:
            return (True, '')
        else:
            quote_message.append("Quote creator/quote invalid.")
            return (False, quote_message)

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registerManager = RegisterManager()
    loginManager = LoginManager()

class Quotes(models.Model):
    creator = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(Users)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quoteManager = QuoteManager()

class Join(models.Model):
    user = models.ForeignKey(Users)
    quote = models.ForeignKey(Quotes)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
