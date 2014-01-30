from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auth.models import DDAUser
from UserInfo.forms import DDAUserForm

from datetime import date

@login_required(login_url="/login/")
def ViewUserInfo(request):
    s_user = DDAUser.objects.get(user=request.user)
    if(s_user.race is None):
        state = "You haven't uploaded any info yet. Please follow the link to do so."
        return render(request, 'ViewUserInfo_None.html', {'user': request.user, 'state': state})
    else:
        state = "Here's your info."
        age = calculate_age(s_user.date_of_birth)
        return render(request, 'ViewUserInfo.html', {'user': request.user, 's_user': s_user, 'age': age})

@login_required(login_url="/login/")
def UploadInfo(request):
    if request.method == 'POST':
        form = DDAUserForm(request.POST, request.FILES)
        if form.is_valid():
            s_user = DDAUser.objects.get(user=request.user)
            s_user.photo = form.cleaned_data['photo']
            s_user.race = form.cleaned_data['race']
            s_user.date_of_birth = form.cleaned_data['date_of_birth']

            '''
            #optional data
            if(form.cleaned_data['ethnicity'] is not None):
                s_user.ethnicity = form.cleaned_data['ethnicity']

            if(form.cleaned_data['nationality'] is not None):
                s_user.ethncitiy = form.cleaned_data['nationality']

            if(form.cleaned_data['mood'] is not None):
                s_user.mood = form.cleaned_data['mood']

            if(form.cleaned_data['occupation'] is not None):
                s_user.occupation = form.cleaned_data['occupation']

            if(form.cleaned_data['intelligence'] is not None):
                s_user.intelligence = form.cleaned_data['intelligence']

            if(form.cleaned_data['socialclass'] is not None):
                s_user.socialclass = form.cleaned_data['socialclass']

            if(form.cleaned_data['attractiveness'] is not None):
                s_user.attractiveness = form.cleaned_data['attractiveness']
            '''
            s_user.save()
            return HttpResponseRedirect('/home/')
    else:
        form = DDAUserForm()

    return render(request, 'UploadInfo.html', {
        'form': form,
    })

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year 
