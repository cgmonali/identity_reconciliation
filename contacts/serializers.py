from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone_number', 'email', 'linked_id', 'link_precedence']

class IdentifyRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phoneNumber = serializers.CharField(required=False, allow_null=True)
    id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        if not any([data.get('email'), data.get('phoneNumber'), data.get('id')]):
            raise serializers.ValidationError("At least one of email, phoneNumber, or id must be provided")
        return data

class IdentifyResponseSerializer(serializers.Serializer):
    primaryContatctId = serializers.IntegerField()
    emails = serializers.ListField(child=serializers.EmailField())
    phoneNumbers = serializers.ListField(child=serializers.CharField())
    secondaryContactIds = serializers.ListField(child=serializers.IntegerField())