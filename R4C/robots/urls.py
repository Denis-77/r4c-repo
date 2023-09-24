from django.urls import path
from .views import RobotView

urlpatterns = [
    path('json/', RobotView.as_view(), name='robot_json'),
]