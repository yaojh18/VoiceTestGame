"""
TODO
"""
# pylint: disable=R0901
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import OriginMedia, UserAudio
from .serializers import OriginMediaSerializer, UserAudioSerializer


class ManagerViewSets(viewsets.ModelViewSet):
    """
    actions on OriginMedia
    """
    queryset = OriginMedia.objects.all()
    serializer_class = OriginMediaSerializer

    @action(detail=False, methods=['POST'])
    def add(self, request):
        """
        add an object to OriginMedia
        """

    @action(detail=False, methods=['POST'])
    def delete(self, request):
        """
        delete an object from OriginMedia
        TODO
        """

    @action(detail=False, methods=['POST'])
    def edit(self, request):
        """
        edit an object in OriginMedia
        """

    # pylint: disable=R0201, R1710
    # these shouldn't be disabled.
    @action(detail=False, methods=['POST'])
    def search(self, request):
        """
        search in OriginMedia according to id
        """
        res = request.data
        if 'id' in res:
            data_id = res['id']
            try:
                _ = OriginMedia.objects.get(pk=data_id)
            except OriginMedia.DoesNotExist:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'msg': 'Fail to find the data'})
            return Response({'code': status.HTTP_200_OK, 'msg': 'Data found successfully'})


class ClientViewSets(viewsets.ModelViewSet):
    """
    actions on UserAudio
    """
    queryset = UserAudio.objects.all()
    serializer_class = UserAudioSerializer

    @action(detail=False, methods=['POST'])
    def add(self, request):
        """
        add an object to UserAudio
        TODO
        """

    @action(detail=False, methods=['POST'])
    def search(self, request):
        """
        search in UserAudio
        TODO
        """
