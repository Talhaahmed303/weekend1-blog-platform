from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
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
