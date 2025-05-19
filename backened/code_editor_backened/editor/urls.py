
# urls.py
from django.urls import path
from .views import CodeExecutionView, FileUploadView, FileDownloadView

urlpatterns = [
    path('execute/', CodeExecutionView.as_view(), name='code_execute'),
    path('files/upload/', FileUploadView.as_view(), name='file_upload'),
    path('files/download/', FileDownloadView.as_view(), name='file_download'),
]
