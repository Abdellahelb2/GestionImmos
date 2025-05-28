from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.contrib.auth import login as loginuser, logout as logoutuser, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser,client,entrepreneur,BienImmo,Reservation,Message,Favoris
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm,BienImmoForm,ReservationForm,MessageForm,CustomUserChangeForm,checkForm,UserStatusForm
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

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

def logout(request):
        logoutuser(request)
        messages.info(request, "🔵 You have been logged out!")
        return redirect('SayHello')

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
                return redirect('SayHello') 
            else:
                messages.error(request, "❌ Invalid username or password!")
                return redirect('SayHello')
        return render(request, 'registration/login.html')


def product_detail(request, id):
    bien = get_object_or_404(BienImmo, id=id)
    is_favoris = request.user.is_authenticated and Favoris.objects.filter(user=request.user, bien=bien).exists()
    form = ReservationForm(request.POST or None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Vous devez être connecté pour réserver.')
            form.add_error(None, 'Vous devez être connecté pour réserver.')
        elif form.is_valid():
            try:
                locataire = client.objects.get(user=request.user)
                reservation = form.save(commit=False)
                reservation.client = locataire
                reservation.bien = bien
                slot_taken = Reservation.objects.filter(
                    bien=bien,
                    reservation_date=reservation.reservation_date,
                    reservation_time=reservation.reservation_time,
                    status='acceptee'
                ).exists()

                if slot_taken:
                    form.add_error('reservation_time', 'Ce créneau est déjà réservé pour ce logement.')
                    messages.error(request, 'Erreur : ce créneau est déjà pris.')
                else:
                    try:
                        reservation.full_clean()
                        reservation.save()
                        messages.success(request, "Demande de reservation en cours de traitement")
                        return redirect('Product', id=bien.id)
                    except ValidationError:
                        form.add_error('reservation_time', 'Erreur de validation des données.')
                        messages.error(request, 'Erreur : ce créneau est invalide.')
            except client.DoesNotExist:
                form.add_error(None, 'Vous devez être un locataire pour effectuer une réservation.')
                messages.error(request, 'Erreur: Vous devez être un locataire pour réserver.')
        else:
            messages.error(request, 'Erreur: Veuillez corriger les erreurs ci-dessus.')

    return render(request, 'products/product.html', {
        'x': bien,
        'form': form,
        'is_favoris': is_favoris,
    })

class BienUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BienImmo
    fields = ['name', 'type', 'price', 'content', 'address', 'image1', 'image2', 'image3', 'image4', 'image5']
    success_url = reverse_lazy('Products')
    def test_func(self):
        bien = self.get_object()
        user = self.request.user
        if user.status == 'admin':
            return True
        try:
            ent = entrepreneur.objects.get(user=user)
            return bien.user == ent
        except entrepreneur.DoesNotExist:
            return False
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
class BienDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BienImmo
    success_url = '/product/'  

    def test_func(self):
        bien = self.get_object()
        return self.request.user.status == 'admin' or bien.user.user == self.request.user
    
@login_required(login_url='/login/')
def add_product(request):
    if request.user.status == 'client':
        messages.error(request, "❌ Tu n'as pas le droit d'ajouter un produit ici.")
        return redirect('SayHello')

    entrepreneur_instance, created = entrepreneur.objects.get_or_create(user=request.user)
    if not entrepreneur_instance.is_profile_complete():
        messages.warning(request, "⚠️ Veuillez compléter votre profil avant d’ajouter un produit.")
        return redirect('SayHello') 

    if request.method == 'POST':
        form = BienImmoForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = entrepreneur_instance
            product.save()
            messages.success(request, "✅ Annonce en cours de taitement !")
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
@login_required
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
    user_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    user_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'messaging/inbox.html', {'messages': user_messages})


def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_message_count': count}
    return {}

