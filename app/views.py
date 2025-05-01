from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import login as loginuser, logout as logoutuser, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser,client,entrepreneur,BienImmo
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm,BienImmoForm

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


def product_detail(request,id):
    print(id)
    item=BienImmo.objects.get(id=id)
    return render(request,'products/product.html',{'x':item})
 
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

    return render(request, 'products/products.html', {
        'house': house,
        'locataire': all_users 
    })


def dash(request):
    return render(request, 'adminp/dash.html')

@login_required(login_url='/login/')
def add_product(request):
    if request.user.status != 'entrepreneur':
        messages.error(request, "❌ Tu n'as pas de droit d'ajouter un produit ici")
        return redirect('main')
    try:
        entrepreneur_instance = entrepreneur.objects.get(user=request.user)
    except entrepreneur.DoesNotExist:
        messages.error(request, "⚠️ Complete ton profile avant de poster une annonce")
        return redirect('profile')  

    if request.method == 'POST':
        form = BienImmoForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = entrepreneur_instance  
            product.save()
            messages.success(request, "✅ Product Ajouter!")
            return redirect('Products')
        else:
            messages.error(request, "⚠️ Erreur")
    else:
        form = BienImmoForm()

    return render(request, 'products/add_product.html', {'form': form})
   
@login_required
def modify_profile(request):
    user = request.user

    if user.status == 'entrepreneur':
        profile_model = entrepreneur
    elif user.status == 'client':
        profile_model = client
    else:
        messages.error(request, "⚠️ Only clients or entrepreneurs can modify their profile.")
        return redirect('profile')

    try:
        profile_instance = profile_model.objects.get(user=user)
    except profile_model.DoesNotExist:
        profile_instance = profile_model(user=user)
        profile_instance.save()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "⚠️ Please fix the errors in the form.")
    else:
        form = CustomUserCreationForm(instance=user)

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
