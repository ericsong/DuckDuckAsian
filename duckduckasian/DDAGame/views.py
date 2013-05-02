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
        photo_user_id = request.POST.get("photo_user_id")
        question_type_id = request.POST.get("question_type")
        answer_id = request.POST.get("answer_id")
        correct = request.POST.get("correct")
        num_attempted = request.POST.get("num_attempted")

        photo_user = DDAUser_model.objects.get(id=photo_user_id)
        question_type = QuestionType_model.objects.get(id=question_type_id)
        answer = Answer_model.objects.get(id=answer_id)

        if(correct == "not answered"): #user skipped
            answer.answer_skipped = True
            answer.num_attempted = 0
        elif(correct == "True"):
            answer.answer_skipped = False
            answer.correct = True
            answer.num_attempted = 1 
        elif(correct == "False"):
            answer.answer_skipped = False
            answer.correct = False
            answer.num_attempted = int(num_attempted)

        answer.time_answered = datetime.now()
        answer.save();

    num_photos = DDAUser_model.objects.count() - DDAUser_model.objects.filter(race=None).count()
    s_userID = random.randint(1, num_photos)
    photo_user = DDAUser_model.objects.get(id=s_userID) #retrieve random DDAUser 
    answering_user = DDAUser_model.objects.get(user_id=request.user.id)

    num_questions = QuestionType_model.objects.filter(active=True).count() 
    questionID = random.randint(1, num_questions)
    questiontype = QuestionType_model.objects.get(id=questionID) #retrieve random question

    if(questiontype.info_type == "race"):
        is_race = True
        is_age = False 
        correct_answer = photo_user.race 
    elif(questiontype.info_type == "age"):
        is_race = False 
        is_age = True
        correct_answer = calculate_age_category(calculate_age(photo_user.date_of_birth))

    new_answer = Answer_model.objects.create_Answer(questiontype, datetime.now(), answering_user, photo_user, correct_answer)
    new_answer.save()

    return render(request, 'PlayGame.html', {
        'user': request.user,
        'photo_user': photo_user,
        'is_race': is_race,
        'is_age': is_age,
        'correct_answer': correct_answer,
        'question': questiontype,
        'answer_id': new_answer.id,
    })

def calculate_age_category(age):
    if(age < 10):
        return "0-9"
    elif(age < 20):
        return "10-19"
    elif(age < 30):
        return "20-29"
    elif(age < 40):
        return "30-39"
    elif(age < 50):
        return "40-49"
    elif(age < 60):
        return "50-59"
    elif(age < 70):
        return "60-69"
    else:
        return "70"

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
