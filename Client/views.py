from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Client, ProfilePicture
from .Serializer import ClientSerializer, ProfilePictureSerializer
from .renderers import CustomStatusRenderer
# API View for updating profile picture alone
class ProfilePictureAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, *args, **kwargs):
        client = Client.objects.get(user=request.user)
        profile_picture = ProfilePicture.objects.filter(client=client).first()

        data = request.data.copy()
        data['user'] = request.user.id

        if profile_picture:
            serializer = ProfilePictureSerializer(profile_picture, data=data, context={'client': client}, partial=True)
        else:
            serializer = ProfilePictureSerializer(data=data, context={'client': client})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        client = Client.objects.get(user=request.user)
        profile_picture = ProfilePicture.objects.get(client=client)
        serializer = ProfilePictureSerializer(profile_picture)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        client = Client.objects.get(user=request.user)
        data = request.data.copy()

        # Separate profile picture data from other fields
        profile_picture_data = data.pop('profile_picture', None)

        serializer = ProfilePictureSerializer(client, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Update profile picture separately if provided in the request
            if profile_picture_data:
                profile_picture_serializer = ProfilePictureSerializer(
                    instance=client.profilepicture, data={'profile_picture': profile_picture_data})
                if profile_picture_serializer.is_valid():
                    profile_picture_serializer.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# views.py in Client app
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Client
from .Serializer import ClientSerializer

class ClientCreateView(generics.CreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ClientSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Client.objects.filter(user=self.request.user)
    
    # views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Client
from .Serializer import ClientupdateSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
User = get_user_model()

class ClientListView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = ClientupdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        # If user_id is provided in the URL, return the Client object for that user
        if user_id:
            user = get_object_or_404(User, userId=user_id)
            return Client.objects.filter(user=user)

        # If no user_id is provided, return the Client object for the current user
        return Client.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        # Set the current user when updating a Client object
        serializer.save(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
from .Serializer import ClientinfoSerializer
class ClientDetailView(generics.ListAPIView):
    serializer_class = ClientinfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Client.objects.all()
    lookup_field = 'user_id'
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Client.objects.filter(user=user_id)


    

class CurrentUserClientView(generics.ListAPIView):
    serializer_class = ClientinfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return data for the current user
        return Client.objects.filter(user=self.request.user)
    

    
