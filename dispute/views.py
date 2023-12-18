# in dispute/views.py
from rest_framework import generics, permissions
from .models import Dispute
from .serializers import DisputeSerializer
from .renderers import CustomStatusRenderer

class DisputeListCreateView(generics.ListCreateAPIView):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer
    renderer_classes = [CustomStatusRenderer] 

    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Filter disputes based on the current user
        return Dispute.objects.filter(client=self.request.user)
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class DisputeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dispute.objects.all()
    renderer_classes = [CustomStatusRenderer] 
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]
from rest_framework.response import Response
class DisputeUpdateResolvedView(generics.UpdateAPIView):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.resolved = request.data.get('resolved', instance.resolved)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)