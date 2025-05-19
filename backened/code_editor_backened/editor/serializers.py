from rest_framework import serializers

class CodeExecutionSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        help_text="The source code to execute."
    )
    language_code = serializers.IntegerField(
        required=True,
        help_text="Language code (1: Python, 2: C, 3: C++, 4: JavaScript, 5: HTML)"
    )
    user_input = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Optional input for interactive programs."
    )

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

