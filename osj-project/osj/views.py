from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from osj.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from pages.views import getUserContext


def registration(request):
    #https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('afterRegistration')
    else:
        form = RegistrationForm()
    context = {'form': form}
    if request.user.is_authenticated:
        # this is unlikley to happen
        context.update(getUserContext(request))
    return render(request, 'registration/registration.html', context)

@login_required
def afterRegistration(request):
    user = request.user
    context = {'user': user}
    context.update(getUserContext(request))
    return render(request, 'registration/afterRegistration.html', context)
        

