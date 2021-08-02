from django.urls import path

from . import views

app_name = 'votes'
urlpatterns = [
    path('', views.Decisions.as_view(), name='decisions'),
    path('create/', views.DecisionCreate.as_view(), name='create'),
    path('invitations/', views.Invitations.as_view(), name='invitations'),
    path('invitations/create/', views.InvitationCreate.as_view(), name='invite'),
    path('join/', views.JoinTeam.as_view(), name='join'),
    path('owned/', views.DecisionsOwned.as_view(), name='owned'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('registration/done/', views.RegistrationDone.as_view(), name='registration-done'),
    path('results/', views.Results.as_view(), name='results'),
    path('teams/', views.Teams.as_view(), name='teams'),
    path('<int:pk>/', views.DecisionInfo.as_view(), name='info'),
    path('<int:pk>/result/', views.ResultInfo.as_view(), name='result'),
    path('<int:pk>/vote/', views.VoteCreate.as_view(), name='vote'),
]
