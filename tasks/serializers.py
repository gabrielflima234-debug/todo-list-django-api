from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    # Desafio 01: Mostra o nome da categoria além do ID
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_done', 'created_at', 'priority', 'category', 'category_name']

    # Desafio 03: Validação de prioridade
    def validate(self, data):
        priority = data.get('priority')
        is_done = data.get('is_done', False)

        # Se a tarefa for de alta prioridade e não estiver concluída
        if priority == 'alta' and not is_done:
            # Conta quantas tarefas 'alta' não concluídas já existem no banco
            total_alta_abertas = Task.objects.filter(priority='alta', is_done=False).count()
            
            if total_alta_abertas >= 3:
                raise serializers.ValidationError(
                    "Não é permitido ter mais de 3 tarefas de alta prioridade pendentes."
                )
                
        return data