@staff_member_required(login_url='/login/')  
def dash(request):
    biens = BienImmo.objects.all() 
    check_forms = {bien.id: checkForm(instance=bien) for bien in biens}
    users = CustomUser.objects.all() 
    clients = client.objects.all()   
    entrepreneurs = entrepreneur.objects.all() 
    reservations = Reservation.objects.all()
    

    
    return render(request, 'adminp/dash.html', {
        'biens': biens,
        'users': users,
        'check_forms': check_forms,
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
    return redirect('Product', id=bien.id)
  

@login_required
def remove_from_favoris(request, bien_id):
    bien = get_object_or_404(BienImmo, id=bien_id)
    Favoris.objects.filter(user=request.user, bien=bien).delete()
    messages.success(request, "🗑️ Supprimé des favoris.")
    return redirect('Product', id=bien.id)


@login_required
def traiter_reservation(request, reservation_id, action):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user != reservation.bien.user.user:
        return HttpResponseForbidden()
    
    if action == 'accepter':
        reservation.status = 'acceptee'
        reservation.save()
    
    elif action == 'refuser':
        
        reservation.delete()
    
    elif action == 'annuler':
    
        reservation.delete()
    
    else:
        return HttpResponseForbidden()
    
    return redirect('dashboard_entrepreneur')

@login_required
def dashboard_entrepreneur(request):
    try:
        entrepreneur_instance = entrepreneur.objects.get(user=request.user)
    except entrepreneur.DoesNotExist:
        messages.error(request, "🚫 Vous n'êtes pas un entrepreneur.")
        return redirect('SayHello')

    biens = BienImmo.objects.filter(user=entrepreneur_instance).order_by('-id')
    reservations = Reservation.objects.filter(bien__in=biens).order_by('-reservation_date')
    check_forms = {bien.id: checkForm(instance=bien) for bien in biens}

    return render(request, 'adminp/dashboard_entrepreneur.html', {
        'reservations': reservations,
        'biens': biens,
        'check_forms': check_forms,
    })



@login_required(login_url='/login/')
def my_favoris(request):
    favoris_list = Favoris.objects.filter(user=request.user).select_related('bien')
    return render(request, 'registration/mesfav.html', {'favoris_list': favoris_list})



@login_required
def mes_notifications(request):
    notifications = request.user.notifications.all().order_by('-timestamp')
    return render(request, 'base.html', {'notifications': notifications})


@login_required
def update_bien_status(request, id):
    bien = get_object_or_404(BienImmo, id=id)
    is_admin = request.user.is_superuser
    is_owner = False
    try:
        current_entrepreneur = entrepreneur.objects.get(user=request.user)
        is_owner = bien.user == current_entrepreneur
    except entrepreneur.DoesNotExist:
        pass

    if not (is_admin or is_owner):
        return HttpResponseForbidden("🚫 Vous n'avez pas la permission de modifier ce bien.")

    if request.method == 'POST':
        form = checkForm(request.POST, instance=bien)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Statut du bien mis à jour.")
           
            return redirect('dashboard_entrepreneur' if not is_admin else 'Dashboard')  
    else:
        form = checkForm(instance=bien)
    return render(request, 'adminp/dash.html', {'form': form, 'bien': bien})


@login_required
def activer_bien(request, id):
    bien = get_object_or_404(BienImmo, id=id)

    is_admin = request.user.is_superuser
    try:
        current_entrepreneur = entrepreneur.objects.get(user=request.user)
        is_owner = bien.user == current_entrepreneur
    except Entrepreneur.DoesNotExist:
        is_owner = False

    if not (is_admin or is_owner):
        return HttpResponseForbidden("🚫 Vous n'avez pas la permission de modifier ce bien.")

    if not bien.active:
        bien.active = True
        bien.save()
        messages.success(request, "✅ Le bien est maintenant marqué comme disponible.")
    else:
        messages.info(request, "ℹ️ Le bien est déjà disponible.")

    return redirect('Dashboard' if is_admin else 'dashboard_entrepreneur')



@staff_member_required(login_url='/login/')  
def update_user_status(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserStatusForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Dashboard')
    else:
        form = UserStatusForm(instance=user)
    
    return render(request, 'registration/update_user_status.html', {'form': form, 'user': user})