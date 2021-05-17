# backend/notes/urls.py
from rest_framework import routers

from .views import PollViewSet, QuestionViewSet, AnswerViewSet, ResultViewSet, UserPollsViewSet, ActiveViewSet

# Создаем router и регистрируем наш ViewSet
router = routers.DefaultRouter()
router.register(r'polls', ActiveViewSet, basename='active')
router.register(r'admin', PollViewSet, basename='all')
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'results', ResultViewSet)
router.register(r'userpolls', UserPollsViewSet, basename='user_polls')


# URLs настраиваются автоматически роутером
urlpatterns = router.urls