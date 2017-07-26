from django.contrib.auth import authenticate, login, logout


def _login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False
    else:
        return False


def _logout(request):
    request.session.flush()
    logout(request)
    return True

