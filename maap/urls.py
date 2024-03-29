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


from django.urls import path, re_path
from django.contrib import admin

import mainapp.views as mainapp

# urlpatterns = [
#     path('', mainapp.main),
#     path('products/', mainapp.products),
#     path('contact/', mainapp.contact),
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import include, url, re_path

urlpatterns = [
    path('', mainapp.main, name='index'),
    path('', mainapp.main, name='main'),
    #path('mathem/<int:pk>/', mainapp.mathem, name='mathem'),#lesson_id
    #ajax ver of mathem
    path('mathemj/<int:pk>/', mainapp.mathemj, name='mathemj'),
    path('clockj/', mainapp.clockj, name='clockj'),
    path('clockj/<int:ans_correct>/<int:ans_amount>/', mainapp.clockj, name='clockj'),

    #path('mathemk/<int:pk1>/<int:pk2>/<int:diff>/', mainapp.mathemk, name='mathemk'),
    path('finish/<int:pk>/', mainapp.finish, name='finish'),
    path('clear-hist/', mainapp.clear_hist, name='clear_hist'),
    path('clear-hist-5/', mainapp.clear_hist_5, name='clear_hist_5'),
    re_path(r'hist/page/(?P<page>\d+)/', mainapp.hist, name='hist'),
    re_path(r'hist/', mainapp.hist, name='hist'),
    path('mathemj/ajax/',mainapp.mathem_ajax),
    path('clockj/ajax/',mainapp.clock_ajax),
    path('clockj/ajax1/',mainapp.clock_ajax1),

    path('checkcron/', mainapp.checkCron, name='checkcron'),
    # kube feature
    path('__heartbeat__', mainapp.checkHeartBeat, name='checkheartbeat'),

    re_path(r'^uncheck/(?P<email>.+)/(?P<id>.+)/$', mainapp.uncheckEmail, name='uncheck'),

    path('auth/', include('authapp.urls', namespace='auth')),
    url(r'^files/', include('db_file_storage.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)