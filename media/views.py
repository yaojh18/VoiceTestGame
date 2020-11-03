"""
Views of media app
"""
# pylint: disable=E5142, R0901, E1101
from django.db.models import Max
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from personnel.models import UserAudio, UserProfile
from .models import OriginMedia
from .serializers import OriginMediaCreateSerializer, OriginMediaUpdateSerializer,\
    SearchOriginSerializer, EditOriginSerializer, OriginMediaListSerializer


class ManagerViewSets(viewsets.ModelViewSet):
    """
    API on api/manager, media data access of for manager
    """
    queryset = OriginMedia.objects.all().order_by('level_id')
    serializer_class = OriginMediaCreateSerializer
    list_serializer = OriginMediaListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """
        Get queryset
        """
        queryset = OriginMedia.objects.all().order_by('level_id')
        level = self.request.query_params.get('level_id', None)
        if level is not None:
            queryset = queryset.filter(level_id=level)
        name = self.request.query_params.get('title', None)
        if name is not None:
            queryset = queryset.filter(title__icontains=name)
        page_limit = self.request.query_params.get('page_limit', None)
        if page_limit is not None:
            page_limit = int(page_limit)
            page_start = int(self.request.query_params.get('page_start', 0))
            page_start = min(page_start, queryset.count())
            page_end = min(page_start+page_limit, queryset.count())
            queryset = queryset.all()[page_start:page_end]
            print(page_start,page_end)
        return queryset

    def get_serializer_class(self):
        """
        Get serializer for different actions
        """
        if self.action == 'search':
            return SearchOriginSerializer
        if self.action == 'list':
            return self.list_serializer
        if self.action == 'create' or self.action == 'add':
            return OriginMediaCreateSerializer
        if self.action == 'update' or self.action == 'edit':
            return OriginMediaUpdateSerializer
        return OriginMediaUpdateSerializer


class ClientMediaViewSets(viewsets.ModelViewSet):
    """
    API on api/media, media data access for client
    """
    queryset = OriginMedia.objects.all().order_by('level_id')
    serializer_class = OriginMediaCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """
        Get serializer for different actions
        """
        if self.action == 'material' or self.action == 'video' \
                or self.action == 'audio':
            return SearchOriginSerializer
        if self.action == 'list':
            return OriginMediaListSerializer
        return OriginMediaCreateSerializer

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
            media_serializer = OriginMediaCreateSerializer(media_data)
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
            media_serializer = OriginMediaCreateSerializer(media_data)
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
            media_serializer = OriginMediaCreateSerializer(media_data)
            title = media_serializer.data['title']
            content = media_serializer.data['content']
            return Response({'title': title, 'text': content}, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        response = super().list(request)
        user_id = self.request.user
        titles = []
        scores = []
        for item in response.data:
            titles.append(item['title'])
            user_audio = UserAudio.objects.filter(user=user_id, level=item['id'])
            score = user_audio.aggregate(score=Max('score'))['score']
            if score is None:
                score = 0
            scores.append(score)
        response.data = {'titles': titles, 'score': scores}
        return response


class MediaDataViewSets(viewsets.ModelViewSet):
    """
    API on api/manager/data/media, data analysis of media data for manager
    """


class UserDataViewSets(viewsets.ModelViewSet):
    """
    API on api/manager/data/user, data analysis of user data for manager
    """


class UserAudioDataViewSets(viewsets.ModelViewSet):
    """
    API on api/manager/data/user_audio, data analysis of user data for manager
    """
