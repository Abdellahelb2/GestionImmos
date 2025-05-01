from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import BienImmo  

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
        fields = ('username', 'email' , 'status', 'password1', 'password2')


