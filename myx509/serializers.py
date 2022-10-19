from rest_framework.serializers import ModelSerializer
from .models import DocSign, Personne, Ca, Cert, VerifSign
from web.models import entreprise


class PersonneSerializers(ModelSerializer):
    class Meta:
        model = Personne
        fields = ['id', 'Nom', 'Prenom', 'Entreprise']


class VerifSerializers(ModelSerializer):
    class Meta:
        model = VerifSign
        fields = '__all__'


class CertificatSerializers(ModelSerializer):
    class Meta:
        model = Cert
        fields = ['id', 'personne', 'certificate']


class DocSignSerializers(ModelSerializer):
    class Meta:
        model = DocSign
        fields = ['id', 'personne', 'media']


class EntrepriseSerializers(ModelSerializer):
    class Meta:
        model = entreprise
        fields = ['id', 'NomE']
