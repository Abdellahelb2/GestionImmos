from django.db import models
from django.contrib.auth.models import AbstractUser  # type: ignore
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime

# Create your models here.
class CustomUser(AbstractUser):
    status = [
        ('entrepreneur', 'entrepreneur'), 
        ('client', ' client'),
        ('admin','admin'),
        ('visiteur','visiteur')
    ]
    status = models.CharField(max_length=50, default='visiteur', choices=status)
    profile_picture = models.ImageField(upload_to='locataire_profile_pics/',default='locataire_profile_pics/car-rental-vector-13423582.png', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    Carteid= models.CharField(max_length=100, null=True, blank=True)
  

class entrepreneur(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,primary_key=True)  
    entreprise=models.CharField(max_length=50, default='x')

class BienImmo(models.Model):
    x = [
        ('a vendre', 'a vendre'), 
        ('a louer', 'a louer')
    ]
    name = models.CharField(max_length=200, default='nouvelle apartement')
    type = models.CharField(max_length=50, null=True, blank=True, choices=x)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    content = models.TextField()
    address = models.CharField(max_length=255, default='') 
    image1 = models.ImageField(upload_to='photos/%y/%m/%d', default='photos/25/04/25/pfp.jpg')
    image2 = models.ImageField(upload_to='photos/%y/%m/%d', default='photos/25/04/25/pfp.jpg')
    image3 = models.ImageField(upload_to='photos/%y/%m/%d', default='photos/25/04/25/pfp.jpg')
    image4 = models.ImageField(upload_to='photos/%y/%m/%d', default='photos/25/04/25/pfp.jpg')
    image5 = models.ImageField(upload_to='photos/%y/%m/%d', default='photos/25/04/25/pfp.jpg')
    user = models.ForeignKey(entrepreneur,on_delete=models.CASCADE)   
    
    active = models.BooleanField(default=True)

    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['price']


class client(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,primary_key=True)   
    bio = models.TextField(null=True, blank=True)


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    bien = models.ForeignKey(BienImmo, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='en_attente')

    def __str__(self):
        return f"{self.client.user.username} reserved {self.bien.name} on {self.reservation_date} at {self.reservation_time}"

    import datetime

def clean(self):
    if self.reservation_date < datetime.date.today():
        raise ValidationError("Vous ne pouvez pas réserver pour une date passée.")
    
    reservations_count = Reservation.objects.filter(
        client=self.client,
        reservation_date=self.reservation_date
    ).exclude(pk=self.pk).count()

    if reservations_count >= 3:
        raise ValidationError("Vous ne pouvez pas réserver plus de 3 fois par jour.")



class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    bien = models.ForeignKey(BienImmo, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"



class Favoris(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    bien = models.ForeignKey(BienImmo, on_delete=models.CASCADE, related_name='favori_par')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'bien')
        verbose_name_plural = "Favoris"

    def __str__(self):
        return f"{self.user.username} ❤️ {self.bien.name}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"
