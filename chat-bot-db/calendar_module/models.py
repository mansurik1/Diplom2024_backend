from django.db import models
from django.contrib.auth.models import User

day_name = {
    0: 'ПН',
    1: 'ВТ',
    2: 'СР',
    3: 'ЧТ',
    4: 'ПТ',
    5: 'СБ',
    6: 'ВС',
}

lesson_type = {
    0: 'Лекция',
    1: 'Лабораторная работа',
    2: 'Семинар',
}


class Subject(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        managed = True
        db_table = "Subjects"
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Group(models.Model):
    has_finished = models.BooleanField(default=False)
    year = models.DateField()
    group_index = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = "Groups"
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.group_index


class TelegramUser(User):
    chat_id = models.CharField(primary_key=True, max_length=10)
    group = models.ForeignKey(Group, models.CASCADE)

    class Meta:
        managed = True
        db_table = "Students"
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.username


class Lesson(models.Model):
    lesson_number = models.SmallIntegerField(choices=[
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ], default=1)
    for_numerator = models.BooleanField(choices=[
        (False, 'Знаменатель'),
        (True, 'Числитель')
    ], default=False)
    week_day_number = models.SmallIntegerField(
        choices=[(key, val) for key, val in day_name.items()], default=1
    )
    group = models.ForeignKey(Group, models.CASCADE)
    subject = models.ForeignKey(Subject, models.CASCADE)
    type = models.IntegerField(choices=[(key, val) for key, val in lesson_type.items()], default=1)

    class Meta:
        managed = True
        db_table = "Lessons"
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.subject.name


class Param(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "Params"
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"