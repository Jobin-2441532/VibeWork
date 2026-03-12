from rest_framework import serializers
from .models import User, Job, Application, Profile, Review, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'FREELANCER')
        )
        Profile.objects.create(user=user)
        return user

class JobSerializer(serializers.ModelSerializer):
    provider_username = serializers.ReadOnlyField(source='provider.username')
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'budget', 'is_active', 'created_at', 'provider', 'provider_username']
        read_only_fields = ['provider', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    freelancer_username = serializers.ReadOnlyField(source='freelancer.username')
    job_title = serializers.ReadOnlyField(source='job.title')
    
    freelancer_skills = serializers.SerializerMethodField()
    freelancer_resume = serializers.SerializerMethodField()
    freelancer_portfolio = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'job', 'freelancer', 'cover_letter', 'status', 'is_completed', 'created_at',
                  'freelancer_username', 'job_title', 'freelancer_skills', 'freelancer_resume', 'freelancer_portfolio']
        read_only_fields = ['freelancer', 'created_at']

    def get_freelancer_skills(self, obj):
        try:
            return obj.freelancer.profile.skills
        except:
            return None

    def get_freelancer_resume(self, obj):
        try:
            if obj.freelancer.profile.resume:
                return obj.freelancer.profile.resume.url
        except:
            pass
        return None

    def get_freelancer_portfolio(self, obj):
        try:
            return obj.freelancer.profile.portfolio_url
        except:
            return None

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    role = serializers.ReadOnlyField(source='user.role')
    email = serializers.ReadOnlyField(source='user.email')
    resume = serializers.SerializerMethodField()
    
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'role', 'email', 'skills', 'portfolio_url', 'resume', 'company_name', 'company_website', 'average_rating', 'total_reviews']
        read_only_fields = ['user']

    def get_resume(self, obj):
        if obj.resume:
            return obj.resume.url  # Returns /media/resumes/filename.pdf
        return None

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(reviewee=obj.user)
        if reviews.exists():
            from django.db.models import Avg
            return round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        return 0.0

    def get_total_reviews(self, obj):
        return Review.objects.filter(reviewee=obj.user).count()

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.ReadOnlyField(source='reviewer.username')
    reviewee_username = serializers.ReadOnlyField(source='reviewee.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Review
        fields = ['id', 'job', 'reviewer', 'reviewee', 'rating', 'comment', 'created_at', 'reviewer_username', 'reviewee_username', 'job_title']
        read_only_fields = ['reviewer', 'reviewee', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at', 'link']
        read_only_fields = ['created_at']
