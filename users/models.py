from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.URLField()

    def get_initials(self):
        if self.first_name and self.last_name:
            return (self.first_name[0] + self.last_name[0]).upper()
        else:
            return self.username[0].upper()
