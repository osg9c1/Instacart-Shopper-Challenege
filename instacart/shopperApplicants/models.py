from django.db import models
from django.utils.translation import gettext as _


class ShopperApplicants(models.Model):
    APPLIED = 1
    WORKFLOW_STATUS_CHOICES = ((1, 'applied'), (2, 'quiz_started'), (3, 'quiz_completed'), (4, 'onboarding_requested'),
                               (5, 'onboarding_completed'), (6, 'hired'), (7, 'rejected'))
    WORKFLOW_STATUS_CHOICES_DICT = dict(WORKFLOW_STATUS_CHOICES)
    id = models.IntegerField(primary_key=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    zipcode = models.IntegerField(blank=True)
    phone = models.IntegerField(blank=True)
    email = models.EmailField(blank=True)
    referral_code = models.TextField(null=True, blank=True)
    workflow_state = models.IntegerField(blank=True, choices=WORKFLOW_STATUS_CHOICES)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(_('password'), max_length=128)

    objects = models.Manager()
