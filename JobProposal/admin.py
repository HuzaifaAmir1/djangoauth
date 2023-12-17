from django.contrib import admin
from .models import JobProposal

@admin.register(JobProposal)
class JobProposalAdmin(admin.ModelAdmin):
    list_display = ('job_post', 'bid', 'get_duration_display', 'seller')
    list_filter = ('duration', 'seller')
    search_fields = ('job_post__job_title', 'seller__user__name', 'seller__user__email')

    def get_duration_display(self, obj):
        return dict(JobProposal.DURATION_CHOICES).get(obj.duration, obj.duration)
    
    get_duration_display.short_description = 'Duration'
