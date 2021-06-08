from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view

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
    try:
        unVaccin = Vaccin.objects.get(pk=pk)
        vaccin_serializer = VaccinSerializer(unVaccin)
        return JsonResponse(vaccin_serializer.data, safe=False)
    except Vaccin.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # GET / PUT / DELETE tutorial