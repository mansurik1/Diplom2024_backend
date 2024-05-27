from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from calendar_module.models import *
from .serialisers import DaysSheduleSerialiser
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


try:
    START_DATE = datetime.strptime(Param.objects.get(name='start_date').value, "%Y-%m-%d")
    START_WEEK_IS_NUMERATOR = bool(Param.objects.get(name='start_week_type').value)
    FIRST_LESSON_TIME = Param.objects.get(name='start_time').value

    # START_DATE = datetime.strptime('2024-02-07', '%Y-%m-%d')
    # START_WEEK_IS_NUMERATOR = True
    # FIRST_LESSON_TIME = '09-00'
    FIRST_LESSON_DURATION = 90
    SMALL_BREAK = 15
    BIG_BREAK = 30

except ObjectDoesNotExist:
    raise ValueError('Admin parameters have incorrect name!')


def count_week():
    today = datetime.now()
    today_week_day_num = today.weekday()

    # Определение номера недели учебы
    delta = today - START_DATE
    week_num = delta.days // 7 + 1

    is_numerator = START_WEEK_IS_NUMERATOR
    if week_num % 2 == 0:
        is_numerator = not is_numerator

    beg_day = (today - timedelta(days=today_week_day_num)).date()

    return {
        'weekNumber': week_num,  'dayNumber': today_week_day_num,
        'isNumerator': is_numerator, 'weekBeginDate': beg_day,
    }


class CalendarView(APIView):
    def get(self, request: Request, *args, **kwargs):

        try:
            user = TelegramUser.objects.get(chat_id=request.GET.get('chat_id'))
        except ObjectDoesNotExist:
            raise ValidationError({'detail': 'User not found.'})

        week_data = count_week()

        shedule = Lesson.objects.filter(group=user.group)
        response = {'shedule': DaysSheduleSerialiser(shedule, many=True).data,
                    'current_week': week_data,
                    'static': {
                        'group':  user.group.group_index,
                        'username': user.username,
                        'firstLessonIn': FIRST_LESSON_TIME,
                        'lessonDuration': FIRST_LESSON_DURATION,
                        'smallBreak': SMALL_BREAK,
                        'bigBreak': BIG_BREAK
                    }}
        return Response(response)
