from django.db import models
import uuid

class UniversityType(models.TextChoices):
    PRIVATE = 'private'
    PUBLIC = 'public'

class University(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512, blank=False, null=False)
    type = models.CharField(max_length=255, choices=UniversityType.choices, blank=False, null=False, default=UniversityType.PRIVATE)
    location = models.CharField(max_length=255, blank=False, null=False)
    location_details = models.TextField(blank=True, null=True)
    usp = models.TextField(blank=True, null=True)
    

