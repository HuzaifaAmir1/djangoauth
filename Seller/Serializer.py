from rest_framework import serializers
from .models import Seller, Language, Skill, Education,ProfilePicture,Portfolio,Rating


# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = ['name']
#     def create(self, validated_data):
#         seller = self.context.get('seller')
#         validated_data['seller'] = seller
#         language = Language.objects.create(**validated_data)
#         return language


# class SkillSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Skill
#         fields = ['name']
#     def create(self, validated_data):
#         seller = self.context.get('seller')
#         validated_data['seller'] = seller
#         skill = Skill.objects.create( **validated_data)
#         return skill


# class EducationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Education
#         fields = ['education', 'from_year', 'to_year']

# class SellerSerializer(serializers.ModelSerializer): 
#     languages = LanguageSerializer(many=True)
#     skills = SkillSerializer(many=True)
#     education=EducationSerializer(many=True)
#     class Meta:
#         model = Seller
#         fields = ['description','skills','education','languages','personal_website', 'phone_number']

#     def create(self, validated_data):
#         languages_data = validated_data.pop('languages')
#         skills_data = validated_data.pop('skills')
#         education_data = validated_data.pop('education') 

#         seller = Seller.objects.create(**validated_data)

#         education_data['seller'] = seller

#         for language_data in languages_data: 
#             Language.objects.create(seller=seller, **language_data)

#         for skill_data in skills_data:
#             Skill.objects.create(seller=seller, **skill_data)

#         if education_data:
#             Education.objects.create(seller=seller,**education_data)

#         return seller
#     def get_overall_rating(self, obj):
#         return obj.calculate_overall_rating()

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('education', 'from_year', 'to_year')

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name',)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name',)

class SellerSerializer(serializers.ModelSerializer):
    education = EducationSerializer()
    languages = LanguageSerializer(many=True)
    skills = SkillSerializer(many=True)

    class Meta:
        model = Seller
        fields = ('description', 'personal_website', 'phone_number', 'education', 'languages', 'skills')

    def create(self, validated_data):
        # Save the seller with the authenticated user
        # Change the user's role to 'seller'
        user = self.context['request'].user
        user.role = 'seller'
        user.save()
        education_data = validated_data.pop('education')
        languages_data = validated_data.pop('languages')
        skills_data = validated_data.pop('skills')
        print(validated_data)
        seller = Seller.objects.create(**validated_data)

        Education.objects.create(seller=seller, **education_data)

        for language_data in languages_data:
            Language.objects.create(seller=seller, **language_data)

        for skill_data in skills_data:
            Skill.objects.create(seller=seller, **skill_data)

        return seller

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.personal_website = validated_data.get('personal_website', instance.personal_website)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        education_data = validated_data.get('education', {})
        education_instance = instance.education
        education_instance.education = education_data.get('education', education_instance.education)
        education_instance.from_year = education_data.get('from_year', education_instance.from_year)
        education_instance.to_year = education_data.get('to_year', education_instance.to_year)
        education_instance.save()

        instance.languages.all().delete()
        languages_data = validated_data.get('languages', [])
        for language_data in languages_data:
            Language.objects.create(seller=instance, **language_data)

        instance.skills.all().delete()
        skills_data = validated_data.get('skills', [])
        for skill_data in skills_data:
            Skill.objects.create(seller=instance, **skill_data)

        instance.save()
        return instance

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['profile_picture']
        extra_kwargs = {
            'profile_picture': {'required': True}
        }

    def update(self, instance, validated_data):
        # Update the profile_picture field of the existing ProfilePicture instance
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

    def create(self, validated_data):
        # Since you are using a one-to-one relationship, you can create the ProfilePicture here
        seller = self.context.get('seller')
        try:
            profile_picture_instance = ProfilePicture.objects.get(seller=seller)
        except ProfilePicture.DoesNotExist:
            # If no ProfilePicture instance exists, create one
            validated_data['seller'] = seller
            profile_picture_instance = ProfilePicture.objects.create(**validated_data)
        else:
            # If a ProfilePicture instance exists, update the profile_picture field
            profile_picture_instance.profile_picture = validated_data.get('profile_picture', profile_picture_instance.profile_picture)
            profile_picture_instance.save()

        return profile_picture_instance
        # seller = self.context.get('seller')
        # validated_data['seller'] = seller
        # profile_picture = ProfilePicture.objects.create(**validated_data)
        # return profile_picture
    
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['profile_picture','url']
        extra_kwargs = {
            'profile_picture': {'required': True}
        }

    def create(self, validated_data):
        seller = self.context.get('seller')
        
        validated_data['seller'] = seller
        instance = Portfolio.objects.create(**validated_data)

        instance.save()

        return instance
    

    
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
    
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Rating.objects.filter(seller_id=seller_id)
    
from account.serializers import UserSerializer
class SellerinfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    portfolios = PortfolioSerializer(many=True)
    education = EducationSerializer()
    languages = LanguageSerializer(many=True)
    skills = SkillSerializer(many=True)
    profile_picture = ProfilePictureSerializer()

    class Meta:
        model = Seller
        fields = ('id', 'user', 'description', 'personal_website', 'phone_number', 'calculate_overall_rating', 'ratings', 'portfolios', 'education', 'languages', 'skills', 'profile_picture')