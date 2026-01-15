"""Core views."""
from django.shortcuts import render
from rest_framework.views import APIView


class WelcomeView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return render(request, 'welcome.html')


class APITestView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return render(request, 'api_test.html')