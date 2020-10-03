from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class ManagerViewSets(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'])
    def add(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def delete(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def edit(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def search(self, request):
        pass


class ClientViewSets(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'])
    def add(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def search(self, request):
        pass

