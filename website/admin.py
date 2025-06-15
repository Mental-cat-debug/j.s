from django.contrib import admin # type: ignore
from .models import NewsPost, Comment

admin.site.register(NewsPost)
admin.site.register(Comment)
