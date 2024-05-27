from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField, BooleanField,
                                        IntegerField)
from calendar_module.models import Lesson


class DaysSheduleSerialiser(ModelSerializer):
    number = IntegerField(source='lesson_number')
    day = IntegerField(source='week_day_number')
    isNumer = BooleanField(source='for_numerator')
    subject = SerializerMethodField()

    class Meta:
        model = Lesson
        many = True
        fields = ['number', 'day', 'isNumer', 'type', 'subject']

    def get_subject(self, obj):
        return obj.subject.name
