"""evalsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#The Eval App urls
from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from evalapp.views import viewEvals
from evalapp.views import viewEval


from django.contrib.auth.models import User

# urlpatterns = [
    # url(r'^$', views.index, name='index')]

# urlpatterns += [   
	# path('referent/<uuid:pk>/', views.referentPage, name='referentPage'),
# ]

urlpatterns = [
    path('', views.index, name='index'),
	path('applyingEval/', views.applyEvalViewFunction, name='applyingEval'),
	path('createReferent/', views.createReferentVF, name='createReferent'),
	path('networkTest/', views.networkTestVF, name='networkTest'),
	path('matchingIdentities/', views.matchIdentitiesViewFunction, name='matchingIdentities'),
	#path('newuser/', views.newUserVF, name='newUser'),
	url(r'^create_user/$',(CreateView.as_view(model=User, get_success_url =lambda: '/evalapp/#tab1', form_class=UserCreationForm, template_name='evalapp/htmlFileForCreateUserForm.html')), name='create_user'),
	#path('viewevals/', viewEvals.as_view(), name='viewevals'),
	path('viewevals/', views.viewEvals, name='viewevals'),
	#path('eval/<int:pk>', viewEval.as_view(), name='vieweval'),
	path('eval/<int:pk>', views.viewEval, name='vieweval'),
	path('editEval/<int:pk>', views.editEval, name='editEval'),
]

