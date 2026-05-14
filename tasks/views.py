from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Desafio 02: Endpoint de tarefas atrasadas
    @action(detail=False, methods=['get'])
    def atrasadas(self, request):
        # Define o que é "7 dias atrás" a partir de AGORA
        limite_data = timezone.now() - timedelta(days=7)
        
        # Filtra: não concluídas (False) E criadas antes do limite (atrasadas)
        tarefas = Task.objects.filter(
            is_done=False, 
            created_at__lt=limite_data
        )
        
        serializer = self.get_serializer(tarefas, many=True)
        return Response(serializer.data)