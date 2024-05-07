from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status

from todo_list.models import TodoItem
from todo_list.serializers import TodoItemSerializer
class TodoItemView(APIView): # Klasse immer wie das Model benennen
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        todo_id = request.data.get('id')
        todo_item = TodoItem.objects.get(id=todo_id)
        print('test', todo_item)
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, format=None):
        todo_id = request.data.get('id')
        todo_item = TodoItem.objects.get(id=todo_id)
        
        updated_data = {
            'title': request.data.get('title') + ' (bearbeitet)'
        }
        serializer = TodoItemSerializer(todo_item, data=updated_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
