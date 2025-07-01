from django.contrib import admin

from .models import Post, Tag, Media

# Register your models here.

admin.site.register(Post, admin.ModelAdmin)
admin.site.register(Tag, admin.ModelAdmin)
admin.site.register(Media, admin.ModelAdmin)