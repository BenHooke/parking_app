from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class TenantRegistrationForm(forms.ModelForm):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), required=True)
    
    class Meta:
        model = Tenant
        fields = ['first_name', 'last_name', 'phone', 'email', 'building', 'unit']

    username = forms.CharField(max_length=200, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        tenant = super().save(commit=False)
        tenant.user = user
        if commit:
            tenant.save()
        return tenant


class StaffRegistrationForm(UserCreationForm):
    name = forms.CharField(required=True, max_length=200)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, max_length=200)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
    
class PassRequestForm(forms.ModelForm):
    class Meta:
        model = Pass
        fields = '__all__'
        exclude = ['user', 'approved']
        
        
class StaffWorkingNowForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['is_working']
        
        
class NewBuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'