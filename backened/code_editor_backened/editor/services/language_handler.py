"""
Helper module for managing programming languages and their specific requirements
"""
from ..models import ProgrammingLanguage


def get_language_info(language_id):
    """
    Get information about a programming language
    
    Args:
        language_id (int): ID of the programming language
    
    Returns:
        ProgrammingLanguage: The programming language object
    """
    try:
        return ProgrammingLanguage.objects.get(id=language_id, is_active=True)
    except ProgrammingLanguage.DoesNotExist:
        return None


def get_all_languages():
    """
    Get all active programming languages
    
    Returns:
        QuerySet: All active programming languages
    """
    return ProgrammingLanguage.objects.filter(is_active=True)


def check_language_support():
    """
    Check if the required programming languages are installed on the system
    
    Returns:
        dict: Dictionary with language names as keys and bool values indicating if they're available
    """
    import subprocess
    import shutil
    
    support = {}
    
    # Check Python
    python_path = shutil.which('python3') or shutil.which('python')
    support['python'] = python_path is not None
    
    # Check C
    gcc_path = shutil.which('gcc')
    support['c'] = gcc_path is not None
    
    # Check C++
    gpp_path = shutil.which('g++')
    support['cpp'] = gpp_path is not None
    
    return support


def initialize_languages():
    """
    Initialize the default programming languages in the database
    """
    languages = [
        {
            'name': 'Python',
            'extension': 'py',
            'version': '3.x',
            'execution_command': 'python3 {filename}',
            'compiler_path': '/usr/bin/python3',
        },
        {
            'name': 'C',
            'extension': 'c',
            'version': 'C11',
            'execution_command': 'gcc {filename} -o {output} && {output}',
            'compiler_path': '/usr/bin/gcc',
        },
        {
            'name': 'C++',
            'extension': 'cpp',
            'version': 'C++14',
            'execution_command': 'g++ {filename} -o {output} && {output}',
            'compiler_path': '/usr/bin/g++',
        },
    ]
    
    for lang_data in languages:
        ProgrammingLanguage.objects.get_or_create(
            name=lang_data['name'],
            defaults={
                'extension': lang_data['extension'],
                'version': lang_data['version'],
                'execution_command': lang_data['execution_command'],
                'compiler_path': lang_data['compiler_path'],
                'is_active': True,
            }
        )