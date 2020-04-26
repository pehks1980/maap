"""maap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.urls import path
from django.contrib import admin

import mainapp.views as mainapp

# urlpatterns = [
#     path('', mainapp.main),
#     path('products/', mainapp.products),
#     path('contact/', mainapp.contact),
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import include

urlpatterns = [
    path('', mainapp.main, name='index'),
    path('', mainapp.main, name='main'),
    path('mathem/<int:pk>/', mainapp.mathem, name='mathem'),#lesson_id
    #path('mathem/<int:pk>/<int:a1>/<int:b1>/<int:c1>', mainapp.mathem, name='mathem'),
    path('mathemk/<int:pk1>/<int:pk2>/<int:diff>/', mainapp.mathemk, name='mathemk'),
    path('finish/<int:pk>/', mainapp.finish, name='finish'),
    path('hist/', mainapp.hist, name='hist'),
    path('clear-hist/', mainapp.clear_hist, name='clear_hist'),

    path('auth/', include('authapp.urls', namespace='auth')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)