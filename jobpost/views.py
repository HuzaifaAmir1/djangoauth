from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import JobPost
from .serializers import JobPostSerializer
from jobpost.renderers import CustomStatusRenderer
from django.db.models import Q
from rest_framework.decorators import action
class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer] 

    def get_queryset(self):
        queryset = JobPost.objects.all()

        # Check if user wants to retrieve only their jobs
        if self.request.query_params.get('user_jobs') == 'true':
            queryset = queryset.filter(client=self.request.user.client)
        
        term = self.request.query_params.get('term')
        if term:
            queryset = queryset.filter(term=term)
        
        order_by = self.request.query_params.get('order_by')
        if order_by == 'most_recent':
            queryset = queryset.order_by('-created_time')  # - for descending order
        elif order_by == 'least_recent':
            queryset = queryset.order_by('created_time')
        
        return queryset
    @action(detail=False, methods=['GET'])
    def search(self, request):
        term = self.request.query_params.get('term')
        queryset = JobPost.objects.all()

        if term:
            queryset = queryset.filter(
                Q(job_title__icontains=term) |
                Q(description__icontains=term)
            )

        serializer = JobPostSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=self.request.user.client)
            
            response_data = {
                'message': 'Job post created successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            if 'freelancer' in request.data:
            # Assuming the value is an ID of the Seller, you can update the freelancer field
                instance.freelancer_id = request.data['freelancer']
            serializer.save()
            
            response_data = {
                'message': 'Job post updated successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        
        response_data = {
            'message': 'Job post deleted successfully.',
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


from .serializers import SavedJobSerializer,SavedJobSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SavedJob
class SaveJobView(APIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer] 
    def post(self, request, job_post_id):
        job_post_id = int(job_post_id)
        job_post = get_object_or_404(JobPost, pk=job_post_id)
        saved_job, created = SavedJob.objects.get_or_create(seller=request.user.seller, job_post=job_post)
        if created:
            return Response({'message': 'Job saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Job is already saved.'}, status=status.HTTP_200_OK)
    def delete(self, request, job_post_id):
        job_post_id = int(job_post_id)
        job_post = get_object_or_404(JobPost, pk=job_post_id)
        saved_job = SavedJob.objects.filter(seller=request.user.seller, job_post=job_post)
        if saved_job.exists():
            saved_job.delete()
            return Response({'message': 'Job removed from saved list.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Job not found in saved list.'}, status=status.HTTP_404_NOT_FOUND)

class SavedJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_jobs = SavedJob.objects.filter(seller=request.user.seller)
        serializer = SavedJobSerializer(saved_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
