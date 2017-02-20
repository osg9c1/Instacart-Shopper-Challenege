from django.contrib import admin
from models import Applicants


class ApplicantsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'first_name', 'last_name', 'region', 'phone', 'email', 'phone_type', 'source', 'over_21', 'reason',
    'workflow_state', 'created_at',
    'updated_at')

    list_filter = ('created_at',)

admin.site.register(Applicants, ApplicantsAdmin)