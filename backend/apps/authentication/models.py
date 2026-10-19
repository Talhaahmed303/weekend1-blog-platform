from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.db import models

@deconstructible
class SafeUsernameValidator(RegexValidator):
    regex = r'^[\w.@+\- ]+$'
    message = (
        'Enter a valid username. This value may contain only letters, numbers, spaces, and @/./+/-/_ characters.'
    )
    flags = 0

class User(AbstractUser):
    username_validator = SafeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits, spaces and @/./+/-/_ only.',
        validators=[SafeUsernameValidator()],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='author')
    bio = models.TextField(blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_blog_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff
