import datetime

import django
from django import utils
from django.core.exceptions import ValidationError
from django.db import models


# Создаём класс Poll
class Poll(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    name = models.CharField(verbose_name='Название', max_length=50)  # Название
    date_start = models.DateField(verbose_name='Дата старта', default=django.utils.timezone.now)  # Дата старта
    date_end = models.DateField(verbose_name='Дата окончания', null=True, blank=True, default='')  # Дата окончания
    description = models.TextField(verbose_name='Описание', blank=True)  # Описание

    # Метод для отображения в админ панели
    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def is_active(self):
        return True if not self.date_end else self.date_end > datetime.date.today()

    def __init__(self, *args, **kwargs):
        super(Poll, self).__init__(*args, **kwargs)
        self.__original_date_start = self.date_start

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.date_end:
            if self.date_end <= self.date_start:
                errors['date_end'] = ValidationError('Дата окончания не может быть равна или меньше даты начала')
        if self.id:
            if self.date_start != self.__original_date_start:
                errors['date_start'] = ValidationError('Дата старта не может быть изменена')

        if errors:
            raise ValidationError(errors)


class Question(models.Model):
    TYPES = [
        ('TEXT', 'Text'),
        ('ONE', 'One'),
        ('MANY', 'Many'),
    ]
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    text = models.TextField(verbose_name='Вопрос', unique=False)  # Текст вопроса
    type = models.CharField(verbose_name='Тип ответа',
                            max_length=4,
                            choices=TYPES,
                            default='TEXT',
                            )  # Тип вопроса
    poll = models.ForeignKey(Poll, default='', on_delete=models.CASCADE, related_name='questions')  # Тип вопроса

    # Метод для отображения в админ панели
    def __str__(self):
        return self.text

    class Meta():
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def save(self, *args, **kwargs):
        print(self.__dict__)
        print(self.answers.all())
        super().save(*args, **kwargs)


class Answer_Variant(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    text = models.TextField(verbose_name='Ответ', unique=False)  # Текст варианта
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', to_field='id')  # Вопрос

    # Метод для отображения в админ панели
    def __str__(self):
        return self.text

    def clean(self):
        errors = {}
        if self.question.type == 'TEXT':
            errors['text'] = ValidationError('Для вопроса с типом TEXT не предполагается вариантов')
        # if self.question.type!='TEXT' and len(self.question.answers.all())==0:
        #         errors['text'] = ValidationError('Для вопроса с типом ONE или MANY нужно как минимум 2 варианта ответа')

        if errors:
            raise ValidationError(errors)

    class Meta():
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class Users(models.Model):
    id = models.AutoField(verbose_name='ID пользователя', primary_key=True, unique=True)  # Идентификатор

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Result(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    create_on = models.DateField(verbose_name='Дата создания', default=django.utils.timezone.now)  # Дата старта
    user = models.PositiveIntegerField(verbose_name='ID пользователя', null=False)
    user_id = models.ForeignKey(Users, null=True, blank=True, on_delete=models.CASCADE, related_name='results',
                                to_field='id')
    poll = models.ForeignKey(Poll, null=True, on_delete=models.CASCADE, related_name='results',
                             to_field='id')  # Тип вопроса

    def __str__(self):
        return str(self.id)

    # проверяем id пользователя на наличие в БД и добавляем в базу при отсутсвии
    def save(self, *args, **kwargs):
        if not bool(Users.objects.filter(id=self.user)) and not self.user_id:
            new_user = Users(id=self.user)
            Users.save(new_user)
            self.user_id = Users.objects.get(pk=self.user)
        super().save(*args, **kwargs)

    class Meta():
        verbose_name = 'Итог опроса'
        verbose_name_plural = 'Итоги опроса'


class Res_Answer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='res_answers',
                                 to_field='id')  # Вопрос
    answer = models.CharField(verbose_name='Ответ', max_length=200)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='res_answers', to_field='id')  # Результат

    def __str__(self):
        return self.answer_list()

    # def save(self, *args, **kwargs):
    #     if self.question.type == 'TEXT':
    #         print(self.question.type)
    #     super().save(*args, **kwargs)

    def answer_list(self):
        if self.question.type == 'TEXT':
            return str([self.answer])
        else:
            #return str([self.question.objects.get(pk=ans_id) for ans_id in self.answer.split(',')])
            return str([ans_id for ans_id in self.answer.split(',')])

    class Meta():
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Списки ответов'
