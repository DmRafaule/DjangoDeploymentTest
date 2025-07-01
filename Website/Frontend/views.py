import json

from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.core.mail import send_mail
from django.template import loader
from django.test import RequestFactory

from Backend.views import PostListView
from Backend.serializers import PostSerializer
from Backend.models import Post, Tag
from Backend.forms import SendEmailForm
from Website.settings import DEFAULT_FROM_EMAIL

class HomeView(TemplateView):

    template_name = 'domashnyaya.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

class EmailTestView(TemplateView):
    template_name = 'test-mail.html'

    def get_context_data(self, **kwargs):
        context = super(EmailTestView, self).get_context_data(**kwargs)
        context.update({'send_email_form': SendEmailForm()})
        return context
    
    def post(self, request, *args, **kwargs):
        ''' Check the e-mail sending feature '''
        context = self.get_context_data(**kwargs)
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = _('Это сообщение было отправленно с тестового сайта по деплою')
            message = f'{form.cleaned_data.get("message")}'
            email = form.cleaned_data.get("email")
            recipients = []
            recipients.append(email)
            send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=recipients)
            context.update({'send_email_form': SendEmailForm()})
            context.update({'status': 'success'})
            context.update({'message': _("Успешно отправил письмо")})
            return render(request, SendEmailForm.template_name, context=context)
        else:
            context.update({'send_email_form': form})
            context.update({'status': 'error'})
            context.update({'message': _("Не смог отправить письмо")})
            return render(request, SendEmailForm.template_name, context=context)

class DatabaseTestView(TemplateView):
    template_name = 'test-database.html'

    def get_context_data(self, **kwargs):
        context = super(DatabaseTestView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        ''' Check the e-mail sending feature '''
        context = super(DatabaseTestView, self).get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

class MediaTestView(TemplateView):
    template_name = 'test-media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaTestView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        ''' Check the e-mail sending feature '''
        context = super(MediaTestView, self).get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

class StaticTestView(TemplateView):
    template_name = 'test-static.html'

    def get_context_data(self, **kwargs):
        context = super(StaticTestView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        ''' Check the e-mail sending feature '''
        context = super(StaticTestView, self).get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

class TestingTestView(TemplateView):
    template_name = 'test-testing.html'

    def get_context_data(self, **kwargs):
        context = super(TestingTestView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        ''' Check the e-mail sending feature '''
        context = super(TestingTestView, self).get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

class TranslationTestView(TemplateView):
    template_name = 'test-translation.html'

    def get_context_data(self, **kwargs):
        context = super(TranslationTestView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        ''' Check the e-mail sending feature '''
        context = super(TranslationTestView, self).get_context_data(**kwargs)
        context.update({'status': 'success'})
        context.update({'message': _("Успешно отправил письмо")})
        return render(request, self.template_name, context=context)

def get_server_strings(request):
    context = {}
    context.update({'status': 'success'})
    context.update({'message': _("Это сообщение с сервера")})
    return render(request, 'Backend/Parts/toast-message.html', context=context)