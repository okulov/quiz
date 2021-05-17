from rest_framework import serializers
from .models import Poll, Question, Answer_Variant, Result, Users


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'name', 'description', 'date_start', 'date_end', 'questions')
        depth = 1


class ActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'name', 'description', 'date_end', 'questions')
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'poll', 'answers')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer_Variant
        fields = ('id', 'text', 'question')


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'create_on', 'user', 'poll', 'res_answers')
        depth = 1


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id',)
