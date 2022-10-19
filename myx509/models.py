from django.contrib.auth.models import User
from django.db import models
from django_x509.base.models import AbstractCa, AbstractCert
from web.models import Personne


class DetailsModel(models.Model):
    details = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        abstract = True


class Ca(DetailsModel, AbstractCa):
    """
    Concrete Ca model
    """

    class Meta(AbstractCa.Meta):
        abstract = False


class Cert(DetailsModel, AbstractCert):
    """
    Concrete Cert model
    """
    personne = models.OneToOneField(Personne, on_delete=models.SET_NULL, null=True, verbose_name='personne')

    class Meta(AbstractCert.Meta):
        abstract = False


class DocSign(models.Model):
    media_nom = models.CharField(max_length=256, verbose_name="nom_du_fichier")
    media = models.FileField(upload_to="Fichiers signes", verbose_name="fichier a signer")
    date_signature = models.CharField(max_length=256, verbose_name="date")
    personne = models.ForeignKey(Personne, on_delete=models.SET_NULL, null=True, verbose_name='personne')
    media_signe = models.FileField(upload_to="DocumentSign", verbose_name="Document deja signes")

    class Meta:
        ordering = ['-date_signature']
        verbose_name = "date_signature"

    def __str__(self):
        return self.media_nom


class VerifSign(models.Model):
    document = models.ManyToManyField(DocSign, verbose_name='document')
    verif = models.CharField(max_length=256, verbose_name="resultat")
