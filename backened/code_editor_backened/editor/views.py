from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeExecutionSerializer, FileUploadSerializer
from .services.code_executor import execute_code
import os

# Map numeric codes to language names.
LANGUAGE_MAPPING = {
    1: "python",
    2: "c",
    3: "cpp",
    4: "javascript",
    5: "html",
}

class CodeExecutionView(APIView):
    """
    POST /api/execute/
    Accepts code, a language_code, and optional user_input.
    Returns JSON with stdout, stderr, gui_output, and execution_time.
    Stateless endpoint.
    """
    permission_classes = []  # Public endpoint

    def post(self, request, *args, **kwargs):
        serializer = CodeExecutionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            language = LANGUAGE_MAPPING.get(data["language_code"])
            
            if not language:
                return Response(
                    {"error": "Unsupported language code provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            result = execute_code(language, data["code"], data.get("user_input", ""))
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(APIView):
    """
    POST /api/files/upload/
    Expects a file and saves it to a temporary location.
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]
            import tempfile
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            return Response({"file_path": temp_path}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDownloadView(APIView):
    """
    GET /api/files/download/?path=your_file_path
    Returns the file if it exists.
    """
    permission_classes = []

    def get(self, request, *args, **kwargs):
        from django.http import FileResponse, Http404
        file_path = request.query_params.get("path")
        if not file_path or not os.path.exists(file_path):
            raise Http404("File not found.")
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
