from django.contrib import admin
from .models import *

#
# # Supplies:
# class WorkInline(admin.StackedInline):
#     model = Work
#     extra = 0
#     readonly_fields = ['sum']
#
#     def got_sum(self, obj):
#         return obj.donation_set.aggregate(Sum('sum'))['sum__sum'] or 0
#
#
# class RestorationView(admin.ModelAdmin):
#     inlines = [WorkInline]
#     list_display = ['name', 'status', 'given_sum', 'total_sum']
#     readonly_fields = ['total_sum', 'given_sum']
#
#     def given_sum(self, obj):
#         return obj.work_set.aggregate(Sum('donation__sum'))['donation__sum__sum'] or 0
#
#     def total_sum(self, obj):
#         return obj.work_set.aggregate(Sum('sum'))['sum__sum'] or 0
#
#
# # Payments:
# class DonationInline(admin.TabularInline):
#     model = Donation
#     extra = 0
#     readonly_fields = ['restoration']
#     can_delete = False
#
#     def restoration(self, instance):
#         return instance.work.restore.name
#
#     def has_add_permission(self, *args):
#         return False
#
#     def has_change_permission(self, *args):
#         return False
#
#
# class PaymentView(admin.ModelAdmin):
#     inlines = [DonationInline]
#     list_display = ['user', 'status', 'code', 'sum', 'date_open', 'date_pay', 'date_close']
#     search_fields = ['user__username', 'status',  'date_open']
#     readonly_fields = ['code', 'sum', 'manager', 'date_open', 'date_close', 'user', 'date_pay']
#
#     def sum(self, obj):
#         return obj.donation_set.aggregate(Sum('sum'))['sum__sum'] or 0
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         obj.manager = request.user
#         obj.save()


from django.contrib import admin
from .models import Subject, Group, TelegramUser, Lesson, Param


class UserInline(admin.TabularInline):
    model = TelegramUser
    fields = ['username', 'first_name', 'chat_id']
    extra = 0
    can_delete = True


class GroupView(admin.ModelAdmin):
    inlines = [UserInline]
    list_display = ('group_index', 'year')
    search_fields = ('group_index', 'year')


class LessonView(admin.ModelAdmin):
    list_display = ('get_lesson', 'get_week_day', 'group', 'subject')
    list_filter = ('group__group_index', 'week_day_number', 'subject__name', 'type', 'for_numerator')
    search_fields = ('group__group_index', 'subject__name')

    def get_week_day(self, obj):
        week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return week_days[obj.week_day_number]
    get_week_day.short_description = 'День недели'

    def get_lesson(self, obj):
        return obj.lesson_number
    get_lesson.short_description = 'Пара'


admin.site.register(Subject)
admin.site.register(Group, GroupView)
admin.site.register(Lesson, LessonView)
admin.site.register(Param)