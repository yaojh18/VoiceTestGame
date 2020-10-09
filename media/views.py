"""
Views of media app
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
        media_serializer = self.serializer_class(data=request.data)
        if media_serializer.is_valid():
            media_serializer.save()
            return Response(media_serializer.data, status=status.HTTP_201_CREATED)
        return Response(media_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        media_serializer = self.serializer_class(data=request.data)
        if media_serializer.is_valid():
            try:
                old_data = OriginMedia.objects.get(pk=media_serializer.id)
            except OriginMedia.DoesNotExist:
                return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
            self.serializer_class.update(old_data)
            return Response('')

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
                media_data = OriginMedia.objects.get(pk=data_id)
            except OriginMedia.DoesNotExist:
                return Response({'code': status.HTTP_404_NOT_FOUND, 'msg': 'Fail to find the data'})
            return Response(media_data.content, status=status.HTTP_200_OK)


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
