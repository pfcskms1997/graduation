"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# settings.py를 개발용이랑 배포용이랑 다르게 바꾸었기 때문에 mysite.settings.product로 경로를 지정해준다.
# 개발용 settings.py는 manage.py 경로를 설정한다. 배포용은 wsgi.py에서 설정한다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.product')

application = get_wsgi_application()
