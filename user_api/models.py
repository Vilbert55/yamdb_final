from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    status = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    bio = models.TextField(max_length=500, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(max_length=9, choices=status, default=USER)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
