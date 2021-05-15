from django.urls import path, include
from . import views
from .views import mail_to



app_name = 'opros'
urlpatterns = [
    # path('<int:variant_id>/', views.VarVoprView.xxx, name='index'),
    path('<int:variant_id>/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:variant_id>/<int:pk>/res_one/', views.ResultsView.as_view(), name='res_question'),
    path('<int:variant_id>/<int:question_id>/choice/', views.ChooseView.choose, name='vote'),
    path('<int:variant_id>/<int:question_id>/next/', views.ChooseView.nextpage, name='vote_again'),
    path('', views.VariantView.as_view(), name='index_t'),
    path('<int:pk>/', views.VarDesView.zzz, name='index_v'),
    path('<int:pk>/res_all/', views.ResultsAllView.as_view(), name='res_test'),
    path('<int:variant_id>/<int:pk>/rec/', views.Zapis_Res.zapis, name='record'),
    path('<int:variant_id>/<int:pk>/rec_total/', views.Zapis_Total.zapis_total, name='record_total'),
    path('contact/', mail_to, name='contact_us'),
]

