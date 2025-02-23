from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import News
from .serializers import NewsSerializer
from django_filters.rest_framework import DjangoFilterBackend

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['publication_date']

    def get_permissions(self):
        """
        Настройка прав доступа:
        - Администраторы могут создавать, редактировать и удалять новости.
        - Остальные пользователи могут только просматривать новости.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Только администраторы могут выполнять эти действия
            return [permissions.IsAdminUser()]
        else:
            # Все пользователи могут просматривать новости
            return [permissions.AllowAny()]

    def list(self, request, *args, **kwargs):
        """
        Просмотр всех новостей.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр конкретной новости по ID.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Создание новости (только для администраторов).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Обновление новости (только для администраторов).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление новости (только для администраторов).
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)