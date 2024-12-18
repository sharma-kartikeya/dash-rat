from django.db import models
from django.contrib.auth.models import User

class AyodhyaUser(User):
    mobile = models.IntegerField(blank=False, null=False, name='mobile-number')
    
    
