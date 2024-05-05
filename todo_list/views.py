from django.shortcuts import render

# Create your views here.

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from todo_list.models import TodoItem
from todo_list.serializers import TodoItemSerializer
class TodoItemView(APIView): # Klasse immer wie das Model benennen
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        
        return Response(serializer.data)

class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })
