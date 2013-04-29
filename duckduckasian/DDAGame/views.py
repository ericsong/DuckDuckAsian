from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from auth.models import DDAUser as DDAUser_model
from DDAGame.models import QuestionType as QuestionType_model
from DDAGame.models import Answer as Answer_model

from DDAGame.forms import AnswerTextForm, AnswerNumberForm

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
        form = AnswerTextForm()
    elif(questiontype.info_type == "age"):
        form = AnswerNumberForm()

    return render(request, 'PlayGame.html', {
        'user': request.user, 
        'photo_user': photo_user, 
        'question': questiontype, 
        'answer_id': new_answer.id,
        'form': form,
    })

def PlayGameAnswer(request):
    if request.method == 'POST':
        photo_user_id = request.POST.get("photo_user_id")
        question_type_id = request.POST.get("question_type")
        answer_id = request.POST.get("answer_id") 

        photo_user = DDAUser_model.objects.get(id=photo_user_id)
        question_type = QuestionType_model.objects.get(id=question_type_id)
        answer = Answer_model.objects.get(id=answer_id)
    
        if(question_type.info_type == "race"):
            form = AnswerTextForm(request.POST)
        elif(question_type.info_type == "age"):
            form = AnswerNumberForm(request.POST)
  
        if form.is_valid():
            user_answer = form.cleaned_data['raw_answer']
        else:
            #what to do if user submits something retarded.... hmmmmmmmmmmmmmmmmmm
            pass 
        
        if question_type.info_type == "race":
            correct_answer = photo_user.race 
        elif question_type.info_type == "age":
            correct_answer = calculate_age(photo_user.date_of_birth) 

        compare1 = user_answer
        compare2 = correct_answer
    
        if isinstance(compare1, str):
            compare1 = compare1.lower()
            compare2 = compare2.lower()
       
        if compare1 == compare2:
            isuser_correct = True
            response = "good job!"
        else:
            isuser_correct = False
            response = "wronggggggggg"

        answer.time_answered = datetime.now()
        answer.answer_skipped = False
        answer.answer_raw = user_answer
        answer.answer_correct = correct_answer
        answer.correct = isuser_correct

        answer.save()

    
        return render(request, 'PlayGameAnswer.html', {
            'user': request.user,
            'photo_user': photo_user,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'response': response,
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
