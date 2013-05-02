from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from DDAGame.models import Answer as Answer_model
from DDAGame.models import QuestionType as QuestionType_model
from auth.models import DDAUser as DDAUser_model

@login_required(login_url="/login/")
def ViewUserStats(request):
    s_user = DDAUser_model.objects.get(user=request.user) 
    races = ['Chinese', 'Korean', 'Filipino', 'Vietnamese', 'Taiwanese', 'Thai']
    race_question = QuestionType_model.objects.get(id=1)
    age_question = QuestionType_model.objects.get(id=2)

    race_stats = {}

    for race in races:
        race_stats[race] = {}
        race_stats[race]['race_total'] = 0
        race_stats[race]['race_attempt_1'] = 0
        race_stats[race]['race_attempt_2'] = 0
        race_stats[race]['race_attempt_3'] = 0
        race_stats[race]['race_attempt_more'] = 0
        race_stats[race]['race_skipped'] = 0
        race_stats[race]['race_total_time'] = 0
        race_stats[race]['age_total'] = 0
        race_stats[race]['age_attempt_1'] = 0
        race_stats[race]['age_attempt_2'] = 0
        race_stats[race]['age_attempt_3'] = 0
        race_stats[race]['age_attempt_more'] = 0
        race_stats[race]['age_skipped'] = 0
        race_stats[race]['age_total_time'] = 0
        
    for race in race_stats:
        user_answers = Answer_model.objects.filter(user_answering=s_user).filter(user_photo_race=race)
        for answer in user_answers:
            if(answer.question_type==race_question): #race 
                if(answer.answer_skipped):
                    race_stats[race]['race_skipped'] += 1
                else:
                    race_stats[race]['race_total'] += 1
                    if(answer.num_attempted == 1):
                        race_stats[race]['race_attempt_1'] += 1
                    elif(answer.num_attempted == 2):
                        race_stats[race]['race_attempt_2'] += 1
                    elif(answer.num_attempted == 3):
                        race_stats[race]['race_attempt_3'] += 1
                    else:
                        race_stats[race]['race_attempt_more'] += 1
            elif(answer.question_type==age_question):
                if(answer.answer_skipped):
                    race_stats[race]['age_skipped'] += 1
                else:
                    race_stats[race]['age_total'] += 1
                    if(answer.num_attempted == 1):
                        race_stats[race]['age_attempt_1'] += 1
                    elif(answer.num_attempted == 2):
                        race_stats[race]['age_attempt_2'] += 1
                    elif(answer.num_attempted == 3):
                        race_stats[race]['age_attempt_3'] += 1
                    else:
                        race_stats[race]['age_attempt_more'] += 1 

    js_data = simplejson.dumps(race_stats) 
    return render(request, 'ViewUserStats.html', {
        'race_stats': js_data,
    })

class GroupStat:
    def __init__(self, name):
        self.name = name
        self.race_total = 0
        self.race_attempt_1 = 0
        self.race_attempt_2 = 0
        self.race_attempt_3 = 0
        self.race_attempt_more = 0
        self.race_skipped = 0
        self.race_total_time = 0
        self.age_total = 0
        self.age_attempt_1 = 0
        self.age_attempt_2 = 0
        self.age_attempt_3 = 0
        self.age_attempt_more = 0
        self.age_skipped = 0
        self.age_total_time = 0
