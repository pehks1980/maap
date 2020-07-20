from django.core.management.base import BaseCommand
from mainapp.models import MaapLesson, MaapReport, Report
from django.contrib.auth.models import User



import json, os

JSON_PATH = ''

import json, os

JSON_PATH = ''

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)

class Command(BaseCommand):
    def handle(self, *args, **options):
        lessons = load_from_json('db_lesson')
        #reload MaapLesson table from json
        MaapLesson.objects.all().delete()
        for lesson in lessons:
            #delete model key
            del lesson['model']
            #copy and delete idx keys
            fields_idx = { 'user_id' : lesson['fields']['user'],
                           'report_id' : lesson['fields']['report'] }

            del lesson['fields']['user'], lesson['fields']['report']
            #create item with fields values
            new_lesson = MaapLesson(**lesson['fields'])
            #set keys to appropriate tables accordingly
            new_lesson.report_id = fields_idx['report_id']
            new_lesson.user_id = fields_idx['user_id']
            #save item
            new_lesson.save()

        print('reloading of lessons is done.')
        # reports = load_from_json('db_report')
        #
        # MaapReport.objects.all().delete()
        # for report in reports:
        #     category_name = report["category"]
        #     # Получаем категорию по имени
        #     _category = ProductCategory.objects.get(name=category_name)
        #     # Заменяем название категории объектом
        #     product['category'] = _category

            # new_report = report(**product)
            # new_report.save()

#         # Создаем суперпользователя при помощи менеджера модели
#         super_user = User.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains')
#
#
# from authapp.models import ShopUser
#
# super_user = ShopUser.objects.create_superuser('root1', 'django@geekshop.local', '123', age=33)