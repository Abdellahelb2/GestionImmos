from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import BienImmo,Message,CustomUser ,Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

class BienImmoForm(forms.ModelForm):
    class Meta:
        model = BienImmo
        fields = [
            'name', 
            'type', 
            'price',
            'content',
            'address', 
            'image1', 
            'image2', 
            'image3', 
            'image4', 
            'image5',
            'active'
           
        ]


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder' : 'Entrez votre username'})
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={'placeholder' : 'Entrez votre adresse email'})
    )
    STATUS_CHOICES = [
    ('entrepreneur', 'Entrepreneur'), 
    ('client', 'Client'),
]

    status = forms.ChoiceField(
    choices=STATUS_CHOICES,
    label="Statut",
    widget=forms.Select(attrs={'placeholder': 'Choisissez votre statut'})
)
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
        'placeholder' : 'Entrez votre mot de passe',
    }))
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
        'placeholder' : 'Entrez votre mot de passe'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'status', 'phone_number', 'profile_picture', 'date_of_birth', 'address', 'Carteid')


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'status',
            'phone_number',
            'profile_picture',
            'date_of_birth',
            'address',
            'Carteid'
        )
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Entrez votre email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Entrez votre numéro'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.TextInput(attrs={'placeholder': 'Entrez votre adresse'}),
            'Carteid': forms.TextInput(attrs={'placeholder': 'Numéro de carte ID'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Écrivez votre message...'})
        }