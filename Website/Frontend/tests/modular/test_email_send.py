from django.test import LiveServerTestCase, RequestFactory

from rest_framework.request import Request

from Frontend.views import EmailTestView


class EmailSendTest(LiveServerTestCase):
    ''' Отправка почты '''

    def test_email_send(self):
        ''' Тестируем отправку почты '''
        # Отправка правильной формы
        response = self.client.post(
            f"{self.live_server_url}/en/test-mail/", 
            data={
                'email': 'chedrden@gmail.com',
                'message': "Some message"
            })
        self.assertEqual(response.context.get('status'), 'success')
        # Отправка не правильной формы
        response = self.client.post(
            f"{self.live_server_url}/en/test-mail/", 
            data={
                'email': 'che.com',
                'message': "Some message"
            })
        self.assertEqual(response.context.get('status'), 'error')