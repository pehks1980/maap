from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

# urlpatterns = [
#     path('', mainapp.main, name='index'),
#     path('category/<int:pk>/', mainapp.products, name='category'),
# ]

urlpatterns = [
    path('', mainapp.main, name='index'),
    # path('category/<int:pk>/', mainapp.products, name='category'),
    # path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
    # path('product/', mainapp.products, name='product'),
]