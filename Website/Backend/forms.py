from django import forms
from django.forms import ModelForm, Textarea, TextInput,  SelectMultiple, FileInput, Form
from django.utils.translation import gettext_lazy as _

from .models import Post, Tag, Media

class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
                'tags': SelectMultiple(attrs={'class': 'select w-auto h-auto rounded-selector'}),
                'title': TextInput(attrs={'class': 'input rounded-selector w-auto'}),
                'description': Textarea(attrs={'class': 'textarea w-auto resize-none rounded-selector', }),
                'note': Textarea(attrs={'class': 'textarea w-auto resize-none rounded-selector'}),
        }

class TagModelForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
                'slug': TextInput(attrs={'class': 'input rounded-selector w-auto'}),
                'name': TextInput(attrs={'class': 'input rounded-selector w-auto'}),
        }

class MediaModelForm(ModelForm):
    class Meta:
        model = Media
        fields = '__all__'
        widgets = {
                'name': TextInput(attrs={'class': 'input rounded-selector w-auto'}),
                'file': FileInput(attrs={'class': 'input rounded-selector w-auto'}),
        }

class SendEmailForm(Form):
    template_name = "Backend/Parts/send_email.html"
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-auto input rounded-selector'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea w-auto resize-none rounded-selector'}))