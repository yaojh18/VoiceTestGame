"""
TODO
"""
# pylint: disable=R0901
#from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import OriginMedia, UserAudio
from .serializers import OriginMediaSerializer, OriginMedia


class ManagerViewSets(viewsets.ModelViewSet):
    """
    TODO
    """
    queryset = OriginMedia.objects.none()
    serializer_class = OriginMediaSerializer

    @action(detail=False, methods=['POST'])
    def add(self, request):
        """
        TODO
        """

    @action(detail=False, methods=['POST'])
    def delete(self, request):
        """
        TODO
        """

    @action(detail=False, methods=['POST'])
    def edit(self, request):
        """
        TODO
        """

    # pylint: disable=W0612, R0201, R1710
    # these shouldn't be disabled.
    @action(detail=False, methods=['POST'])
    def search(self, request):
        """
        TODO
        """
        res = request.data
        if 'id' in res:
            data_id = res['id']
            try:
                media_data = OriginMedia.objects.get(pk=data_id)
            except OriginMedia.DoesNotExist:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'msg': 'Fail to find the data'})
            return Response({'code': status.HTTP_200_OK, 'msg': 'Data found successfully'})


class ClientViewSets(viewsets.ModelViewSet):
    """
    TODO
    """
    @action(detail=False, methods=['POST'])
    def add(self, request):
        """
        TODO
        """

    @action(detail=False, methods=['POST'])
    def search(self, request):
        """
        TODO
        """
