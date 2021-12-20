import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.core.files.storage import default_storage
from django.db import models
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False)

    def get_initials(self):
        if self.first_name and self.last_name:
            return (self.first_name[0] + self.last_name[0]).upper()
        else:
            return self.username[0].upper()

    def save(self, *args, **kwargs):

        if not self.avatar:
            initials = self.get_initials()
            avatar_name = f'{initials}_avatar_.jpg'
            file_path = f'{default_storage.location}\\avatars\\{avatar_name}'
            W, H = (60, 60)
            random_image = Image.new('RGB', (W, H), color=(73, 109, 137))
            random_image_text = ImageDraw.Draw(random_image)
            font = ImageFont.truetype("arial.ttf", 25)
            random_image_text.text((30, 30), initials, font=font, anchor="mm")
            random_image.save(file_path, quality=100)
            random_image.close()
            self.avatar.save(f'{avatar_name}', File(open(file_path, 'rb')), )
        super(CustomUser, self).save(*args, **kwargs)
