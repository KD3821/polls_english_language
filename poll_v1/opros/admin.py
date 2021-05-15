from django.contrib import admin
from .models import Variant, Question, Answer, Table_Res

# Register your models here.
admin.site.register(Variant)

class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 3



class QuestionAdmin(admin.ModelAdmin):
    list_display = ('variant', 'question_text', 'pub_date')
    list_filter = ['variant', 'pub_date']
    search_fields = ['question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Вариант теста', {'fields': ['variant']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [AnswerInLine]



class Table_ResAdmin(admin.ModelAdmin):
    list_display = ('uchenik_name', 'variant_done', 'mark', 'date_res')
    list_filter = ['uchenik_name', 'variant_done', 'date_res']
    search_fields = ['uchenik_name']


admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer)

admin.site.register(Table_Res, Table_ResAdmin)