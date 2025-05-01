from django.db import models
from django.contrib.auth.models import AbstractUser 

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
    name = models.CharField(max_length=50, default='nouvelle apartement')
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




    