from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from billman.authmanager.views import _login, _logout
from billman.services_crud.models import CustomerDetails
from billman.services_crud.formatters import decimal_to_brz
from billman.services_crud.forms import ProfileForm


# def _get_session_email_as_username(request):
#     session_id = request.session.session_key
#     session = Session.objects.get(session_key=session_id)
#     uid = session.get_decoded().get('_auth_user_id')
#     username = get_user_model().objects.get(pk=uid).email
#     return username



def public_home(request):
    return render(request, 'core/public_home.html')


def private_home(request):
    if request.user.is_authenticated:
        total = 0
        if CustomerDetails.objects.filter(email=request.user).exists() and CustomerDetails.objects.get(email=request.user).services.all().exists():
            user_services_queryset = CustomerDetails.objects.get(email=request.user).services.all()
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

        return render(request, 'core/private_home.html', {'user_services': user_services, 'user_empty_services': user_empty_services, 'total': total})
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
        if request.method == 'POST':
            print(request.POST)
            profile_form = ProfileForm(request.POST)
            if profile_form.is_valid():
                profile_form.save()
                profile_form = ProfileForm(instance=CustomerDetails.objects.get(email=request.user))
                return render(request, 'core/profile.html', {'profile_form': profile_form, 'status_message': 'Cadastro atualizado.'})
            else:
                print('erros: {}'.format(profile_form.errors))
                try:
                    profile_form = ProfileForm(instance=CustomerDetails.objects.get(email=request.user))
                except ObjectDoesNotExist:
                    profile_form = ProfileForm()
                finally:
                    return render(request, 'core/profile.html', {'profile_form': profile_form, 'errors': profile_form.errors})
        else:
            try:
                profile_form = ProfileForm(instance=CustomerDetails.objects.get(email=request.user))
            except ObjectDoesNotExist:
                profile_form = ProfileForm(instance=CustomerDetails.objects.create(email=request.user))
            finally:
                return render(request, 'core/profile.html', {'profile_form': profile_form})
    else:
        return render(request, 'core/login.html', {'status_message': 'Você não está logado. Faça o login primeiro.'})
