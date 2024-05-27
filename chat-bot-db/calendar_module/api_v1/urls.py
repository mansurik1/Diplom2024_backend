from django.urls import path, include
from .views import CalendarView


urlpatterns = [
    path('full_schedule/', CalendarView.as_view()),
]
