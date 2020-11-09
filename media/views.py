"""
Views of media app
"""
# pylint: disable=E5142, R0901, E1101
import datetime
from django.db.models import Max
from rest_framework import viewsets, status, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from personnel.models import UserAudio, UserProfile
from .models import OriginMedia
from .serializers import MediaCreateSerializer, MediaUpdateSerializer, \
    MediaListSerializer, MediaSearchSerializer, MediaAnalysisSerializer, \
    UserAnalysisSerializer, UserAudioAnalysisSerializer, MediaChartSerializer, \
    UserChartSerializer, UserAudioChartSerializer

DATA_LOAD_FAIL = 'Fail to find the data'


class ManagerViewSets(viewsets.ModelViewSet):
    """
    API on api/manager, media data access of for manager
    """
    queryset = OriginMedia.objects.all().order_by('level_id')
    serializer_class = MediaCreateSerializer
    list_serializer = MediaListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """
        Get queryset
        """
        queryset = OriginMedia.objects.all().order_by('level_id')
        level = self.request.query_params.get('level_id', None)
        if level is not None:
            queryset = queryset.filter(level_id=level)
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        page_object = PageNumberPagination()
        size = self.request.query_params.get('size', None)
        if size is not None:
            queryset = page_object.paginate_queryset(queryset, self.request)
        return queryset

    def get_serializer_class(self):
        """
        Get serializer for different actions
        """
        if self.action == 'list':
            return self.list_serializer
        if self.action == 'create':
            return MediaCreateSerializer
        if self.action == 'update':
            return MediaUpdateSerializer
        return MediaUpdateSerializer


class ClientMediaViewSets(viewsets.ModelViewSet):
    """
    API on api/media, media data access for client
    """
    queryset = OriginMedia.objects.all().order_by('level_id')
    serializer_class = MediaCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """
        Get serializer for different actions
        """
        if self.action == 'material' or self.action == 'video' \
                or self.action == 'audio':
            return MediaSearchSerializer
        if self.action == 'list':
            return MediaListSerializer
        return MediaCreateSerializer

    @action(detail=False, methods=['POST'])
    def video(self, request):
        """
        return video file according to id
        """
        self.serializer_class = MediaSearchSerializer
        search_serializer = MediaSearchSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = request.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response(DATA_LOAD_FAIL, status=status.HTTP_404_NOT_FOUND)
            media_serializer = MediaCreateSerializer(media_data)
            video_path = media_serializer.data['video_path']
            url = video_path
            return Response(url, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def audio(self, request):
        """
        return audio file according to id
        """
        self.serializer_class = MediaSearchSerializer
        search_serializer = MediaSearchSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = request.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response(DATA_LOAD_FAIL, status=status.HTTP_404_NOT_FOUND)
            media_serializer = MediaCreateSerializer(media_data)
            audio_path = media_serializer.data['audio_path']
            url = audio_path
            return Response(url, status=status.HTTP_200_OK)
        return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def material(self, request):
        """
        return title and content according to id
        """
        self.serializer_class = MediaSearchSerializer
        search_serializer = MediaSearchSerializer(data=request.data)
        if search_serializer.is_valid():
            data_id = request.data['level_id']
            try:
                media_data = OriginMedia.objects.get(level_id=data_id)
            except OriginMedia.DoesNotExist:
                return Response(DATA_LOAD_FAIL, status=status.HTTP_404_NOT_FOUND)
            media_serializer = MediaCreateSerializer(media_data)
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
            user_audio = UserAudio.objects.filter(user=user_id, media=item['id'])
            score = user_audio.aggregate(score=Max('score'))['score']
            if score is None:
                score = 0
            scores.append(score)
        response.data = {'titles': titles, 'score': scores}
        return response


class PageNumberPagination(pagination.PageNumberPagination):
    """
    paginator
    """
    page_size = 20
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = None


class MediaDataViewSets(viewsets.ModelViewSet):
    """
    API on api/manager/data, data analysis for manager
    """
    permission_classes = [IsAuthenticated, ]
    queryset = OriginMedia.objects.all().order_by('level_id')
    serializer_class = MediaAnalysisSerializer

    def get_queryset(self):
        """
        Get queryset
        """
        queryset = OriginMedia.objects.all().order_by('level_id')
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        page_object = PageNumberPagination()
        size = self.request.query_params.get('size', None)
        if size is not None:
            queryset = page_object.paginate_queryset(queryset, self.request)
        return queryset

    def get_serializer_class(self):
        """
        Get serializer for different actions
        """
        if self.action == 'chart':
            return MediaChartSerializer
        return MediaAnalysisSerializer

    # @action(detail=False, methods=['GET'])
    # def chart(self, request):
    #     """
    #     overall data for charts
    #     """

    @action(detail=True, methods=['GET'])
    def chart(self, request, pk=None):
        """
        charts of one level
        """
        media = self.get_object()
        serializer = self.get_serializer(media)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataViewSets(viewsets.ModelViewSet):
    """
    API on api/manager/data/user, data analysis of user data for manager
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAnalysisSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        """
        get queryset
        """
        queryset = UserProfile.objects.all().order_by('pk')
        gender = self.request.query_params.get('gender', None)
        if gender is not None:
            queryset = queryset.filter(gender=gender)
        page_object = PageNumberPagination()
        size = self.request.query_params.get('size', None)
        if size is not None:
            queryset = page_object.paginate_queryset(queryset, self.request)
        return queryset

    def get_serializer_class(self):
        """
        get serializer class
        """
        if self.action == 'chart':
            return UserChartSerializer
        return UserAnalysisSerializer

    @action(detail=False, methods=['GET'])
    def chart(self, request):
        """
        overall data for charts
        """
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAudioDataViewSets(viewsets.ModelViewSet):
    """
    API on api/manager/data/user_audio, data analysis of user data for manager
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAudioAnalysisSerializer
    queryset = UserAudio.objects.all()

    def get_queryset(self):
        queryset = UserAudio.objects.all()
        level = self.request.query_params.get('level', None)
        gender = self.request.query_params.get('gender', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)
        sort = self.request.query_params.get('sort', None)
        if level is not None:
            media_id = OriginMedia.objects.get(level_id=level).id
            queryset = queryset.filter(media=media_id)
        if gender is not None:
            queryset = queryset.filter(user__userprofile__gender=gender)
        if start_time is not None:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
            queryset = queryset.filter(timestamp__gte=start_time)
        if end_time is not None:
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            queryset = queryset.filter(timestamp__lte=end_time)
        if sort == "score":
            queryset = queryset.order_by('score')
        if sort == "level":
            queryset = queryset.order_by('media__level_id')
        if sort == "time":
            queryset = queryset.order_by('timestamp')
        page_object = PageNumberPagination()
        size = self.request.query_params.get('size', None)
        if size is not None:
            queryset = page_object.paginate_queryset(queryset, self.request)
        return queryset

    @action(detail=False, methods=['GET'])
    def chart(self, request):
        """
        overall data for charts
        """
