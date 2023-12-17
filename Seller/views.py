from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Seller
from .Serializer import SellerSerializer,ProfilePictureSerializer,PortfolioSerializer
from .renderers import CustomStatusRenderer
from rest_framework import generics
class SellerListCreateView(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print('hello world')
        print(self.request.user)
        serializer.save(user=self.request.user)

class SellerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Seller.objects.get(user=self.request.user)
    
# class SellerAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [CustomStatusRenderer]
#     def post(self, request, *args, **kwargs):
#         data = request.data.copy()
#         serializer = SellerSerializer(data=data)

#         if serializer.is_valid():
#             # Create a new Seller instance but don't save it yet
#             new_seller = serializer.save(user=request.user)

#             # Now, since user is a OneToOneField, save the Seller instance
#             # and associate it with the authenticated user
#             new_seller.user = request.user
#             new_seller.save()

#             return Response(status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .models import ProfilePicture,Portfolio
class ProfilePictureAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, *args, **kwargs):
            seller = Seller.objects.get(user=request.user)
            profile_picture = ProfilePicture.objects.filter(seller=seller).first()

            data = request.data.copy()
            data['user'] = request.user.id

            if profile_picture:
                serializer = ProfilePictureSerializer(profile_picture, data=data, context={'seller': seller}, partial=True)
            else:
                serializer = ProfilePictureSerializer(data=data, context={'seller': seller})

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get(user=request.user)
        profile_picture = ProfilePicture.objects.filter(seller=seller).first()

        if profile_picture:
            serializer = ProfilePictureSerializer(profile_picture)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Profile picture not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class PortfolioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, *args, **kwargs):
            seller = Seller.objects.get(user=request.user)
            portfolio = Portfolio.objects.filter(seller=seller).first()

            data = request.data.copy()
            data['user'] = request.user.id

            if portfolio:
                serializer = PortfolioSerializer(portfolio, data=data, context={'seller': seller}, partial=True)
            else:
                serializer = PortfolioSerializer(data=data, context={'seller': seller})

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get(user=request.user)
        portfolios = Portfolio.objects.filter(seller=seller)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from .models import Seller, Rating
from .Serializer import RatingSerializer
from notifications.models import Notification 
class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        value = request.data.get("value")
        review = request.data.get("review", "")

        rating = Rating(seller=seller, user=user, value=value, review=review)
        rating.save()
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
from rest_framework import generics
class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class SellerOverallRatingView(APIView):
    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

        overall_rating = seller.calculate_overall_rating()
        return Response({"overall_rating": overall_rating}, status=status.HTTP_200_OK)
    

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
class SellerDetailViewset(viewsets.ModelViewSet):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['overall_rating'] = instance.calculate_overall_rating()
        return Response(data)
    
from rest_framework import viewsets
from .models import Seller, Education, Language, Skill
from .Serializer import SellerSerializer, EducationSerializer,LanguageSerializer,SkillSerializer,SellerSerializer
from rest_framework.decorators import action
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Seller.objects.filter(user_id=user_id)

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Education.objects.filter(seller__id=seller_id)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Language.objects.filter(seller__id=seller_id)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Skill.objects.filter(seller__id=seller_id)


from rest_framework import generics
from .models import Seller
from .Serializer import SellerinfoSerializer

class SellerListView(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerinfoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            # If user_id is provided, fetch information for that specific user
            return Seller.objects.filter(user__id=user_id)
        else:
            # Otherwise, fetch information for all sellers
            return Seller.objects.filter(user__id= self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)