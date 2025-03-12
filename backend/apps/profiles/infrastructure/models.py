from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
