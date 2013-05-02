from django.db import models
from auth.models import DDAUser

#model representing the possible questions a user can receive
class QuestionType(models.Model):
    active = models.BooleanField() #whether or not the question is currently active
    info_type = models.CharField(max_length=1024) #what info the question is asking for. Race, Age, etc
    text = models.CharField(max_length=1024) #Text that the question will display
    submit_format = models.CharField(max_length=1024) #what kind of submittion. radio? text input? number? etc

class AnswerManager(models.Manager):
    def create_Answer(self, question_type, time_started, user_answering, user_photo, user_photo_race, correct_answer):
        answer = self.create(question_type=question_type, time_started=time_started, user_answering=user_answering, user_photo=user_photo, user_photo_race=user_photo_race, answer_correct = correct_answer)
        return answer 

#model representing a user's answer
class Answer(models.Model):
    question_type = models.ForeignKey(QuestionType) #question type
    time_started = models.DateTimeField() #time the user started
    time_answered = models.DateTimeField(null=True) #time the user answered
    user_answering = models.ForeignKey(DDAUser, related_name='user_answering') #user answering the question
    user_photo = models.ForeignKey(DDAUser, related_name='user_photo') #user in the photo
    user_photo_race = models.CharField(max_length=1024) #user_photo's race 
    answer_skipped = models.BooleanField(blank=True) #whether or not the user skipped
    answer_raw = models.CharField(max_length=1024, null=True) #user's submitted answer
    answer_correct = models.CharField(max_length=1024) #correct answer retrieved from the user_photo's profile 
    correct = models.BooleanField(blank=True) #whether or not the answer is correct. redundant informatino but it might save some computation
    num_attempted = models.IntegerField(null=True); #number of attempts user took before getting the right answer

    objects = AnswerManager()
