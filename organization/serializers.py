from rest_framework.serializers import ModelSerializer
from .models import Organization


class OrganSerializar(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'province', 'phone', 'email', 'agent', 'agent_phone']
