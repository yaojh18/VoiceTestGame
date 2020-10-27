"""
Views of media app
"""
# pylint: disable=E5142, R0901
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import OriginMedia
from .serializers import OriginMediaSerializer, SearchOriginSerializer, \
    EditOriginSerializer, ListOriginSerializer


class ManagerViewSets(viewsets.ModelViewSet):
    """
    actions on OriginMedia
    """
    queryset = OriginMedia.objects.all().order_by('level_id')
    serializer_class = OriginMediaSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """
        Get serializer for different actions
        """
        # if self.action == 'add':
        #     return OriginMediaSerializer
        # if self.action == 'edit':
        #     return EditOriginSerializer
        # if self.action == 'get_list':
        #     return ListOriginSerializer
        # return SearchOriginSerializer
        if self.action == 'search' or self.action == 'material' \
                or self.action == 'video' or self.action == 'audio':
            return SearchOriginSerializer
        return OriginMediaSerializer

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
        # print('add:400', media_serializer.errors)
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
        # print('edit:400', search_serializer.errors)
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
            data_id = search_serializer.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
            media_serializer = OriginMediaSerializer(media_data)
            return Response(media_serializer.data, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def video(self, request):
        """
        return video file according to id
        """
        self.serializer_class = SearchOriginSerializer
        search_serializer = SearchOriginSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = request.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
            media_serializer = OriginMediaSerializer(media_data)
            video_path = media_serializer.data['video_path']
            url = video_path
            return Response(url, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def audio(self, request):
        """
        return audio file according to id
        """
        self.serializer_class = SearchOriginSerializer
        search_serializer = SearchOriginSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = request.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
            media_serializer = OriginMediaSerializer(media_data)
            audio_path = media_serializer.data['audio_path']
            url = audio_path
            return Response(url, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def material(self, request):
        """
        return title and content according to id
        """
        self.serializer_class = SearchOriginSerializer
        search_serializer = SearchOriginSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = request.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response('Fail to find the data', status=status.HTTP_404_NOT_FOUND)
            media_serializer = OriginMediaSerializer(media_data)
            title = media_serializer.data['title']
            content = media_serializer.data['content']
            return Response({'title': title, 'text': content}, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_list(self, request):
        """
        return list of data
        """
        self.serializer_class = ListOriginSerializer
        list_serializer = ListOriginSerializer(OriginMedia.objects.all(), many=True)
        data = self.generate_list(list_serializer)
        return Response(data, status=status.HTTP_200_OK)

    def generate_list(self, serializer):
        """
        change the format of list
        """
        titles = []
        scores = []
        for item in serializer.data:
            titles.append(item['title'])
            scores.append(0)
        return {'titles': titles, 'scores': scores}
