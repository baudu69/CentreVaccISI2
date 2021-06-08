from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from Centre.Serializer import VaccinSerializer
from Centre.models import Vaccin


@api_view(['GET', 'POST', 'DELETE'])
def vaccin_list(request):
    if request.method == 'GET':
        lesVaccins = Vaccin.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            lesVaccins = lesVaccins.filter(title__icontains=title)

        vaccin_serializer = VaccinSerializer(lesVaccins, many=True)
        return JsonResponse(vaccin_serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def vaccin_detail(request, pk):
    unVaccin = Vaccin.objects.get(pk=pk)
    if request.method == 'GET':
        try:
            vaccin_serializer = VaccinSerializer(unVaccin)
            return JsonResponse(vaccin_serializer.data, safe=False)
        except Vaccin.DoesNotExist:
            return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        vaccin_data = JSONParser().parse(request)
        vaccin_serializer = VaccinSerializer(unVaccin, data=vaccin_data)
        if vaccin_serializer.is_valid():
            vaccin_serializer.save()
            return JsonResponse(vaccin_serializer.data)
        return JsonResponse(vaccin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        unVaccin.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
