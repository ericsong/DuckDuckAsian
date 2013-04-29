from django import forms

class AnswerTextForm(forms.Form):
    raw_answer = forms.CharField(max_length=1024)

class AnswerNumberForm(forms.Form):
    raw_answer = forms.IntegerField()
