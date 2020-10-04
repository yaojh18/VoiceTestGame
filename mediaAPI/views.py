from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class ManagerViewSets(viewsets.ModelViewSet):
    serializer_class = OriginMediaSerializer

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
        res = request.data
        if 'id' in res:
            data_id = res['id']
            try:
                media_data = OriginMedia.objects.get(pk=data_id)
            except:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'msg': 'Fail to find the data'})
            return Response({'code': status.HTTP_200_OK, 'msg': 'Data found successfully'})


class ClientViewSets(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'])
    def add(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def search(self, request):
        pass

