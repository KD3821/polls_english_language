from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView

from .models import Question, Answer, Variant, Student_User, Table_Res
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages


def sample_view(request):
    html = '<body><h1>Django sample_view</h1><br><p>Отладка sample_view</p></body>'
    return HttpResponse(html)



def mail_to(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'mail_from_person@mail.com', ['mail_to_person@mail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('../')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'opros/contact.html', {"form": form})




class IndexView(LoginRequiredMixin, generic.ListView):
    model = Question
    template_name = 'opros/index.html'




class VarVoprView(LoginRequiredMixin, generic.ListView):
    model = Question
    template_name = 'opros/index.html'

    def xxx(request, variant_id):
        question_filtered =Question.objects.filter(variant__id=variant_id).order_by('pub_date')
        return render(request, 'opros/index.html', {'variant_id': variant_id, 'question_filtered': question_filtered})




class VarDesView(LoginRequiredMixin, generic.ListView):
    model = Variant
    template_name = 'opros/index_v.html'

    def zzz(request, pk):
        var_needed=Variant.objects.get(id=pk)
        var_description = var_needed.description
        variant_id = var_needed.id
        return render(request, 'opros/index_v.html', {'var_description': var_description, 'variant_id': variant_id})




class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'opros/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())




class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'opros/res_question.html'




class ResultsAllView(LoginRequiredMixin, generic.DetailView):
    model = Variant
    template_name = 'opros/res_spisok.html'




class ChooseView(LoginRequiredMixin, generic.FormView):
    model = Question
    template_name = 'opros/detail.html'

    def choose(request, variant_id, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_answer = question.answer_set.get(pk=request.POST['choice'])
        except (KeyError, Answer.DoesNotExist):
            return render(request, 'opros/detail.html', {
                'question': question,
                'error_message': "You didn't select an answer",
            })
        else:
            selected_answer.choices = 1
            selected_answer.save()
        # return HttpResponseRedirect(reverse('opros:res_question', args=(question.variant_id, question.id,)))
        return HttpResponseRedirect(reverse('opros:record', args=( variant_id, question_id,)))

    def nextpage(request, variant_id, question_id):
        if question_id == 0:
            pub_date = datetime.now()
            variant = Variant.objects.get(id=variant_id)
            results = variant.table_res_set.all()
            for result in results:
                if result.uchenik == request.user.id:
                    if result.variant_done_id == variant_id:
                        hhh = result.mark
                        return HttpResponseRedirect(reverse('opros:res_test', args=(variant_id,)))

        else:
            pub_date_obj = Question.objects.get(id=question_id)
            pub_date = pub_date_obj.pub_date

        question_list = Question.objects.filter(variant=variant_id, pub_date__lt=pub_date).order_by('-pub_date')
        if question_list.first() is not None:
            question_id = question_list.first().id
            variant_id = question_list.first().variant_id
            question = get_object_or_404(Question, pk=question_id)
            return HttpResponseRedirect(reverse('opros:detail', args=(variant_id, question_id, )))
        else:
            return HttpResponseRedirect(reverse('opros:record_total', args=(variant_id, question_id,)))
            # return HttpResponseRedirect(reverse('opros:res_test', args=(variant_id,)))




class VariantView(LoginRequiredMixin, generic.ListView):
    model = Variant
    template_name = 'opros/index_t.html'
    context_object_name = 'var_vopr'




class Zapis_Res(LoginRequiredMixin, generic.DetailView):
    model = Student_User
    template_name = 'opros/index_zap.html'

    def zapis(self, variant_id, pk):
        exemplyar = Student_User()
        exemplyar.user_zovut_id = self.user.id
        exemplyar.variant_sdelal = Variant.objects.all().get(id=variant_id)
        exemplyar.question_sdelal = Question.objects.get(id=pk)
        exemplyar.question_text_sdelal = exemplyar.question_sdelal.question_text
        xxx = Student_User.objects.all().filter(user_zovut_id=exemplyar.user_zovut_id)
        for x in xxx.filter(variant_sdelal_id=exemplyar.variant_sdelal):
            if x.question_sdelal_id == exemplyar.question_sdelal_id:
                x.delete()

        # exemplyar.answer_sdelal = exemplyar.question_sdelal.answer_set.get(pk=request.POST['choice'])
        exemplyar.answer_sdelal = exemplyar.question_sdelal.answer_set.get(choices = 1)
        exemplyar.answer_pravil = exemplyar.question_sdelal.answer_set.get(correct_answer = 1)
        if exemplyar.answer_sdelal == exemplyar.answer_pravil:
            exemplyar.point_ball = 1
        else:
            exemplyar.point_ball = 0
        exemplyar.save()
        x = exemplyar.answer_sdelal
        x.choices = 0
        x.save()

        return HttpResponseRedirect(reverse('opros:vote_again', args=(variant_id, pk,)))



class Zapis_Total(LoginRequiredMixin, generic.FormView):
    model = Table_Res
    template_name = 'opros/index_zap_all.html'


    def zapis_total(request, variant_id, pk):
        prav_count = 0
        exemplyar_res = Table_Res()

        exemplyar = Student_User()
        exemplyar.user_zovut_id = request.user.id
        exemplyar.variant_sdelal = Variant.objects.all().get(id=variant_id)
        ooo = Student_User.objects.all().filter(user_zovut_id=exemplyar.user_zovut_id)
        for ppp in ooo.filter(variant_sdelal_id=variant_id):
            if ppp.point_ball == 1:
                prav_count += 1

        aaa = Question.objects.all().filter(variant = variant_id)

        bbb = aaa.count()
        res = (prav_count/bbb)*100
        ccc = res
        exemplyar_res.mark = ccc
        exemplyar_res.variant_done_id = variant_id
        exemplyar_res.uchenik = exemplyar.user_zovut_id
        exemplyar_res.uchenik_name = exemplyar.user_zovut
        exemplyar_res.save()

        return HttpResponseRedirect(reverse('opros:res_test', args=(variant_id, )))

