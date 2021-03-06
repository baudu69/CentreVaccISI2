from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Centre.Serializer import VaccinSerializer, LotSerializer, CreneauSerializer, UserSerializer, PatientSerializer
from Centre.models import Vaccin, Lot, Creneau, Patient, Pratiquant
from django.contrib.auth.middleware import get_user

from Tentative2CentreVacc.middleware import JWTAuthenticationInMiddleware


@api_view(['GET'])
def creneauPraticien(request):
    lesCreneaux = Creneau.objects.filter(Patient__creneau__isnull=False, Pratiquant__creneau__isnull=True)
    title = request.GET.get('title', None)
    if title is not None:
        lesCreneaux = lesCreneaux.filter(title__icontains=title).order_by('dateCreneau')
    creneau_serializer = CreneauSerializer(lesCreneaux, many=True)
    return JsonResponse(creneau_serializer.data, safe=False)


# Regler prblm mdp + ajouter patient
@api_view(['POST'])
def inscription(request):
    user_data = JSONParser().parse(request)
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        unUser = User.objects.latest('id')
        unUser.set_password(unUser.password)
        unPatient = Patient()
        unPatient.MailPatient = unUser.email
        unPatient.Nom = unUser.last_name
        unPatient.Prenom = unUser.first_name
        unPatient.user_id = unUser.id
        unPatient.save()
        unUser.save()
        return JsonResponse({'message': 'OK'}, status=status.HTTP_201_CREATED)
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def creneau_list(request, vaccin_id=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    lesCreneaux = Creneau.objects.filter(LotUtilise__Vaccin_id=vaccin_id, Patient__creneau__isnull=True,
                                         Pratiquant__creneau__isnull=True)
    title = request.GET.get('title', None)
    if title is not None:
        lesCreneaux = lesCreneaux.filter(title__icontains=title)
    creneau_serializer = CreneauSerializer(lesCreneaux, many=True)
    return JsonResponse(creneau_serializer.data, safe=False)


@api_view(['GET'])
def mesCreneaux_list(request):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        lePatient = Patient.objects.filter(user_id=request.user.id).first()
        lesCreneaux = Creneau.objects.filter(Patient=lePatient.id)
        creneau_serializer = CreneauSerializer(lesCreneaux, many=True)
        return JsonResponse(creneau_serializer.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def creneau_detail(request, pk=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    unCreneau = Creneau.objects.get(pk=pk)
    if request.method == 'GET':
        try:
            creneau_serializer = CreneauSerializer(unCreneau)
            return JsonResponse(creneau_serializer.data, safe=False)
        except Creneau.DoesNotExist:
            return JsonResponse({'message': 'Ce creneau n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        creneau_data = JSONParser().parse(request)
        creneau_serializer = CreneauSerializer(data=creneau_data)
        if creneau_serializer.is_valid():
            creneau_serializer.save()
            return JsonResponse(creneau_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(creneau_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        unCreneau.delete()
        return JsonResponse({'message': 'Creneau supprime'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def vaccin_list(request):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        lesVaccins = Vaccin.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            lesVaccins = lesVaccins.filter(title__icontains=title)

        vaccin_serializer = VaccinSerializer(lesVaccins, many=True)
        return JsonResponse(vaccin_serializer.data, safe=False)


@api_view(['GET'])
def lot_liste(request, pk=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    lesLots = Lot.objects.filter(Vaccin=pk)
    if request.method == 'GET':
        lot_serializer = LotSerializer(lesLots, many=True)
        return JsonResponse(lot_serializer.data, safe=False)


@api_view(['POST', 'GET'])
def lot_detail(request, pk=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        lot_data = JSONParser().parse(request)
        lot_serializer = LotSerializer(data=lot_data)
        if lot_serializer.is_valid():
            lot_serializer.save()
            return JsonResponse(lot_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        leLot = Lot.objects.get(pk=pk)
        lot_serializer = LotSerializer(leLot, many=False)
        return JsonResponse(lot_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def patient_detail(request, pk=''):
    if request.method == 'GET':
        lePatient = Patient.objects.get(pk=pk)
        patient_serializer = PatientSerializer(lePatient, many=False)
        return JsonResponse(patient_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def reserverCreneau(request, idCreneau=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    leCreneau = Creneau.objects.get(pk=idCreneau)
    lePatient = Patient.objects.filter(user_id=request.user.id).first()
    leCreneau.Patient = Patient.objects.get(pk=lePatient.id)
    leCreneau.save()
    return JsonResponse({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def annulerCreneau(request, idCreneau=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    leCreneau = Creneau.objects.get(pk=idCreneau)
    leCreneau.Patient = None
    leCreneau.save()
    return JsonResponse({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def validerCreneau(request, idCreneau=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    lePratiquant = Pratiquant.objects.filter(user_id=request.user.id).first()
    leCreneau = Creneau.objects.get(pk=idCreneau)
    leCreneau.Pratiquant = Pratiquant.objects.get(pk=lePratiquant.id)
    leCreneau.save()
    return JsonResponse({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(['PUT', 'GET'])
def detail_creneau(request, idCreneau=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        creneau_data = JSONParser().parse(request)
        creneau_serializer = CreneauSerializer(data=creneau_data)
        if creneau_serializer.is_valid():
            creneau_serializer.save()
            lotUtilise = creneau_serializer.data.get('LotUtilise')
            leLot = Lot.objects.get(pk=lotUtilise)
            leLot.QteRestante = leLot.QteRestante.real - 1
            leLot.save()
            return JsonResponse({'message': 'OK'}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'pasOK'}, status=status.HTTP_304_NOT_MODIFIED)
    elif request.method == 'GET':
        leCreneau = Creneau.objects.get(pk=idCreneau)
        leCreneauSerializer = CreneauSerializer(leCreneau, many=False)
        return JsonResponse(leCreneauSerializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def vaccin_detail(request, pk=''):
    if request.user is None:
        return JsonResponse({'message': 'Vous n\'etes pas connecte'}, status=status.HTTP_401_UNAUTHORIZED)
    unVaccin = Vaccin.objects.get(pk=pk)
    if request.method == 'GET':
        try:
            vaccin_serializer = VaccinSerializer(unVaccin)
            return JsonResponse(vaccin_serializer.data, safe=False)
        except Vaccin.DoesNotExist:
            return JsonResponse({'message': 'Ce vaccin n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        vaccin_data = JSONParser().parse(request)
        vaccin_serializer = VaccinSerializer(unVaccin, data=vaccin_data)
        if vaccin_serializer.is_valid():
            vaccin_serializer.save()
            return JsonResponse(vaccin_serializer.data)
        return JsonResponse(vaccin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        unVaccin.delete()
        return JsonResponse({'message': 'Vaccin supprime'}, status=status.HTTP_204_NO_CONTENT)


def get_jwt_user(request):
    user = get_user(request)
    if user.is_authenticated:
        return user
    jwt_authentication = JSONWebTokenAuthentication()
    if jwt_authentication.get_jwt_value(request):
        user, jwt = jwt_authentication.authenticate(request)
    return user
