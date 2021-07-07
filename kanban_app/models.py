from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
import re, bcrypt

from django.http import request

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USER_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')

class usermanager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['first_name'] = "User's first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "User's last name should be at least 2 characters"
        if len(postData['uname']) < 5:
            errors['username'] = "Username should be at least 5 characters"
        if not USER_REGEX.match(postData['uname']):
            errors['username'] = "Username should not have specialized symbols or spaces"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        User = self.filter(email=postData['email'])
        if User:
            errors['email'] = "Email is already in use"
        if len(postData['pw']) < 5:
            errors['password'] = "Password should be at least 8 characters long"
        if len(postData['pw']) > 32:
            errors['password len'] = "Password should be less than 32 characters"
        if postData['pw'] != postData['confpw']:
            errors['match'] = "Passwords should match each other"
        return errors

    def editvalid(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['first_name'] = "User's first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "User's last name should be at least 2 characters"
        if len(postData['uname']) < 5:
            errors['username'] = "Username should be at least 5 characters"
        if not USER_REGEX.match(postData['uname']):
            errors['username'] = "Username should not have specialized symbols or spaces"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"

        # find a way to check username and email is used but excluding this current user
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]

        return bcrypt.checkpw(password.encode(), user.password.encode())

    def checkpoint(self, User, verify):
        users = user.objects.get(id=User)
        return bcrypt.checkpw(verify.encode(), users.password.encode())

    def multipass(self, newpassword, matchnew):
        errors = {}
        if len(newpassword) < 5:
            errors['password'] = "Password should be at least 8 characters long"
        if len(newpassword) > 32:
            errors['password len'] = "Password should be less than 32 characters"
        if newpassword != matchnew:
            errors['match'] = "Passwords should match each other"


class colmanager(models.Manager):
    def nonull(self, postData):
        errors = {}
        if len(postData['coltitle']) < 1:
            errors['column_title'] = "Have at least one (1) character in the column title"
        return errors

class cardmanager(models.Manager):
    def validatecard(self, postData):
        errors = {}
        if len(postData['cardname']) < 1:
            errors['subject_line'] = "Have at least one (1) character in the subject line of a card"
        if len(postData['info']) < 2:
            errors['card_info'] = "Have at least two (2) characters in the information section of a card"
        return errors

# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    about_me = models.TextField(default="Some info should be here!")
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = usermanager()
    # user.user_boards
    # user.boards_imin
    # user.columns
    # user.cards
    # user.working_on

class board(models.Model):
    title = models.CharField(max_length=65)
    created_by = models.ForeignKey(user, related_name='user_boards', on_delete=CASCADE)
    board_group = models.ManyToManyField(user, related_name='boards_imin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # board.created_by.username
    # board.columns
    # board.columns.cards

class columns(models.Model):
    title = models.CharField(max_length=55)
    created_by = models.ForeignKey(user, related_name='columns', on_delete=CASCADE)
    board = models.ForeignKey(board, related_name='columns', on_delete=CASCADE)
    color = models.CharField(max_length=24, default='lite-gray')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = colmanager()
    # columns.cards

class card(models.Model):
    subject = models.CharField(max_length=65)
    content = models.TextField()
    created_by = models.ForeignKey(user, related_name='cards', on_delete=CASCADE)
    status = models.ForeignKey(columns, related_name='cards', on_delete=CASCADE)
    owners = models.ManyToManyField(user, related_name='working_on')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = cardmanager()
    # card.user
    # card.columns
    # card.owners
    # color = models.CharField(max_length=25)  deprecating to have status hold color only
