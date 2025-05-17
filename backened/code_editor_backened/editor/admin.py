from django.contrib import admin
from .models import ProgrammingLanguage, CodeSnippet, ExecutionResult


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'extension', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'version')


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'user', 'is_public', 'created_at', 'updated_at')
    list_filter = ('language', 'is_public', 'created_at')
    search_fields = ('title', 'code', 'user__username')
    date_hierarchy = 'created_at'


@admin.register(ExecutionResult)
class ExecutionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'user', 'status', 'execution_time', 'created_at')
    list_filter = ('status', 'language', 'created_at')
    search_fields = ('stdout', 'stderr', 'raw_code', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('execution_time', 'memory_used', 'execution_started_at', 'execution_completed_at')