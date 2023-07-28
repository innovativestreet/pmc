from django.shortcuts import render
from rest_framework import viewsets, permissions, status, views

from pmc_app.models import UserProfile
from pmc_app.searializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
