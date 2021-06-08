from rest_framework import serializers
from Centre.models import Vaccin


class VaccinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccin
        fields = ('id',
                  'nomVac',
                  'nbrDoses',
                  'tempsEntreDoses')
