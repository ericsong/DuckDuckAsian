from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from DDAGame.models import Answer as Answer_model
from auth.models import DDAUser as DDAUser_model

@login_required(login_url="/login/")
def ViewUserStats(request):
    s_user = DDAUser_model.objects.get(user=request.user) 
    user_answers = Answer_model.objects.filter(user_answering=s_user)
    races = ['Chinese', 'Korean', 'Filipino', 'Vietnamese', 'Taiwanese', 'Thai']
    race_stats = {}

    for race in races:
        race_stats[race] = GroupStat(race)

    for race in race_stats:
        

    for answer in user_answers:
        if(answer.answer_skipped):
            num_skipped += 1
        if(answer.correct):
            num_correct += 1
        num_answers += 1

    percent_correct = num_correct / float(num_answers) * 100

    return render(request, 'ViewUserStats.html', {
        'num_answers': num_answers,
        'num_correct': num_correct,
        'num_skipped': num_skipped,
        'percent_correct': percent_correct,
    })

class GroupStat:
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.attempt_1 = 0
        self.attempt_2 = 0
        self.attempt_3 = 0
        self.attempt_more = 0
        self.skipped = 0
        self.total_time = 0
