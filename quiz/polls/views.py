# Create your views here.
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
import datetime

import django
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Poll, Result, Users
from .models import Question, Answer_Variant
from .serializers import PollSerializer, ResultsSerializer, ActiveSerializer
from .serializers import QuestionSerializer, AnswerSerializer


# @api_view(['GET'])
# def api_poll(request):
#     if request.method == 'GET':
#         polls = Poll.objects.all()
#         serializer = PollSerializer(polls, many=True)
#         return Response(serializer.data)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-date_start')
    serializer_class = PollSerializer


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-poll')
    serializer_class = QuestionSerializer


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer_Variant.objects.all().order_by('-question')
    serializer_class = AnswerSerializer


class ActiveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Poll.objects.filter(date_start__gte=datetime.date.today())
    serializer_class = ActiveSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().order_by('-id')
    serializer_class = ResultsSerializer


class UserPollsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = Result.objects.filter(user_id=pk)
        serializer = ResultsSerializer(queryset, many=True)
        return Response(serializer.data)
