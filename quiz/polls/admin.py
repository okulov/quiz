from django.contrib import admin

from .models import Poll, Question, Answer_Variant, Result, Res_Answer, Users


class QuestionsInline(admin.StackedInline):
    model = Question
    extra = 1


class AnswersInline(admin.TabularInline):
    model = Answer_Variant
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline, ]
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInline, ]
    list_display = ('id', 'text', 'poll')
    list_display_links = ('id', 'text')


class Res_AnswerInline(admin.StackedInline):
    model = Res_Answer


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    inlines = [Res_AnswerInline, ]
    list_display = ('id', 'user_id', 'poll', 'create_on')
    list_display_links = ('id',)


@admin.register(Res_Answer)
class Res_AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'answer_list','result')
    list_display_links = ('id', 'question', 'answer', 'result')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)


@admin.register(Answer_Variant)
class Answer_VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question')
    list_display_links = ('id',)
