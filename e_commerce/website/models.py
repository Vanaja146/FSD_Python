from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token   

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')

    def _str_(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):   # fixed typo
        return f"Review for {self.product.name} - {self.rating} stars"
@receiver(post_save, sender='website.AuthUser')
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class AuthUser(AbstractUser):
    #Inherits all the fields and methods from AbstractUser
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=150,unique=True)
    user_permissions=None
    groups=None
    first_name=None
    last_name=None
    
    def __str__(self):
        return self.email