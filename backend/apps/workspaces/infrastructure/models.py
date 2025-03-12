from django.db import models

class Workspace(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
