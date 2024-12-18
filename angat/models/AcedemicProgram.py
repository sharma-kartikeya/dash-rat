from django.db import models
import uuid
from .University import University
from django.core.exceptions import ValidationError
from typing import Optional

cost_schema = {
    "futurense_pricing": Optional[str],
    "original_pricing": Optional[str],
}

credits_schema = {
    'total_credits': Optional[str],
    'iit_or_iim': Optional[str],
    'credit_in_iit_iim': Optional[str],
    'credit_in_us': Optional[str],
    'total_duration': Optional[str]
}

eligibility_schema = {
    'ug_bacground': Optional[str],
    'min_gpa_perc': Optional[str],
    'max_backlogs': Optional[str],
    'work_exp': Optional[str],
    'three_year_undergrad': Optional[str],
    'decision_factor': Optional[str]
}

application_requirements_schema = {
    'transcription_evaluation': Optional[str],
    'lor': Optional[str],
    'sop': Optional[str],
    'interviews': Optional[str],
    'deposit': Optional[str],
    'deposit_refundabe': Optional[str]
}

placement_details_schema = {
    'co-op': Optional[str],
    'key_companies': Optional[str],
    'key_job_roles': Optional[str]
}

def JSON_Validator(schema: dict[str], object) -> None:
    # Validate schema
        for key, expected_type in schema.items():
            if key not in object:
                raise ValidationError(f"{key} is required in object.")
            
            if isinstance(expected_type, dict):  # Check nested structure
                JSON_Validator(expected_type, object[key])
            else:
                if not isinstance(object[key], expected_type):
                    raise ValidationError(f"{key} must be of type {expected_type.__name__}.")

class AcedemicProgram(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranking = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(blank=False, null=False, max_length=512)
    university = models.ForeignKey(to=University, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=512)
    # type = models.CharField(blank=False, null=False, max_length=100)
    usp = models.TextField(blank=True, null=True)
    specialization = models.TextField(blank=True, null=True)
    intern_or_co_op = models.CharField(null=True, blank=True, max_length=100)
    curriculum_link = models.URLField(max_length=512, null=True, blank=True)
    cost = models.JSONField()
    credits = models.JSONField()
    eligibility = models.JSONField()
    application_requirements = models.JSONField()
    placement_details = models.JSONField()
    study_type = models.CharField(max_length=255, null=False, blank=False)

    def clean(self):
        super().clean()
        JSON_Validator(cost_schema, self.cost)
        JSON_Validator(credits_schema, self.credits)
        JSON_Validator(application_requirements_schema, self.application_requirements)
        JSON_Validator(placement_details_schema, self.placement_details)