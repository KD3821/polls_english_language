from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.



class Variant(models.Model):
    variant_text = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.variant_text

    def var_vopr(self):
        return Variant.objects.all()

    def var_vopr_var(self):
        return Variant.objects.all().filter(id)




class Question(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now
    #     # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    #
    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = 'Published recently?'




class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    choices = models.IntegerField(default=0)
    COR_ANSWER = (
        (1, 'Да'),
        (0, 'Нет')
    )
    correct_answer = models.IntegerField(verbose_name='Правильный Ответ', default=0, choices=COR_ANSWER)
    # point = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text




class CorrectAns(models.Model):
    user = 'teacher'
    variant_asked = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    vopros_asked = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    cor_ans = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)




class ChosenAns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant_done = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    vopros_done = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    chosen_ans = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)



class Student_User(models.Model):
    user_zovut = models.ForeignKey(User, on_delete=models.CASCADE)
    variant_sdelal = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    question_sdelal = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    question_text_sdelal = models.CharField(max_length=200, null=True)
    answer_sdelal = models.CharField(max_length=200)
    answer_pravil = models.CharField(max_length=200)
    point_ball = models.IntegerField(default=0)



    # def __init__(self, *args, **kwargs):
    #     return super().__init__(*args, **kwargs)

class Table_Res(models.Model):
    # uchenik = models.ForeignKey(Student_User, on_delete=models.CASCADE)
    uchenik = models.IntegerField(default=0)
    uchenik_name = models.CharField(max_length=200, null=True)
    variant_done = models.ForeignKey(Variant, on_delete=models.CASCADE)
    # variant_done = models.IntegerField(default=0)
    mark = models.IntegerField(default=0)
    date_res = models.DateTimeField(default=datetime.now, blank=True)

