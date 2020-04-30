from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from chat import settings
from core.serializers import MessageModelSerializer, UserModelSerializer,GroupMessageSerializer
from core.models import MessageModel,GroupMessage


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__username=target) |
                Q(recipient__username=target, user=request.user))
            return super(MessageModelViewSet, self).list(request, *args, **kwargs)
        else:
            print("handle get without parameters")
            
    # @ POST
    # @ /api/v1/message/ 
    # @ Description: receives message to be sent, saves it and notifies users
    def create(self, request, *args, **kwargs):
        self.serializer_class(data=request.data)
        return super(MessageModelViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
class GroupMessageViewSet(ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    # # Change this soon
    # def list(self, request, *args, **kwargs):
    #     print("InSIDE 00))))00000")
    #     target = self.request.query_params.get('target', None)
    #     if target is not None:
    #         self.queryset = self.queryset.filter()
    #     return super(GroupMessage, self).list(request, *args, **kwargs)
            
    def get_queryset(self):
        queryset = GroupMessage.objects.all()
        target = self.request.query_params.get('target', None)

        if target is not None:
            pass
            # queryset = queryset.filter(pks__in=target)

        return queryset
    # @ POST
    # @ /api/v1/message/ 
    # @ Description: receives message to be sent, saves it and notifies users
    def create(self, request, *args, **kwargs):
        self.serializer_class(data=request.data)
        return super(GroupMessage, self).create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)
