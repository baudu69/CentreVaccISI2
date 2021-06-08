from rest_framework import serializers
from Centre.models import Vaccin, Lot


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
