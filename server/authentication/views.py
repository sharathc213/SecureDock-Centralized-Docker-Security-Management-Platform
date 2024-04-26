from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.conf import settings

def signin(request):
    if request.method == 'POST':
        # try:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            remember_me = request.POST.get('rememberme')  # Get the "Remember Me" checkbox value
            print(remember_me)
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_superuser:
                login(request,user)
                messages.success(request,'Login successful')
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires on browser close
                else:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # Session expires in 2 weeks

                return redirect('dashboard/')
            else:
                messages.error(request, 'Invalid username or password') 
        else:
            messages.error(request, 'Invalid details')
            return redirect(reverse('signin'))
        # except Ratelimited:
        #     messages.error(request, 'Rate limit exceeded. Please try again later.')
    else:
        form = AuthenticationForm(request)
    if request.user.is_authenticated and request.user.is_superuser:
        messages.success(request, 'User Already Authenticated')
        return redirect('dashboard/')
    return render(request, 'login.html', {'form': form, "is_admin": True})


def signout(request):
    logout(request)
    return redirect('signin')