from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USER_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')

class usermanager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['first_name'] = "User name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "User's last name should be at least 2 characters"
        if len(postData['username']) < 5:
            errors['username'] = "Username should be at least 5 characters"
        if not USER_REGEX.match(postData['username']):
            errors['username'] = "Username should not have specialized symbols or spaces"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        User = self.filter(email=postData['email'])
        if User:
            errors['email'] = "Email is already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long"
        if len(postData['password']) > 32:
            errors['password len'] = "Password should be less than 32 characters"
        if postData['password'] != postData['confpass']:
            errors['match'] = "Passwords should match each other"
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]

        return bcrypt.checkpw(password.encode(), user.password.encode())

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
    # user.status_columns
    # user.cards
    # user.working_on

class board(models.Model):
    title = models.CharField(max_length=55)
    created_by = models.ForeignKey(user, related_name='user_boards', on_delete=CASCADE)
    board_group = models.ManyToManyField(user, related_name='boards_imin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # board.created_by.username
    # board.status_columns
    # board.status-columns.cards

class status(models.Model):
    title = models.CharField(max_length=55)
    created_by = models.ForeignKey(user, related_name='status_columns', on_delete=CASCADE)
    for_board = models.ForeignKey(board, related_name='status_columns', on_delete=CASCADE)
    color = models.CharField(max_length=25, default='light-gray')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # status.cards

class card(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(user, related_name='cards', on_delete=CASCADE)
    status = models.ForeignKey(status, related_name='cards', on_delete=CASCADE)
    owners = models.ManyToManyField(user, related_name='working_on')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # card.user
    # card.status
    # card.owners
    # color = models.CharField(max_length=25)  deprecating to have status hold color only
