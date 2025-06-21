from rest_framework import serializers
from .models import Contact

# Serializer for the Contact model
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone_number', 'email', 'linked_id', 'link_precedence']

# Serializer for handling identify request payloads
class IdentifyRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phoneNumber = serializers.CharField(required=False, allow_null=True)
    id = serializers.IntegerField(required=False, allow_null=True)

    # Ensure at least one field is provided in the request
    def validate(self, data):
        if not any([data.get('email'), data.get('phoneNumber'), data.get('id')]):
            raise serializers.ValidationError("At least one of email, phoneNumber, or id must be provided")
        return data

# Serializer for formatting the identify response
class IdentifyResponseSerializer(serializers.Serializer):
    primaryContatctId = serializers.IntegerField()  # ID of the primary contact
    emails = serializers.ListField(child=serializers.EmailField())  # List of associated emails
    phoneNumbers = serializers.ListField(child=serializers.CharField())  # List of associated phone numbers
    secondaryContactIds = serializers.ListField(child=serializers.IntegerField())  # IDs of secondary contacts