from rest_framework import serializers
from .models import *


class DSASerializer(serializers.ModelSerializer):
    class Meta:
        model=DSA
        fields='__all__'



class DSAApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=DSA_Applications
        fields='__all__'