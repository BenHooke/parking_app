from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.urls import reverse
from .forms import *
from .models import *
from .decorators import *

@login_required(login_url='/login')
def home(request):
    approved_passes = Pass.objects.filter(approved=True).order_by('-created_at')
    unapproved_passes = Pass.objects.filter(approved=False)
    paginator = Paginator(approved_passes, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'approved_passes': approved_passes,
               'unapproved_passes': unapproved_passes,
               'page_obj': page_obj}
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'parking/home.html', context)
    else:
        return redirect(reverse('dashboard', args=[request.user.tenant.pk]))


@login_required(login_url='/login')
def user_dashboard(request,pk):
    tenant = get_object_or_404(Tenant, user_id=pk)
    passes = tenant.pass_set.all().order_by('-created_at')
    paginator = Paginator(passes, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'tenant': tenant, 'passes': passes, 'page_obj': page_obj}
    return render(request, 'parking/user_dashboard.html', context)


@login_required(login_url='/login')
@staff_only
def valid_passes(request):
    now = timezone.now()
    last_24_hours = now - timedelta(hours=24)
        
    passes = Pass.objects.filter(approved=True, created_at__gte=last_24_hours)
    
    context = {'passes': passes}
    return render(request, 'parking/valid_passes.html', context)


@login_required(login_url='/login')
@staff_only
def pass_requests(request):
    if request.method == 'POST':
        pass_id = request.POST.get('pass_id')
        if pass_id:
            parking_pass = get_object_or_404(Pass, id=pass_id)
            if request.user.is_staff:
                parking_pass.approved = True
                parking_pass.save()
        return redirect('requests')
    
    passes = Pass.objects.filter(approved=False)
    context = {'passes': passes}
    return render(request, 'parking/pass_requests.html', context)


@login_required(login_url='/login')
@admin_only
def staff_list(request):
    staff = Staff.objects.all()
        
    if request.method == 'POST':
        staff_ids = [int(key.split('_')[1]) for key in request.POST.keys() if key.startswith('staff_')]
        for staff_id in staff_ids:
            staff_member = Staff.objects.get(id=staff_id)
            staff_member.is_working = True
            staff_member.save()
            
        Staff.objects.exclude(id__in=staff_ids).update(is_working=False) 
                   
        return redirect('/staff_list')
    
    context = {'staff': staff}
    return render(request, 'parking/staff_list.html', context)


@login_required(login_url='/login')
@admin_only
def tenant_list(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            new_tenant = get_object_or_404(Tenant, user_id=user_id)
            if request.user.is_superuser:
                new_tenant.approved = True
                new_tenant.save()
        return redirect('tenant_list')
    
    tenants = Tenant.objects.all()
    tenant_requests = tenants.filter(approved=False).exists
    
    context = {'tenants': tenants, 'tenant_requests': tenant_requests}
    return render(request, 'parking/tenant_list.html', context)


def tentant_signup(request):
    if request.method == 'POST':
        form = TenantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = TenantRegistrationForm()
        
    context = {'form': form}
    return render(request, 'registration/tenant_signup.html', context)


@login_required(login_url='/login')
@admin_only
def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Staff.objects.create(user=user,
                                 name=form.cleaned_data['name'],
                                 phone=form.cleaned_data['phone'],
                                 email=form.cleaned_data['email'])
            return redirect('staff_list')
    else:
        form = StaffRegistrationForm()
        
    context = {'form': form}
    return render(request, 'registration/register_staff.html', context)


def register_building(request):
    if request.method == 'POST':
        form = NewBuildingForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('tenant_list')
    else:
        form = NewBuildingForm()
    
    context = {'form': form}
    return render(request, 'registration/register_building.html', context)


@login_required(login_url='/login')
def request_pass(request, pk):
    tenant = get_object_or_404(Tenant, user_id=pk)
    
    if request.method == 'POST':
        form = PassRequestForm(request.POST)
        if form.is_valid:
            pass_instance = form.save(commit=False)
            pass_instance.user = tenant
            pass_instance.save()
            return redirect('/')
    else:
        form = PassRequestForm()
    
    context = {'form': form, 'tenant': tenant}
    return render(request, 'parking/request_pass.html', context)


@login_required(login_url='/login')
def approval_pending(request):
    return render(request, 'parking/approval_pending.html')


@login_required(login_url='/login')
def profile(request, pk):
    tenant = Tenant.objects.get(user_id=pk)
    
    context = {'tenant': tenant}

    return render(request, 'parking/profile.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')