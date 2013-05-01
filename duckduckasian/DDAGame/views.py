from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from auth.models import DDAUser as DDAUser_model
from DDAGame.models import QuestionType as QuestionType_model
from DDAGame.models import Answer as Answer_model

from datetime import date, datetime
import random

@login_required(login_url="/login/")
def PlayGame(request):
    if request.POST:
        if(request.POST.get('skipped') == "True"):
            skipped_answer_id = request.POST.get('answer_id')
            skipped_answer = Answer_model.objects.get(id=skipped_answer_id)
            skipped_answer.answer_skipped = True
            skipped_answer.save()
            #need to separately handle the case where the user skips before/after answering
            #save the previous question appropriately and load a new one
        else:
            pass
            #what to do if user submits his answer

    num_photos = DDAUser_model.objects.count() - DDAUser_model.objects.filter(race=None).count()
    s_userID = random.randint(1, num_photos)
    photo_user = DDAUser_model.objects.get(id=s_userID) #retrieve random DDAUser 
    answering_user = DDAUser_model.objects.get(user_id=request.user.id)

    num_questions = QuestionType_model.objects.filter(active=True).count() 
    questionID = random.randint(1, num_questions)
    questiontype = QuestionType_model.objects.get(id=questionID) #retrieve random question

    new_answer = Answer_model.objects.create_Answer(questiontype, datetime.now(), answering_user, photo_user)
    new_answer.save()
    
    if(questiontype.info_type == "race"):
        is_race = True
        is_age = False 
        correct_answer = photo_user.race 
    elif(questiontype.info_type == "age"):
        is_race = False 
        is_age = True
        correct_answer = calculate_age(photo_user.date_of_birth)

    return render(request, 'PlayGame.html', {
        'user': request.user,
        'photo_user': photo_user,
        'is_race': is_race,
        'is_age': is_age,
        'correct_answer': correct_answer,
        'question': questiontype,
        'answer_id': new_answer.id,
    })

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    
    if birthday > today:
        return today.year - born.year -1
    else:
        return today.year - born.year
