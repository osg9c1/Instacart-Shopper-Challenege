from django.db import models
from datetime import datetime

class Applicants(models.Model):
    WORKFLOW_STATUS_CHOICES = ((1, 'applied'), (2, 'quiz_started'), (3, 'quiz_completed'), (4, 'onboarding_requested'),
                               (5, 'onboarding_completed'), (6, 'hired'), (7, 'rejected'))
    WORKFLOW_STATUS_DICT = {'applied': 1, 'quiz_started': 2, 'quiz_completed': 3, 'onboarding_requested': 4,
                            'onboarding_completed': 5, 'hired': 6, 'rejected': 7}
    id = models.IntegerField(primary_key=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    region = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    email = models.TextField(blank=True)
    phone_type = models.TextField(blank=True)
    source = models.TextField(blank=True)
    over_21 = models.NullBooleanField(null=True, blank=True)
    reason = models.TextField(blank=True)
    workflow_state = models.TextField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = u'applicants'

