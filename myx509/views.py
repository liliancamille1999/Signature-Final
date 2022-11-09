import base64
from binascii import Error
from datetime import datetime

import qrcode
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from myx509.Empreinte import DigitalSignature
from myx509.models import DocSign, Cert, VerifSign
from web.models import Personne, entreprise
from .serializers import DocSignSerializers, PersonneSerializers, CertificatSerializers, EntrepriseSerializers, \
    VerifSerializers


class DocList(APIView):

    def get(self, request, format=None):
        snippets = DocSign.objects.all()
        serializer = DocSignSerializers(snippets, many=True)
        return Response(serializer.data)



class verifDetail(APIView):

    def get_object(self, pk):
        try:
            return VerifSign.objects.get(pk=pk)
        except VerifSign.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = VerifSerializers(snippet)
        return Response(serializer.data)


class verifList(APIView):

    def get(self, request, format=None):
        snippets = VerifSign.objects.all()
        serializer = VerifSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        error=""
        data = request.data
        # sign = '1Zazc8T+GBFCXMYq/VHMVETpsKGimbqY1Zb0yEzIZ7V78YwLDzCm/q8tahNm6XHPlJvWpoMB8T/QRynGTxN0AGLwZ9grVBUF75CcuzLr4nX5gEAgJqEHM+VWpWUltqxey0NSLl8HR2n0Ep/Ln2l0ec7MnFhXn9g30w0S9qc/XeYiyLOIhcZXr1ivQIIHagkXSfbIJL/mSWFsWjiCwXJp9iecJAylAsV5SrnGWewUJyfdqJYccIfL+Eh3f68JPy55YC/aXL/kya0bwG4OL3KhODGB7Qo1nrFRgrnlrE/ppTd+mu/5pxbkXJl4nJKsORtsHrA3zTl+5JixJQPYX7aB0Q=='
        sign = data['signature']
        signe = bytes(sign, encoding='utf-8')
        print(signe)
        try:
           signe4 = base64.b64decode(signe)
           fichier = DocSign.objects.filter(id=data['id_doc'])
           fichier2 = DocSign.objects.get(id=data['id_doc'])
           fiche1 = fichier2.media
           doc = fiche1.read()
           file = base64.b64encode(doc)
           test = DigitalSignature.verify(DigitalSignature, data['Cert'], signe4, file)
           note = VerifSign.objects.create(verif=test)
           note.document.set(fichier)
           serializer = VerifSerializers(note, many=False)
           return Response(serializer.data)
        except Error:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class PersonneList(viewsets.ModelViewSet):
    queryset = Personne.objects.all()
    serializer_class = PersonneSerializers


class CaList(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertificatSerializers


class EntrepriseList(viewsets.ModelViewSet):
    queryset = entreprise.objects.all()
    serializer_class = EntrepriseSerializers


def signer(request):
    id_u = request.user.id
    personne = Personne.objects.get(user_id=id_u)
    id_Per = personne.id
    Certificat = Cert.objects.get(personne_id=id_Per)
    id_Cert = Certificat.id
    Entreprises_id = personne.Entreprise_id
    Entreprises = entreprise.objects.get(id=Entreprises_id)
    date = datetime.now()
    if request.method == "POST":
        media = request.FILES['media']
        taille = media.size
        if taille > 50000000:
            messages.error(request, "votre fichier est trop volumineux")
        else:
            file = base64.b64encode(media.read())
            passphrase = request.POST['mot_de_passe']

            signe = DigitalSignature.Sign(DigitalSignature, id_u, passphrase, file)
            if signe == 0:
                Pdf = DocSign.objects.filter(personne=personne)
                message = "votre document n'a pas ete signe"
            else:
                message = "votre document a ete signe"
                DocSign.objects.create(media_nom=media.name, personne=personne, date_signature=date, media=media,
                                       media_signe=media)
                doc = DocSign.objects.latest("id")
                id_doc = doc.id
                signe2 = str(id_doc) + " " + str(id_Cert) + " "
                signe3 = base64.b64encode(signe)
                signe5 = bytes(signe2, encoding="utf-8")
                signe6 = signe5 + signe3
                signe4 = base64.b64decode(signe3)

                print(signe3)
                print(signe4)
                print(signe)
                print(signe2)

                # json.dumps(DATA)
                img = qrcode.make(signe6)

                '''
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10,
                    border=4,
                )
                print(type(qr))
                qr0 = QrCode.encode_text("Bonjour, monde!", QrCode.Ecc.MEDIUM)
                qr.add_data(signe2)
                qr.add_data(signe3)
                qr.make(fit=True)'''

                # img = qr.make_image(fill_color="black", back_color="white")
                c1 = canvas.Canvas('canvas.pdf')
                file = img.get_image()
                b = ImageReader(file)
                # On insére l'image souhaitée dans le fichier précédent à la position souhaitée ('adresseimage.png',
                # x, y)
                c1.drawImage(b, 0, 0, width=87, height=87)

                c1.save()

                # On ouvre le fichier contenant le tamon
                montampon = PdfFileReader(open("canvas.pdf", "rb"))

                # On ouvre le fichier sur lequel le tampon doit être inséré
                output_file = PdfFileWriter()
                fichier = DocSign.objects.latest('id')
                fiche = fichier.media_signe
                fiche1 = fichier.media
                input_file = PdfFileReader(open(fiche1.path, "rb"))

                # On récupère le nombre de pages du fichier
                page_count = input_file.getNumPages()

                # On ajoute à chaque page le tampon avec une boucle pour
                for page_number in range(page_count):
                    input_page = input_file.getPage(page_number)
                    input_page.mergePage(montampon.getPage(0))
                    output_file.addPage(input_page)

                with open(fiche.path, "wb") as OutputStream:
                    output_file.write(OutputStream)

                Pdf = DocSign.objects.filter(personne=personne)
                # test1=createVerif(createVerif,21,1)
                # print(test1)
    return render(request, 'Accueil.html',
                  {'message': message, 'Document': Pdf, 'Personne': personne, 'entreprise': Entreprises})
