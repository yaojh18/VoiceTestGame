"""
Views of media app
"""
# pylint: disable=E5142, R0901
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import OriginMedia, UserAudio
from .serializers import OriginMediaSerializer, UserAudioSerializer, \
    SearchOriginSerializer, EditOriginSerializer


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
        self.serializer_class = OriginMediaSerializer
        media_serializer = OriginMediaSerializer(data=request.data)
        if media_serializer.is_valid():
            media_serializer.save()
            return Response(media_serializer.data, status=status.HTTP_201_CREATED)
        print('add:400', media_serializer.errors)
        return Response(media_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def edit(self, request):
        """
        edit an object in OriginMedia
        """
        self.serializer_class = EditOriginSerializer
        search_serializer = EditOriginSerializer(data=request.data)
        if search_serializer.is_valid():
            edit_res = search_serializer.update_data()
            if edit_res:
                return Response(search_serializer.data, status=status.HTTP_201_CREATED)
            return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
        print('edit:400', search_serializer.errors)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # pylint: disable=R0201, R1710
    # these shouldn't be disabled.
    @action(detail=False, methods=['POST'])
    def search(self, request):
        """
        search in OriginMedia according to id
        """
        self.serializer_class = SearchOriginSerializer
        search_serializer = SearchOriginSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = search_serializer.data['id']
            try:
                media_data = OriginMedia.objects.get(pk=data_id)
            except OriginMedia.DoesNotExist:
                return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
            media_serializer = OriginMediaSerializer(media_data)
            return Response(media_serializer.data, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def delete(self, request):
        """
        delete an object from OriginMedia
        TODO
        """


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
