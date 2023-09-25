import json

from django.shortcuts import render, redirect
from django.views import View

from .forms import NewRobotForm
from .models import Robot


class RobotView(View):
    def get(self, request):
        form = NewRobotForm()
        context = {
            'form': form
        }
        return render(request, 'robots/robot_form.html', context)

    def post(self, request):
        form = NewRobotForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('json_string')
            robot_dict = json.loads(data)
            Robot.objects.create(
                serial='-'.join([robot_dict['model'], robot_dict['version']]),
                model=robot_dict['model'],
                version=robot_dict['version'],
                created=form.date_object,
            )
            return redirect('/robots/json/')
        context = {
            'form': form
        }
        return render(request, 'robots/robot_form.html', context)
