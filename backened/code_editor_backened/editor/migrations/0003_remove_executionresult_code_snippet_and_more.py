# Generated by Django 4.2.21 on 2025-05-17 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0002_executionresult_user_input'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='executionresult',
            name='code_snippet',
        ),
        migrations.RemoveField(
            model_name='executionresult',
            name='language',
        ),
        migrations.RemoveField(
            model_name='executionresult',
            name='user',
        ),
        migrations.DeleteModel(
            name='CodeSnippet',
        ),
        migrations.DeleteModel(
            name='ExecutionResult',
        ),
        migrations.DeleteModel(
            name='ProgrammingLanguage',
        ),
    ]
