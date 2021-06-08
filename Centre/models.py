from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=75)
    Prenom = models.CharField(max_length=75)
    MailPatient = models.CharField(max_length=75)
    TelPatient = models.CharField(max_length=75)

    def __str__(self):
        return "%s %s", (self.Nom, self.Prenom)


class Pratiquant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=75)
    Prenom = models.CharField(max_length=75)
    status = models.CharField(max_length=75)

    def __str__(self):
        return "%s %s", (self.Nom, self.Prenom)


class Vaccin(models.Model):
    nomVac = models.CharField(max_length=75)
    nbrDoses = models.IntegerField()
    tempsEntreDoses = models.IntegerField()

    def __str__(self):
        return "Nom : %s", self.nomVac


class Lot(models.Model):
    noLot = models.IntegerField()
    QuantiteLot = models.IntegerField()
    QteRestante = models.IntegerField()
    Vaccin = models.ForeignKey(Vaccin, on_delete=models.CASCADE)

    def __str__(self):
        return "noLot : %s, Vaccin : %s", (self.noLot, self.Vaccin)


class EffetSecondaire(models.Model):
    nomLot = models.CharField(max_length=75)

    def __str__(self):
        return self.nomLot


class EnregistrerEffet(models.Model):
    Lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    EffetSecondaire = models.ForeignKey(EffetSecondaire, on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return "Patient : %s, Effet : %s, Vaccin : ", (self.Patient, self.EffetSecondaire, self.Lot)


class Creneau(models.Model):
    dateCreneau = models.DateField
    LotUtilise = models.ForeignKey(Lot, on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Pratiquant = models.ForeignKey(Pratiquant, on_delete=models.CASCADE)

    def __str__(self):
        return "Date : %s, Vaccin : %s, Patient : %s, Pratiquant : %s", (
            self.dateCreneau, self.LotUtilise, self.Patient, self.Pratiquant)
