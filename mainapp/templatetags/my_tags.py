from django import template
from django.conf import settings

#лямбда функции для обработки переменных через pipe var | func => result = lambda func(var)
register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    фильтр шаблона извлекает значение ключа словаря
    """

    return dictionary.get(key)

#replaces /media/{{product.image|default:'products_images/default.jpg'}}
@register.filter(name='media_folder_products')
def media_folder_products(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


#replaces /media/{{ object.avatar|default:'users_avatars/default.jpg'
@register.filter(name='media_users_avatars')
def media_users_avatars(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам user
    users_avatars/product1.jpg --> /media/users_avatars/product1.jpg
    """
    if not string:
        string = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'