
from django.shortcuts import render
from rest_framework import generics,viewsets,status

from dsaSLN.serializers import DSASerializer,DSAApplicationsSerializer
from .models import *
from rest_framework.response import Response




class DSAViewsets(viewsets.ModelViewSet):
    queryset=DSA.objects.all()
    serializer_class=DSASerializer

    

    def getByRegisterId(self,request,register_id):
     try:
        queryset = DSA.objects.filter(dsa_registerid=register_id)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data,status=200)
        else:
            return Response({"message": "No records found"}, status=404)
     except Exception as e:
        return Response({"error": str(e)}, status=500)


class DSA_AppliViewsets(viewsets.ModelViewSet):
    queryset=DSA_Applications.objects.all()
    serializer_class=DSAApplicationsSerializer

   

   