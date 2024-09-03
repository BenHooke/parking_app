from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.address


class Tenant(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, primary_key=True) # add primary_key=True when you figure it out
    first_name = models.CharField(max_length=200, null= True)
    last_name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null= True)
    email = models.EmailField(null= True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null= True, blank= True)
    unit = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    
class Staff(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null= True)
    email = models.EmailField(max_length=200, null= True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_working = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.user:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username
    
    
class Pass(models.Model):
    user = models.ForeignKey(Tenant, null=True, on_delete=models.CASCADE)
    make = models.CharField(max_length=200, null=True)
    model = models.CharField(max_length=200, null=True)
    plate = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    approved = models.BooleanField(default=False)
    
    
    