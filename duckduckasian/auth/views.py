from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from auth.forms import RegistrationForm
from auth.models import SherlockUser

def login_user(request):
    if request.user.is_authenticated():
        return render(request, 'home.html', {'user': request.user})

    state = "Please log in below..."
    username = password = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return render(request, 'home.html', {'user': user})
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render(request, 'login.html', {'state': state, 'username': username})

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')

@login_required(login_url="/login/")
def homepage(request):
    return render(request, 'home.html', {'user': request.user})



def register_user(request):
    state = "Please fill in all of the blanks below..."
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():#add user existing check, password same check
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            new_user = User.objects.create_user(username, email, password)
            new_s_user = SherlockUser.objects.create_SherlockUser(new_user) 
            new_user.save()
            new_s_user.save()

            user = authenticate(username=username, password=password)
            login(request, user)            
            return HttpResponseRedirect('/home/')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {
        'form': form,
    })
