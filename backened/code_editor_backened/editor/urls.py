
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'languages', views.ProgrammingLanguageViewSet, basename='language')
router.register(r'snippets', views.CodeSnippetViewSet, basename='snippet')
router.register(r'executions', views.ExecutionResultViewSet, basename='execution')
router.register(r'execute', views.CodeExecutionView, basename='execute')

urlpatterns = [
    path('', include(router.urls)),
]