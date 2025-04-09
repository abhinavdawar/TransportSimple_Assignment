from django.urls import path
from django.contrib.auth.views import LoginView , LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('question/new/', views.post_question, name='post_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('answer/<int:answer_id>/like/', views.like_answer, name='like_answer'),
    path('questions/<int:question_id>/answer/', views.post_answer, name='post_answer'),
]
