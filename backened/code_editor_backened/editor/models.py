from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ProgrammingLanguage(models.Model):
    """Model for storing programming language information"""
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    
    # Command template for executing code (placeholders will be replaced)
    execution_command = models.CharField(max_length=255)
    
    # Compiler/interpreter path
    compiler_path = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.version})"


class CodeSnippet(models.Model):
    """Model for storing user code snippets"""
    title = models.CharField(max_length=100)
    code = models.TextField()
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ExecutionResult(models.Model):
    """Model for storing code execution results"""
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
        ('pending', 'Pending'),
    ]
    
    code_snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, null=True, blank=True)
    raw_code = models.TextField(null=True, blank=True)  # For non-saved executions
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow anonymous users
      # User input for interactive code execution
    user_input = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stdout = models.TextField(blank=True)  # Standard output
    stderr = models.TextField(blank=True)  # Standard error
    friendly_error = models.TextField(blank=True)  # Beginner-friendly error explanation
    execution_time = models.FloatField(default=0.0)  # Time taken to execute in seconds
    memory_used = models.IntegerField(default=0)  # Memory used in KB
    
    execution_started_at = models.DateTimeField(null=True, blank=True)
    execution_completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Execution {self.id} - {self.status}"
    
    def execution_duration(self):
        """Calculate execution duration in seconds"""
        if self.execution_started_at and self.execution_completed_at:
            return (self.execution_completed_at - self.execution_started_at).total_seconds()
        return None