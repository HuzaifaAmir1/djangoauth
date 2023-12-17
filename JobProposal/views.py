# from rest_framework import viewsets
# from .models import JobProposal
# from .serializers import JobProposalSerializer  # You'll need to create this serializer

# class JobProposalViewSet(viewsets.ModelViewSet):
#     queryset = JobProposal.objects.all()
#     serializer_class = JobProposalSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import JobProposal
from .serializers import JobProposalSerializer
from rest_framework import renderers
from rest_framework.response import Response
import json

class CustomStatusRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response =''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps(data)
        return response


class JobProposalViewSet(viewsets.ModelViewSet):
    queryset = JobProposal.objects.all()
    serializer_class = JobProposalSerializer
    renderer_classes = [CustomStatusRenderer] 
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def get_queryset(self):
        queryset = JobProposal.objects.all()
        if self.request.query_params.get('job_post_id'):
            job_post_id = self.request.query_params.get('job_post_id')
            queryset = queryset.filter(job_post_id=job_post_id)


        return queryset

    def perform_create(self, serializer):
        # Customize how a new JobProposal is created here, if needed
        serializer.save(seller=self.request.user.seller)

    def perform_update(self, serializer):
        # Customize how a JobProposal is updated here, if needed
        serializer.save()

    def perform_destroy(self, instance):
        # Customize how a JobProposal is deleted here, if needed
        instance.delete()
