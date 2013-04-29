from django import forms
from UserInfo.race_choices import raceChoices

RACE_CHOICES = RaceChoices.RACE_CHOICES

class AnswerTextForm(forms.Form):
    raw_answer = forms.CharField(max_length=1024)

class AnswerNumberForm(forms.Form):
    raw_answer = forms.IntegerField()

class RaceSelectForm(forms.Form):
    raw_answer = forms.ChoiceField(choices=RACE_CHOICES)
