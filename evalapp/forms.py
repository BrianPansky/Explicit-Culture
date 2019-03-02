from django.forms import ModelForm
from django.core.exceptions import ValidationError
from evalapp.models import *
from django.contrib.auth.models import User

class create_user(ModelForm):
	def clean_this(self):
		data = self.cleaned_data['username', 'email', 'password']
		return data
	class Meta:
		model = User
		fields = ['username', 'password', 'email']


class create_ontology(ModelForm):
	def clean_this(self):
		data = self.cleaned_data['name', 'description']
		return data
	class Meta:
		model = ontology
		fields = '__all__'
	
class create_referentStandIn(ModelForm):
	def clean_this(self):
		data = self.cleaned_data['type', 'name', 'description']
		return data
	class Meta:
		model = referentStandIn
		fields = '__all__'

class create_identity(ModelForm):
	def clean_this(self):
		data = self.cleaned_data['userIfAny', 'referentStandInIfAny']
		return data
	class Meta:
		model = identity
		exclude = ['identifiedBy']

class create_evalType(ModelForm):
	def clean_this(self):
		data = self.cleaned_data['name', 'description']
		return data
	class Meta:
		model = evalType
		fields = '__all__'
	
class formFuncToApplyEval(ModelForm):
	def clean_this(self):
		data = self.cleaned_data['typeApplied', 'appliedTo', 'appliedBy', 'evaluation']
		return data
	class Meta:
		model = appliedEval
		exclude = ['appliedBy']