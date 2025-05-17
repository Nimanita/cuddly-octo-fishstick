from rest_framework import serializers
from .models import ProgrammingLanguage, CodeSnippet, ExecutionResult
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'email']


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    """Serializer for the ProgrammingLanguage model"""
    class Meta:
        model = ProgrammingLanguage
        fields = ['id', 'name', 'extension', 'version', 'is_active']
        read_only_fields = ['id']


class CodeSnippetSerializer(serializers.ModelSerializer):
    """Serializer for the CodeSnippet model"""
    language_name = serializers.ReadOnlyField(source='language.name')
    user_username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = CodeSnippet
        fields = [
            'id', 'title', 'code', 'language', 'language_name', 
            'user', 'user_username', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_username', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Set the user from the request context"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExecutionResultSerializer(serializers.ModelSerializer):
    """Serializer for the ExecutionResult model"""
    language_name = serializers.ReadOnlyField(source='language.name')
    execution_duration = serializers.ReadOnlyField()
    
    class Meta:
        model = ExecutionResult
        fields = [
            'id', 'code_snippet', 'raw_code', 'language', 'language_name', 
            'user', 'status', 'stdout', 'stderr', 'friendly_error',
            'execution_time', 'memory_used', 'execution_started_at',
            'execution_completed_at', 'created_at', 'execution_duration','user_input'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'stdout', 'stderr', 'friendly_error',
            'execution_time', 'memory_used', 'execution_started_at',
            'execution_completed_at', 'created_at', 'execution_duration'
        ]


class CodeExecutionSerializer(serializers.Serializer):
    """Serializer for code execution requests"""
    code = serializers.CharField(required=True)
    language_id = serializers.IntegerField(required=True)
    save_snippet = serializers.BooleanField(default=False)
    snippet_title = serializers.CharField(required=False, allow_blank=True)
     # Add user input field
    user_input = serializers.CharField(required=False, allow_blank=True, 
                                      help_text="Input data to provide to the program during execution")
 
    def validate_language_id(self, value):
        """Validate that the language exists and is active"""
        try:
            language = ProgrammingLanguage.objects.get(id=value, is_active=True)
            return value
        except ProgrammingLanguage.DoesNotExist:
            raise serializers.ValidationError("Selected programming language is not available.")