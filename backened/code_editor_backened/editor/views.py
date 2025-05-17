from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProgrammingLanguage, CodeSnippet, ExecutionResult
from .serializers import (
    ProgrammingLanguageSerializer, 
    CodeSnippetSerializer, 
    ExecutionResultSerializer,
    CodeExecutionSerializer
)
from .services.code_executor import execute_code
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


class ProgrammingLanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving programming languages"""
    queryset = ProgrammingLanguage.objects.filter(is_active=True)
    serializer_class = ProgrammingLanguageSerializer
    permission_classes = [AllowAny]


class CodeSnippetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing code snippets"""
    serializer_class = CodeSnippetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return snippets for the current user or public snippets"""
        user = self.request.user
        if user.is_authenticated:
            # Return user's snippets and public snippets
            return CodeSnippet.objects.filter(
                user=user
            ).select_related('language', 'user').order_by('-updated_at')
        # No snippets for unauthenticated users
        return CodeSnippet.objects.none()
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        """Return public snippets"""
        public_snippets = CodeSnippet.objects.filter(
            is_public=True
        ).select_related('language', 'user').order_by('-updated_at')
        
        page = self.paginate_queryset(public_snippets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(public_snippets, many=True)
        return Response(serializer.data)


class ExecutionResultViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving execution results"""
    serializer_class = ExecutionResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return execution results for the current user"""
        user = self.request.user
        if user.is_authenticated:
            return ExecutionResult.objects.filter(
                user=user
            ).select_related('language', 'code_snippet').order_by('-created_at')
        return ExecutionResult.objects.none()


class CodeExecutionView(viewsets.ViewSet):
    """ViewSet for executing code"""
    permission_classes = [AllowAny]  # Allow anonymous code execution
    
    @action(detail=False, methods=['post'])
    def execute(self, request):
        """Execute code and return results"""
        serializer = CodeExecutionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        code = serializer.validated_data['code']
        language_id = serializer.validated_data['language_id']
        save_snippet = serializer.validated_data['save_snippet']
        snippet_title = serializer.validated_data.get('snippet_title', '')
        user_input = serializer.validated_data.get('user_input', '')
        language = get_object_or_404(ProgrammingLanguage, id=language_id, is_active=True)
        
        # Save snippet if requested and user is authenticated
        code_snippet = None
        if save_snippet and request.user.is_authenticated and snippet_title:
            code_snippet = CodeSnippet.objects.create(
                title=snippet_title,
                code=code,
                language=language,
                user=request.user
            )
        
        # Create execution record
        execution = ExecutionResult.objects.create(
            code_snippet=code_snippet,
            raw_code=None if code_snippet else code,
            language=language,
            user=request.user if request.user.is_authenticated else None,
            user_input=user_input,
            status='pending'
        )
        
        # Execute the code
        result = execute_code(execution)
        
        # Return the serialized execution result
        result_serializer = ExecutionResultSerializer(result)
        return Response(result_serializer.data)