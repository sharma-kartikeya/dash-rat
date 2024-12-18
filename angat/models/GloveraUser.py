from django.db import models
# from .AcedemicProgram import AcedemicProgram
import uuid

class GloveraUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, null=False, max_length=255)
    email = models.EmailField(blank=False, null=False, max_length=255)
    mobile = models.IntegerField(blank=False, null=False)
    # intake = models.CharField(blank=True, null=True, max_length=255)
    # naac_grade = models.FloatField(blank=True, null=True, max_length=255)
    percentage = models.CharField(blank=True, null=True)
    backlogs = models.CharField(blank=False, null=False, default=0, max_length=255)
    work_exp = models.CharField(blank=False, null=False, default=0, max_length=255)
    bachlors = models.CharField(blank=True, null=True)
    bachlors_program = models.CharField(blank=True, null=True)
    univ = models.CharField(blank=True, null=True)
    # eligible_programs = models.ForeignKey(to=AcedemicProgram, on_delete=models.CASCADE, blank=True, null=True)