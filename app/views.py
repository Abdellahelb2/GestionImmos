from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import login as loginuser, logout as logoutuser, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser,client,entrepreneur,BienImmo,Reservation,Message  
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm,BienImmoForm,ReservationForm,MessageForm,CustomUserChangeForm
from django.contrib.admin.views.decorators import staff_member_required

    # Pages
def SayHello(request):
        x = {
            'name': 'taha',
            'age': '25574546545454545451',
            'job': 'teacher'
        }
        return render(request, 'pages/index.html', x)

def Settings(request):
        return render(request, 'pages/about.html')

def Said(request):
        return render(request, 'pages/Services.html')



    # contact Views
def Con(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            full_message = f"Message from {name} <{email}>:\n\n{message}"

            try:
                send_mail(
                    subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')  
            except Exception as e:
                messages.error(request, 'An error occurred while sending the message.')

        return render(request, 'pages/Contact.html')
def main(request):
        return render(request, 'pages/main.html')
def logout(request):
        logoutuser(request)
        messages.info(request, "🔵 You have been logged out!")
        return redirect('main')

def Register(request):
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save() 
                login(request, user) 
                messages.success(request, "✅ Account created and logged in!")
                return redirect('SayHello') 
            else:
                messages.error(request, form.errors)
        else:
            form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {"form": form})


def Loginpage(request):
        if request.method == 'POST':
            username = request.POST.get('username')  
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                loginuser(request, user)
                messages.success(request, "🟢 You are now logged in!")
                return redirect('main') 
            else:
                messages.error(request, "❌ Invalid username or password!")
                return redirect('main')
        return render(request, 'registration/login.html')

def product_detail(request, id):
    bien = get_object_or_404(BienImmo, id=id)
    is_favoris = False
    if request.user.is_authenticated:
        is_favoris = Favoris.objects.filter(user=request.user, bien=bien).exists()

    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']

            if Reservation.objects.filter(bien=bien, reservation_date=reservation_date).exists():
                form.add_error('reservation_date', 'Cette date est déjà réservée pour ce logement.')
                messages.error(request, 'La date sélectionnée est déjà réservée.')
            else:
                if request.user.is_authenticated:
                    try:
                        locataire = client.objects.get(user=request.user)
                        reservation = form.save(commit=False)
                        reservation.client = locataire
                        reservation.bien = bien
                        reservation.save()
                        messages.success(request, "Réservation effectuée avec succès.")
                        return redirect('Product', id=bien.id)
                    except client.DoesNotExist:
                        form.add_error(None, 'Vous devez être un locataire pour effectuer une réservation.')
                        messages.error(request, 'Erreur: Vous devez être un locataire pour réserver.')
                else:
                    form.add_error(None, 'Vous devez être connecté en tant que locataire pour réserver.')
                    messages.error(request, 'Erreur: Vous devez être connecté pour réserver.')
        else:
            messages.error(request, 'Erreur: Veuillez corriger les erreurs ci-dessus.')
    else:
        form = ReservationForm()

    return render(request, 'products/product.html', {
        'x': bien,
        'form': form,
        'is_favoris': is_favoris
    })

def product_list(request):
    try:
        all_users = CustomUser.objects.all()
    except CustomUser.DoesNotExist:
        raise Http404("Locataire not found")

    type_filter = request.GET.get('type')

    if type_filter in ['a vendre', 'a louer']:
        house = BienImmo.objects.filter(type=type_filter)
    else:
        house = BienImmo.objects.all()

    q = request.GET.get('q')
    if q:
        house = house.filter(name__icontains=q)
    return render(request, 'products/products.html', {
        'house': house,
        'locataire': all_users,
    })

@login_required(login_url='/login/')
def add_product(request):
    if request.user.status == 'client':
        messages.error(request, "❌ Tu n'as pas de droit d'ajouter un produit ici")
        return redirect('main')
    entrepreneur_instance, created = entrepreneur.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BienImmoForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = entrepreneur_instance
            product.save()
            messages.success(request, "✅ Produit ajouté !")
            return redirect('Products')
        else:
            messages.error(request, "⚠️ Erreur lors de la soumission du formulaire.")
    else:
        form = BienImmoForm()

    return render(request, 'products/add_product.html', {'form': form})
    
@login_required
def modify_profile(request):
        user = request.user

   
        profile_model = entrepreneur
       
        profile_model = client
     

        try:
            profile_instance = profile_model.objects.get(user=user)
        except profile_model.DoesNotExist:
            profile_instance = profile_model(user=user)
            profile_instance.save()

        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Profile updated successfully!")
                return redirect('profile')
            else:
                messages.error(request, "⚠️ Please fix the errors in the form.")
        else:
            form = CustomUserChangeForm(instance=user)

        return render(request, 'registration/modify_profile.html', {'form': form})

def profile(request):
        user = request.user
        role_data = None

        if user.status == 'entrepreneur':
            role_data = entrepreneur.objects.filter(user=user).first()
        elif user.status == 'client':
            role_data = client.objects.filter(user=user).first()

        return render(request, 'registration/profile.html', {
            'user': user,
            'role_data': role_data
        })

@login_required
def conversation(request, bien_id, recipient_id):
    bien = get_object_or_404(BienImmo, id=bien_id)
    recipient = get_object_or_404(CustomUser, id=recipient_id)
    
    messages_qs = Message.objects.filter(
        bien=bien,
        sender__in=[request.user, recipient],
        recipient__in=[request.user, recipient]
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.bien = bien
            msg.save()
            return redirect('conversation', bien_id=bien.id, recipient_id=recipient.id)
    else:
        form = MessageForm()

    return render(request, 'messaging/conversation.html', {
        'messages': messages_qs,
        'form': form,
        'recipient': recipient,
        'bien': bien,
    })

@login_required
def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages_received})


@staff_member_required(login_url='/login/')  
def dash(request):
    users = CustomUser.objects.all() 
    clients = client.objects.all()   
    entrepreneurs = entrepreneur.objects.all() 
    reservations = Reservation.objects.all()

    
    return render(request, 'adminp/dash.html', {
        'users': users,
        'clients': clients,
        'entrepreneurs': entrepreneurs,
        'reservations':reservations,
    })

@login_required
def add_to_favoris(request, bien_id):
    bien = get_object_or_404(BienImmo, id=bien_id)
    favoris, created = Favoris.objects.get_or_create(user=request.user, bien=bien)
    if created:
        messages.success(request, "✅ Ajouté aux favoris !")
    else:
        messages.info(request, "ℹ️ Déjà dans vos favoris.")
    return redirect('Product', id=bien.id)
  

@login_required
def remove_from_favoris(request, bien_id):
    bien = get_object_or_404(BienImmo, id=bien_id)
    Favoris.objects.filter(user=request.user, bien=bien).delete()
    messages.success(request, "🗑️ Supprimé des favoris.")
    return redirect('Product', id=bien.id)


@login_required(login_url='/login/')
def my_favoris(request):
    favoris_list = Favoris.objects.filter(user=request.user).select_related('bien')
    return render(request, 'registration/mesfav.html', {'favoris_list': favoris_list})