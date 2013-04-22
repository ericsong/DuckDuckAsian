from django import forms
from auth.models import SherlockUser

from django.forms.fields import DateField
from django.forms.extras.widgets import SelectDateWidget

BIRTH_YEAR_CHOICES = range(1913,2014)

RACE_CHOICES = (
    ('1', 'Asian'),
    ('2', 'White'),
    ('3', 'Black'),
    ('4', 'Hispanic'))

class SherlockUserForm(forms.Form):
    photo = forms.ImageField()

    #user profile info (main)
    race = forms.ChoiceField(choices=RACE_CHOICES)

    # ethnicity = forms.CharField(max_length=255, required=False)
    # nationality = forms.CharField(max_length=255, required=False)
    date_of_birth = DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))

    #user profile info (possiblez) some info that might be fun to play around with in the future
    # mood = forms.CharField(max_length=1024, required=False) #not sure how I want to store this one yet. word descriptions? numerical levels? idk
    # occupation = forms.CharField(max_length=1024, required=False) #this one might actually be kind of fun
    # intelligence = forms.CharField(max_length=1024, required=False) #not sure how to measure this either. degree of education?
    # socialclass = forms.CharField(max_length=1024, required=False) #income levels?
    # attractiveness = forms.IntegerField(required=False) #1-10 i guess
