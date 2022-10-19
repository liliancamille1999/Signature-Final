from django.contrib.auth.models import User
from django.db import models


class entreprise(models.Model):
    NomE = models.CharField(max_length=255, verbose_name="NomE")
    Secteur = models.CharField(max_length=255, verbose_name="Secteur")
    Region = models.CharField(max_length=255, verbose_name="Region")
    Ville = models.CharField(max_length=255, verbose_name="Ville")
    Unit_name = models.CharField(max_length=255, verbose_name="Unit_name")
    Date_de_creation = models.DateField()
    emailE = models.EmailField()
    telE = models.CharField(max_length=255, verbose_name="TelE")

    class Meta:
        ordering = ['-NomE']
        verbose_name = "Entreprise"

    def __str__(self):
        return self.NomE

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Personne(models.Model):
    Nom = models.CharField(max_length=255, verbose_name="Nom")
    Prenom = models.CharField(max_length=255, verbose_name="Prenom")
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True)
    Entreprise = models.ForeignKey(entreprise, on_delete=models.SET_DEFAULT, default=0)
    Sexe = models.CharField(max_length=255, verbose_name="Sexe")
    Date_naissance = models.CharField(max_length=255,verbose_name="date")
    email = models.EmailField()
    tel = models.CharField(max_length=255, verbose_name="Tel")

    class Meta:
        ordering = ['-Nom']
        verbose_name = "Personne"

    def __str__(self):
        return self.Nom

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
