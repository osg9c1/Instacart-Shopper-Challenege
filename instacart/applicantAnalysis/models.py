from django.db import models


class Applicants(models.Model):
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

    objects = models.Manager()

    class Meta:
        db_table = u'applicants'

