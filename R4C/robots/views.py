import datetime
import os

from openpyxl import Workbook

from django.http import HttpResponse
from django.utils.encoding import escape_uri_path

from .models import Robot


def download_excel(request):
    week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    robots = Robot.objects.exclude(created__lt=week_ago)
    robots_dict = {}
    for robot in robots:
        robots_dict.setdefault(robot.model, {})
        robots_dict[robot.model].setdefault(robot.version, 0)
        robots_dict[robot.model][robot.version] += 1

    workbook = Workbook()
    first_list = True
    for model in robots_dict:
        if first_list:
            sheet = workbook.active
            sheet.title = model
            first_list = False
        else:
            sheet = workbook.create_sheet(model)

        sheet['A1'] = 'Модель'
        sheet['B1'] = 'Версия'
        sheet['C1'] = 'Количество за неделю'
        for num, version in enumerate(robots_dict[model]):
            sheet[f'A{num + 2}'] = model
            sheet[f'B{num + 2}'] = version
            sheet[f'C{num + 2}'] = robots_dict[model][version]
    workbook.save('robots.xlsx')

    with open('robots.xlsx', 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{escape_uri_path("robots.xlsx")}"'
    os.remove('robots.xlsx')
    return response
