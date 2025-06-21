from django.db import models
from django.utils import timezone

class Contact(models.Model):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'

    LINK_PRECEDENCE_CHOICES = [
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
    ]

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linked_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    link_precedence = models.CharField(max_length=10, choices=LINK_PRECEDENCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f"{self.id} - {self.email} - {self.phone_number}"