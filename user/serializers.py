from django.contrib.auth import get_user_model, password_validation

class UserWriteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "email",
            "password",
            "is_verified",
        ]
        read_only_fields = [
            "is_verified",
        ]