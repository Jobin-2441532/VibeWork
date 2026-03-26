from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count, Sum, Q
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Job, Application, Profile, Review, Notification
from .serializers import (
    UserSerializer, JobSerializer, ApplicationSerializer,
    ProfileSerializer, ReviewSerializer, NotificationSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        if user.email:
            try:
                html_message = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; color: #333;">
                    <div style="background-color: #1a1a2e; padding: 20px; text-align: center;">
                        <h1 style="color: #4facfe; margin: 0;">VibeWork</h1>
                    </div>
                    <div style="padding: 20px;">
                        <h2 style="color: #333;">Welcome aboard, {user.username}!</h2>
                        <p>We are absolutely thrilled to have you join <strong>VibeWork</strong>, the premier freelance marketplace.</p>
                        <p>Whether you're here to hire top talent or find your next big project, you're in the right place.</p>
                        <div style="text-align: center; margin: 20px 0;">
                            <img src="http://127.0.0.1:3000/vibework_promo_banner.png" alt="VibeWork Promo" style="width: 100%; max-width: 500px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        </div>
                        <p style="text-align: center;">
                            <a href="http://127.0.0.1:3000/" style="background-color: #4facfe; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">Explore the Marketplace</a>
                        </p>
                    </div>
                    <div style="background-color: #f7f7f7; padding: 15px; text-align: center; font-size: 12px; color: #888;">
                        &copy; 2026 VibeWork. All rights reserved.
                    </div>
                </div>
                """
                send_mail(
                    subject='Welcome to VibeWork!',
                    message=f'Hi {user.username},\n\nWelcome to VibeWork - The Premier Freelance Marketplace! We are excited to have you on board.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                    html_message=html_message
                )
            except Exception as e:
                print(f"Failed to send email: {e}")

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            response.data['user_id'] = user.id
            response.data['role'] = user.role
            response.data['username'] = user.username
        return response

class JobListView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

    def get_queryset(self):
        # If user is a provider, show all active jobs, or optionally their own
        if self.request.user.role == 'PROVIDER':
            return Job.objects.filter(provider=self.request.user).order_by('-created_at')
        return super().get_queryset()

class ApplicationListView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job_id = self.request.data.get('job')
        job = Job.objects.get(id=job_id)
        serializer.save(freelancer=self.request.user, job=job)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'FREELANCER':
            return Application.objects.filter(freelancer=user).order_by('-created_at')
        elif user.role == 'PROVIDER':
            # Provider sees applications for their jobs
            return Application.objects.filter(job__provider=user).order_by('-created_at')
        return Application.objects.none()

class ApplicationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Only Provider can change status or mark complete
        if user.role == 'PROVIDER' and instance.job.provider == user:
            old_status = instance.status
            old_completed = instance.is_completed
            
            new_status = request.data.get('status', old_status)
            new_completed = request.data.get('is_completed', old_completed)
            
            # Type casting for safety if it comes as string from JS
            if isinstance(new_completed, str):
                new_completed = new_completed.lower() in ['true', '1', 'yes']

            changed = False
            
            if new_status != old_status:
                instance.status = new_status
                changed = True
                Notification.objects.create(
                    recipient=instance.freelancer,
                    title=f"Application {new_status.title()}",
                    message=f"Your application for '{instance.job.title}' was {new_status.lower()}.",
                )
                
                # Send email if application is accepted
                if new_status == 'ACCEPTED' and instance.freelancer.email:
                    try:
                        html_message = f"""
                        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; color: #333;">
                            <div style="background-color: #1a1a2e; padding: 20px; text-align: center;">
                                <h1 style="color: #4facfe; margin: 0;">VibeWork</h1>
                            </div>
                            <div style="padding: 20px;">
                                <h2 style="color: #333;">Congratulations, {instance.freelancer.username}!</h2>
                                <p>Great news! Your application for the job <strong>'{instance.job.title}'</strong> has been accepted by the provider <strong>'{user.username}'</strong>.</p>
                                <div style="text-align: center; margin: 20px 0;">
                                    <img src="http://127.0.0.1:3000/vibework_promo_banner.png" alt="VibeWork Promo" style="width: 100%; max-width: 500px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                                </div>
                                <p style="text-align: center;">
                                    <a href="http://127.0.0.1:3000/freelancer_dashboard.html" style="background-color: #4facfe; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">View Your Dashboard</a>
                                </p>
                            </div>
                            <div style="background-color: #f7f7f7; padding: 15px; text-align: center; font-size: 12px; color: #888;">
                                &copy; 2026 VibeWork. All rights reserved.
                            </div>
                        </div>
                        """
                        send_mail(
                            subject='Your Application was Accepted!',
                            message=f"Hi {instance.freelancer.username},\n\nGreat news! Your application for the job '{instance.job.title}' has been accepted by the provider '{user.username}'.\n\nGood luck with the project!\n\nThe VibeWork Team",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[instance.freelancer.email],
                            fail_silently=False,
                            html_message=html_message
                        )
                    except Exception as e:
                        print(f"Failed to send acceptance email: {e}")
                
            if new_completed and not old_completed:
                instance.is_completed = True
                changed = True
                # Notify Freelancer
                Notification.objects.create(
                    recipient=instance.freelancer,
                    title="Job Completed!",
                    message=f"The job '{instance.job.title}' has been marked as completed. You can leave a review!",
                )
                # Notify Provider
                Notification.objects.create(
                    recipient=user,
                    title="Job Completed!",
                    message=f"You marked '{instance.job.title}' as completed. Please leave a review.",
                )

            if changed:
                instance.save()
            return Response(self.get_serializer(instance).data)

        # Freelancer could theoretically update their cover letter before approval, but restricting for MVP
        return Response({'detail': 'Not authorized to update this application'}, status=status.HTTP_403_FORBIDDEN)

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'PROVIDER':
            total_jobs = Job.objects.filter(provider=user).count()
            total_applications = Application.objects.filter(job__provider=user).count()
            # Calculate total budget of active jobs
            total_budget = Job.objects.filter(provider=user).aggregate(Sum('budget'))['budget__sum'] or 0
            
            return Response({
                'total_jobs': total_jobs,
                'total_applications': total_applications,
                'total_budget': total_budget,
            })
        elif user.role == 'FREELANCER':
            total_applications = Application.objects.filter(freelancer=user).count()
            accepted = Application.objects.filter(freelancer=user, status='ACCEPTED').count()
            rejected = Application.objects.filter(freelancer=user, status='REJECTED').count()
            
            return Response({
                'total_applications': total_applications,
                'accepted': accepted,
                'rejected': rejected,
            })
        return Response({'detail': 'Role undefined'}, status=400)

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Auto-create profile if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Handle text fields via serializer (skills, portfolio_url, company_name, etc.)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Manually save text fields that the serializer handles
        if 'skills' in request.data:
            instance.skills = request.data['skills']
        if 'portfolio_url' in request.data:
            instance.portfolio_url = request.data['portfolio_url']
        if 'company_name' in request.data:
            instance.company_name = request.data['company_name']
        if 'company_website' in request.data:
            instance.company_website = request.data['company_website']

        # Handle resume file upload explicitly (request.FILES)
        if 'resume' in request.FILES:
            instance.resume = request.FILES['resume']

        instance.save()
        return Response(self.get_serializer(instance).data)

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can see reviews they have received or given
        user = self.request.user
        return Review.objects.filter(Q(reviewer=user) | Q(reviewee=user)).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        job = serializer.validated_data['job']
        
        # Determine who is the reviewee based on who is reviewing.
        if user.role == 'PROVIDER':
            # Provider reviewing freelancer
            app = Application.objects.filter(job=job, status='ACCEPTED').first()
            if app:
                reviewee = app.freelancer
            else:
                raise serializers.ValidationError("No accepted freelancer found for this job.")
        else:
            # Freelancer reviewing provider
            reviewee = job.provider
            
        serializer.save(reviewer=user, reviewee=reviewee, job=job)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

class NotificationUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        return Response(self.get_serializer(instance).data)
