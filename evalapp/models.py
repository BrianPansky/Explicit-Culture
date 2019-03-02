from django.db import models
from django.contrib.auth.models import User

class ontology(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)
	#ontologies are like types of things
	#(the type of existence the things have)
	#main types are "realspace" and "cyberspace"
	#people are in realspace, their biography on the website is in cyberspace
	def __str__(self):
		return self.name
	
class referentStandIn(models.Model):
	type = models.ForeignKey(ontology, models.PROTECT, related_name='ontologies')
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class evalType(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)
	def __str__(self):
		return self.name
	
class identity(models.Model):
	userIfAny = models.ForeignKey(User, models.PROTECT, related_name='usersIfAny', blank=True, null=True)
	#need to figure out how to OPTIONALLY have MULTIPLE of these
	referentStandInIfAny = models.ForeignKey(referentStandIn, models.PROTECT, related_name='referentStandInsIfAny', blank=True, null=True)
	identifiedBy = models.ForeignKey(User, models.PROTECT, related_name='identifierPeople')
	def __str__(self):
		#!!!!!!!!!!  need to fix this string!  needs to say userIfAny and/or referentStandInIfAny!!!!!
		#could just ask user to specify which name to use as the "main name", then use it here in str
		#and/or use if statements to check what exists, and by default choose the first one that exists
		return 'identified by' + self.identifiedBy.username
	
class appliedEval(models.Model):
	typeApplied = models.ForeignKey(evalType, models.PROTECT, related_name='appliedEvals')
	appliedTo = models.ForeignKey(identity, models.PROTECT, related_name='referentStandInEvalApplyees')
	evaluation = models.DecimalField(max_digits=2, decimal_places=2)
	appliedBy = models.ForeignKey(User, models.PROTECT, related_name='evaluators', blank=True, null=True)
	#!!!!!!!!!!  Made it nullable just to shut up errors for now!!!!!!!!!!!
	def __str__(self):
		return self.appliedBy.username + ' ' + 'evaluated' + ' ' + self.appliedTo.__str__() + ' ' + str(self.evaluation) + ' ' + 'on' + ' ' + self.typeApplied.name

		
		
# class metaReport(models.Model):
	# #holds my "T" value for each report
	# #"T" is how much the report is trusted
	# #it collapses a chain of evaluations into one number
	# forUser = models.ForeignKey(User, models.PROTECT, related_name='metaReporters', blank=True, null=True)
	# T = models.DecimalField(max_digits=2, decimal_places=2)
	# aboutReport = models.ForeignKey(appliedEval, models.PROTECT, related_name='reportsAboutReports')
	
	# #could also store the final report on the person?  But that would involve a "T" coming from multiple directions...
	
	# def __str__(self):
		# return self.forUser.username + 'will viewthe follwoing report as ' + self.T + 'percent trustworthy:  ' + self.aboutReport.__str__()

# class report(models.Model):
	# #should take someone's applied eval? And how much someone trusts it?
	# #but for chaining......shouldn't all of this be collapsed into "applied eval"?
	# #otherwise some reports will be about appliedEvals, some will need to be about other reports
	# #would be better to have all one thing!!!
	# #only difference is that this report includes TWO DIFFERENT evaluations
	# #one by reporter, one by reportee, right?
	# reportee =
	# reporter =
	# evalType = 
	# reportedEval =
	# def __str__(self):
		# return self.reporter.username + 'says' + self.reportee.__str__() + 'is' self.evalType.__str__()
	
	
	
	