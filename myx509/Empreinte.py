import OpenSSL
from OpenSSL import crypto
from myx509.models import Cert
from web.models import Personne


class DigitalSignature:
    """
            Class with two static methods that sign or validate a file.
        """

    def Sign(self, id_p, pas, dat):
        """
                """
        personne = Personne.objects.get(user_id=id_p)
        id_Per = personne.id
        Certificat = Cert.objects.get(personne_id=id_Per)
        Privee = Certificat.private_key
        pass1 = Certificat.passphrase
        password = bytes(pas, encoding="utf-8")
        if pass1 == pas:
            Private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, Privee, password)
            sign = OpenSSL.crypto.sign(Private_key, dat, "sha256")
        else:
            sign = 0
        return sign

    def verify(self, id_p, sign, dat):
        personne = Personne.objects.get(user_id=id_p)
        id_Per = personne.id
        Certificat = Cert.objects.get(personne_id=id_Per)
        Certificat_P = Certificat.certificate
        Certificat_en_claire = crypto.load_certificate(crypto.FILETYPE_PEM, Certificat_P)
        try:
            if crypto.verify(Certificat_en_claire, sign, dat, "sha256") is None:
                verify = 1
        except OpenSSL.crypto.Error:
            verify = 0
        return verify