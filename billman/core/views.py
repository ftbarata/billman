from django.shortcuts import render, redirect
from billman.authmanager.views import _login, _logout
from billman.services_crud.models import CustomerDetails, Service
from billman.services_crud.formatters import decimal_to_brz
from billman.services_crud.forms import ProfileForm
from .models import Contacts
from billman.billing_control.models import BillingHistory
from billman.authmanager.models import User
from django.conf import settings

def public_home(request):
    return render(request, 'core/public_home.html')


def private_home(request):
    if request.user.is_authenticated:
        if BillingHistory.objects.all().filter(customer__email=request.user).exists():
            billing_history = BillingHistory.objects.all().filter(customer__email=request.user)
        else:
            billing_history = None

        total = 0
        if CustomerDetails.objects.filter(email=request.user).exists() and Service.objects.filter(customer__email=request.user).exists():
            user_services_queryset = Service.objects.all().filter(customer__email=request.user)
            user_services = []
            total = 0
            for i in user_services_queryset:
                description = i.description
                count = i.count
                unit_price = decimal_to_brz(i.unit_price)
                user_services.append({'description':description, 'count':count, 'unit_price':unit_price, 'subtotal': decimal_to_brz(unit_price * count)})
                total += unit_price * count

            if user_services_queryset.count() == 0:
                user_empty_services = True
            else:
                user_empty_services = False
        else:
            user_empty_services = True
            user_services = []

        return render(request, 'core/private_home.html', {'user_services': user_services, 'user_empty_services': user_empty_services, 'total': total, 'billing_history': billing_history})
    else:
        return render(request, 'core/login.html', {'status_message': 'Você não está logado. Faça o login primeiro.'})


def login(request):
    if request.method == 'POST':
        if request.method == 'POST':
            if _login(request):
                return redirect('private-home')
            else:
                context = {'status_message': 'Acesso negado. Verifique seu login e senha.'}
                return render(request, 'core/login.html', context)

    else:
        return render(request, 'core/login.html')


def logout(request):
    _logout(request)
    context = {'status_message': 'Você foi deslogado.'}
    return render(request, 'core/public_home.html', context)


def profile_view(request):
    if request.user.is_authenticated:
        try:
            instance = CustomerDetails.objects.get(email=request.user)
        except CustomerDetails.DoesNotExist:
            instance = None

        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=instance)
            if profile_form.is_valid():
                profile_form.save()
                return render(request, 'core/profile_updated_success.html')
        else:
            profile_form = ProfileForm(instance=instance, initial={'email': request.user})
        return render(request, 'core/profile.html', {'profile_form': profile_form})
    else:
        return render(request, 'core/login.html', {'status_message': 'Você não está logado. Faça o login primeiro.'})


def contacts_view(request):
    if request.user.is_authenticated:
        try:
            contact_text = []
            for user in User.objects.all().filter(groups__name=settings.ADMINS_GROUP_NAME):
                contact_text.append((user.email, Contacts.objects.get(email=user.email).contacts))
        except Contacts.DoesNotExist:
            contact_text = None
        finally:
            print(contact_text)
            return render(request, 'core/contacts.html', {'contact_text': contact_text})
    else:
        return render(request, 'core/login.html', {'status_message': 'Você não está logado. Faça o login primeiro.'})
