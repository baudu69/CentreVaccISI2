from django.contrib.auth.models import User
from rest_framework import serializers
from Centre.models import Vaccin, Lot, Creneau


class VaccinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccin
        fields = ('id',
                  'nomVac',
                  'nbrDoses',
                  'tempsEntreDoses')


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ('id',
                  'noLot',
                  'QuantiteLot',
                  'QteRestante',
                  'Vaccin')


class CreneauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creneau
        fields = ('id',
                  'dateCreneau',
                  'LotUtilise',
                  'Patient',
                  'Pratiquant')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'password',
                  'email',
                  'first_name',
                  'last_name')
