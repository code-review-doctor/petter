from django.contrib import admin

# Register your models here.
from deals.models import Comment
from deals.models import Deal

admin.site.register(Deal)
admin.site.register(Comment)
