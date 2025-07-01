from django.db import models


class Tag(models.Model):
    slug = models.SlugField(max_length=100, blank=False, null=True)
    name = models.CharField(max_length=100, blank=False, default='LABEL', null=True)

    def __str__(self):
        return self.name.__str__()

class Post(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=200, blank=False, default='TITLE', null=True)
    description = models.TextField(max_length=500, blank=False, default='DESCRIPTION')
    timeCreated = models.DateTimeField(auto_created=True, auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)
    note = models.TextField(max_length=300, blank=False, default='NOTE')

class Media(models.Model):
    name = models.CharField(max_length=100, blank=False, default='LABEL', null=True)
    file = models.FileField(upload_to="")