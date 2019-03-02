from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from evalapp.models import *
from evalapp.forms import *
from evalapp.trustCalc import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# views for Eval App

from django.views import generic

# class viewEvals(generic.ListView):
	# model = appliedEval
	
# class viewEval(generic.DetailView):
	# model = appliedEval

def index(request):
	"""everything in this 'index' function is for the main page of evalapp""" 
	#right now it's a test for form submission
	if request.method == 'POST':
		referent_creation_form = create_referentStandIn(request.POST)
		if referent_creation_form.is_valid():
			newReferent = referent_creation_form.save(commit=False)
			newReferent.save()
			return HttpResponseRedirect('/admin/')
	else:
		referent_creation_form = create_referentStandIn(request.POST)
	context = {'form' : referent_creation_form}
	return render(request, 'evalapp/home.html', context)

	
#def referentPage(request, pk):
	# referent_object = get_object_or_404(referent, pk=pk)
	# if request.method == 'POST':
		
def applyEvalViewFunction(request):
	if request.method == 'POST':
		evalApplyingForm = formFuncToApplyEval(request.POST)
		if evalApplyingForm.is_valid():
			newAppliedEval = evalApplyingForm.save(commit=False)
			newAppliedEval.appliedBy = request.user
			newAppliedEval.save()
			return HttpResponseRedirect('/admin/')
	else:
		evalApplyingForm = formFuncToApplyEval(request.POST)
	context = {'form' : evalApplyingForm}
	return render(request, 'evalapp/htmlFileForApplyEvalForm.html', context)
	
def viewEval(request, pk):
	#have to check if the user owns the evaluation
	#if yes, they can see and edit it
	#if not, they get told they can't view it
	
	evalObj = appliedEval.objects.get(pk=pk)
	if request.user == evalObj.appliedBy:
		context = {'user': 'correctUser', 'appliedeval': evalObj}
		
	
	else:
		context = {'user': 'wrongUser'}
		
	return render(request, 'evalapp/appliedeval_detail.html', context)
	
def contextForUser(request, pk, correctUser, itemsToGet):

	if request.user == correctUser:
		context = itemsToGet
	
	return context
	
	
def viewEvals(request):
	allEvals = appliedEval.objects.all()
	
	evalList = []
	
	#for security, only supply items that
	#belong to the user!
	for eachEval in allEvals:
		if eachEval.appliedBy == request.user:
			evalList += [eachEval]
	
	context = {'appliedeval_list': evalList}
	return render(request, 'evalapp/appliedeval_list.html', context)
	
def editEval(request, pk):
	#have to check if the user owns the evaluation
	#if yes, they can see and edit it
	#if not, they get told they can't view it
	
	evalObj = appliedEval.objects.get(pk=pk)
	if request.user == evalObj.appliedBy:
		context = {'user': 'correctUser', 'appliedeval': evalObj}
		
	
	else:
		context = {'user': 'wrongUser'}
		
	return render(request, 'evalapp/appliedeval_detail.html', context)
	

def matchIdentitiesViewFunction(request):
	if request.method == 'POST':
		identityMatchingForm = create_identity(request.POST)
		if identityMatchingForm.is_valid():
			newIdentityMatch = identityMatchingForm.save(commit=False)
			newIdentityMatch.identifiedBy = request.user
			newIdentityMatch.save()
			return HttpResponseRedirect('/admin/')
	else:
		identityMatchingForm = create_identity(request.POST)
	context = {'form' : identityMatchingForm}
	return render(request, 'evalapp/htmlFileForMatchingIdentitiesForm.html', context)
	
def networkTestVF(request):
	x = request.user
	context = {'user': x}
	#context["users_evaluations"] = gettingEstimates(x, 1, 1)
	#context['estimates'] = weightedCalc(x, context["users_evaluations"])
	#context += {"users_evaluations": x.appliedEval}
	context['estimates'] = masterTrustFunc(x)
	return render(request, 'evalapp/htmlFileForNetworkTest.html', context)
	
def boilerplateFormStuff(request, form, autoUserField, redirect, theUrl):
	#this function does boilerplate form creation
	#inputs:
	#form:  the function in the file forms.py being used
	#autoUserField:  what the field is called (in the model) that
	#          specifies which user created the object instance
	#redirect: what page to go to after submission, like: '/admin/'
	#theUrl:  the Url that will show this form to the user
	
	if request.method == 'POST':
		thisForm = form(request.POST)
		if thisForm.is_valid():
			newObjectInstance = thisForm.save(commit=False)
			
			#damn, this is the part that's tricky to automate, whyyyyy
			#maybe I need to change this to a generic thing
			#in all models call it "madeByUser"
			#for now I'll see if "autoUserField" variable idea works
			if autoUserField != 'nada':
				newObjectInstance.autoUserField = request.user
			newObjectInstance.save()
			
			
			#redirect = ('/admin/')
			return HttpResponseRedirect(redirect)
	else:
		thisForm = form(request.POST)
	context = {'form' : thisForm}
	return render(request, theUrl, context)
	
def createReferentVF(request):
	theView = boilerplateFormStuff(request, create_referentStandIn, 'nada', '/admin/', 'evalapp/htmlFileForCreateReferentForm.html')
	return theView
	
def newUserVF(request):
	theView = boilerplateFormStuff(request, create_user, 'nada', '/admin/', 'evalapp/htmlFileForCreateUserForm.html')
	return theView