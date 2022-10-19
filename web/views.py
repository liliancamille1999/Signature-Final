from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from SignatureFinal2022 import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .token import generatorToken
from web.models import entreprise, Personne
from django.contrib.auth import authenticate, login, logout
from myx509.models import DocSign


# Create your views here.

def home(request):
    id = request.user.id
    if id is None:
        return render(request,"Accueil.html")
    else:
        personne = Personne.objects.get(user_id=id)
        Entreprises_id = personne.Entreprise_id
        Entreprises = entreprise.objects.get(id=Entreprises_id)
        Pdf = DocSign.objects.filter(personne=personne)
        nombr=len(Pdf)
        nombre=range(1,nombr)
        print(nombre)
        return render(request, "Accueil.html",
                  {"entreprise": Entreprises, "Personne": personne, "Document": Pdf,"nombre":nombr})


def register(request):
    Entreprises = entreprise.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        entreprises = request.POST['entreprise']
        sexe = request.POST['sexe']
        date = request.POST['date']
        email = request.POST['email']
        tel = request.POST['tel']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request, 'Ce nom est déjà pris')
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, 'Cet email a déjà un compte')
            return redirect('register')

        if not username.isalnum():
            messages.error(request, 'Le nom doit etre alphanumérique')
            return redirect('register')

        if password != password1:
            messages.error(request, 'Les deux mots de passe ne coincident pas')
            return redirect('register')

        # creation de l'utilisateur

        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.is_active = False
        mon_utilisateur.save()
        messages.success(request, 'Votre compte a été crée avec succès')

        # enregistrement de personne
        ct = entreprise.objects.get(NomE=entreprises)
        cr = User.objects.latest('id')
        personne = Personne.objects.create(Nom=firstname, Entreprise=ct, user=cr)
        personne.Nom = firstname
        personne.Prenom = lastname
        personne.email = email
        personne.Entreprise = ct
        personne.Sexe = sexe
        personne.tel = tel
        personne.Date_naissance = date
        personne.user = cr
        personne.save()

        # envoi d'email de bienvenu

        subject = "Bienvenue"
        message = "Bienvenue" + " " + mon_utilisateur.first_name + " " + mon_utilisateur.last_name + "\n Nous sommes heureux de vous compter parmi nous\n\n\n Merci \n\n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # email de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de l'adresse email"
        messageconfirm = render_to_string("emailconfirm.html", {
            "name": mon_utilisateur.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            "token": generatorToken.make_token(mon_utilisateur)
        })
        email = EmailMessage(
            email_subject,
            messageconfirm,
            settings.EMAIL_HOST_USER,
            [mon_utilisateur.email]

        )
        email.fail_silently = False
        email.send()
        return redirect('login')

    return render(request, 'appl/register.html', {"entreprise": Entreprises})


def logIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return redirect('home')
        elif my_user.is_active == False:
            messages.error(request,
                           "Vous n'avez pas confirmé votre adresse email. Faite le avant de vous connecter.Merci!")
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')
    return render(request, 'appl/login.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a bien été activé, félicitation. Connectez-vous maintenant")
        return redirect('login')
    else:
        messages.error(request, 'Activation échouée!!!!!! Réessayez plutard')
        return redirect('home')


def Deconnexion(request):
    logout(request)
    return redirect('home')
