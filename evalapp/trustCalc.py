from django.shortcuts import get_object_or_404

from evalapp.models import *

import copy

#ok how to do this
#gather all evaluation objects that are relevant?
#could do that easily if I just arbitrarily set a limit to the number of
#"degrees of separation" I'll allow.  But if I want to use %trust threshholds to 
#determine the cutoff, will need to be calculating that as it crawls the network
#I guess I'll start with the simple way, just to get stuff in place and tested
#then I'll modify with fancy stuff :)


def evalReportsAndMap(asker):
	#crawls through the network from the user
	#gathers all reports
	evals = appliedEval.objects.filter(appliedBy = asker)
	
	evalSet = []
	evaluators = [asker]
	
	baseSet = {asker: {'upper': 1, 'lower': 1}}
	
	for i in evals:
		evalSet.append(i)
		if i.appliedTo.userIfAny != None:
			evaluators.append(i.appliedTo.userIfAny)
			baseSet[i.appliedTo.userIfAny] = {'upper':i.evaluation, 'lower': i.evaluation}
		else:
			baseSet[i.appliedTo.referentStandInIfAny] = {'upper':i.evaluation, 'lower': i.evaluation}
	# print(baseSet)
	
	#need to do one loop for each EVALUATOR
	#not once for each EVALUATION
	#so I need to make a set of all evaluators
	
	
	
	for evaluator in evaluators:
		evalsByUserInLoop = appliedEval.objects.filter(appliedBy = evaluator)
		for x in evalsByUserInLoop:
			if x not in evalSet:
				evalSet.append(x)
			if x.appliedTo.userIfAny != None:
				if x.appliedTo.userIfAny not in evaluators:
					evaluators.append(x.appliedTo.userIfAny)
		
		

	return [evalSet, baseSet]

def organizeReportsByIdentity(unorganizedReports):
	#oprganizes reports so that each identity is paired with a set of
	#all evaluations of that identity (whether user or nonuser)
	
	#input should be QuerySet of all evals
	#output should be dictionary such as:
	#  {itentityObject: [listOfEvalsOfThatIdentity], ...}
	
	#might also be good to store the map of eval dependencies along with each identity
	#but probably good to make as much of that map in the initial scouting?
	#good in what way?  efficiency?  actually less iterations?  Faster?  Am I sure?
	#  {personUserEvaluated: {whoTheyEvaluated1: {etc.}, whoTheyEvaluated2: {etc}}}
	
	organizedReports = {}  #initializing
	
	for each in unorganizedReports:
		if each.appliedTo.userIfAny != None:
			if each.appliedTo.userIfAny in organizedReports:
				organizedReports[each.appliedTo.userIfAny] += [each]
			else:
				organizedReports[each.appliedTo.userIfAny] = [each]
		else:
			if each.appliedTo.referentStandInIfAny in organizedReports:

				organizedReports[each.appliedTo.referentStandInIfAny] += [each]
			else:
				organizedReports[each.appliedTo.referentStandInIfAny] = [each]
	return organizedReports


	
def makeRatios(report, estimates, ratioSet):
	#adds to numerators and denominators
	#print(report.appliedTo.userIfAny)
	R = float(report.evaluation)
	upperT = float(estimates[report.appliedBy]['upper'])
	lowerT = float(estimates[report.appliedBy]['lower'])
	
	#numerators:
	#numerators (upper and lower) for R
	RU = R*upperT
	RL = R*lowerT
	
	#numerators (upper and lower) for T
	TU = upperT*upperT
	TL = lowerT*lowerT
	
	#denominators (upper and lower)
	dU = upperT
	dL = lowerT
	
	toAdd = {'RU': RU,'RL': RL,'TU': TU,'TL': TL,'dU': dU,'dL': dL}
	
	for i in toAdd:
		#print('???????????????is ratioset empty???????????????????????????')
		#print(ratioSet)
		ratioSet[i] = ratioSet[i] + toAdd[i]
	
	#print(ratioSet)
	return ratioSet
	

def estimateLoop(theUser, baseSet, organizedReports, reportSet, estimates, unevaluated, pathSet, fillPreReq):
	
	#OUTLINE OF ALGORITHM:------------------------------
	# loop for each report on that person in the parent loop (where this function is called)
	# a check to see if the report is from someone we have an estimate for
	# if yes, add their report and trustworthiness to the numerators and denominators
	# if not, recursively do the above steps, and this one*
	# use the completed numerators and denominators to create an entry in the collection of estimates!
	# this function returns "estimates"
	
	#* IMPORTANT EXCEPTIONS:
	#if recursion has led us in a circle, have to change tactics to prevent infinite loop
	
	
	#EXPLANATION OF INPUT VARIABLES----------------------
	#"unevaluated" is the person we are trying to calculate an estimate for
	#"reportSet" is the set of reports specific to the "unevaluated" person
	#print(estimates)
	
	
	#initializing ratioSet so we can add to numerators and denominators:
	ratioSet = {'RU': 0,'RL': 0,'TU': 0,'TL': 0,'dU': 0,'dL': 0}
	
	print('=============== starting a thing ===============')
	
	
	# loop for each report on that person in the parent loop (where this function is called)
	for report in reportSet:
		#print('4444444444444for report in reportSet4444444444444')
		#print(ratioSet)
		#is this report made by someone we have an estimate for?
		if report.appliedBy in estimates:
			#print(str(report.appliedBy) + ' is in estimates')
			#yes this report is made by someone we have an estimate for
			#thus, it can be used without further investigation (at least in analytic mode)
			
			
			#so, add their report and trustworthiness to the numerators and denominators:
			#print('makes ratios, where do they go?')
			ratioSet = makeRatios(report, estimates, ratioSet)
			#print('done ratios')
			#print(estimates)
		else:
			#no, this report is not by someone we have an estimate for
			#print(str(report.appliedBy) + ' is NOT in estimates')
			#thus we need an estimate for THEM before we can use this report
		
			#but if we've already gone in a loop, just break
			
			#print(estimates)
			if report.appliedBy not in pathSet:
				#print(str(report.appliedBy) + ' is NOT in pathset')
			
				#recursively do the above steps, and this one
				
				#but first, add to the path set as we move along the path
				pathSet.append(unevaluated)
				#print("--------STARTING recursion meant to fill pre-requisites-------")
				#print(estimates)
				#print("need the following report.appliedBy in estimates, currently isn't")
				#print(report.appliedBy)
				
				#NOW do recursion to fill pre-requisites
				estimates = estimating(theUser, baseSet, organizedReports, organizedReports[report.appliedBy], estimates, report.appliedBy, pathSet)
				
				#print("--------DONE recursion meant to fill pre-requisites, so here's the report.appliedBy that we needed it to have, and here's estimates to see if we successfully have it-------")
				#print(report.appliedBy)
				#print(estimates)
				#print(ratioSet)
				
				#remove items from the path set as we finish that area of the path
				if unevaluated in pathSet:
					pathSet.remove(unevaluated)
				
				#now can add their report and trustworthiness to the numerators and denominators:
				ratioSet = makeRatios(report, estimates, ratioSet)
				#print(estimates)
		
			else:
				#ok, this is where I make "false estimates" to deal with a circular
				#set of evaluations
				#print(str(report.appliedBy) + ' IS in pathset, thus we have gone in a circle!!!!')
				#print(pathSet)
				#print('went in loop, so, we have to get ' + str(report.appliedBy) + ' into estiamtes, using a false estiamate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				#print('sorting out user and username:')
				#print(report.appliedBy)
				
				
				
				
				estimates[report.appliedBy] = {'upper': 0.5, 'lower': 0.5}
				
				
				#print('and now use this false estimate, and recursion, to evaluate this unevaluated:')
				#print(unevaluated)
				
				estimates = estimating(theUser, baseSet, organizedReports, reportSet, estimates, report.appliedBy, pathSet)
				
				#print('ok, now special recursion is done!  so now do ratioset???****************************************************************************************************************************************')
				ratioSet = makeRatios(report, estimates, ratioSet)
				#print(estimates)


			
			
			#print('yes, we have gone in a loop, and got back at the start')
	
		
	#print('?????????????????????????is this where the bad calculation happens???????????????????????????????')
	#print(estimates)
	if ratioSet['dU'] != 0:
		#use the numerators and denominators to get the
		#combined versions of upper and lower T
		newUpperR = float(ratioSet['RU']/ratioSet['dU'])
		newLowerR = float(ratioSet['RL']/ratioSet['dL'])
		
		newUpperT = float(ratioSet['TU']/ratioSet['dU'])
		newLowerT = float(ratioSet['TL']/ratioSet['dL'])
		#print("+++++++++++++++++++++here's some internal calculation figures:++++++++++++++")
		#print(newUpperT, newUpperR, newLowerR, newLowerT)
		
		#use these new combined values to make an upper and lower estimate
		upper = 1 + newUpperT*(newUpperR - 1)
		lower = newLowerR*newLowerT
		
		#print(upper, lower)
		
		if lower > upper:
			swap = [lower, upper]
			lower = swap [1]
			upper = swap[0]
		
		#print(upper, lower)
		
		estimates[unevaluated] = {'upper': upper, 'lower': lower}
	#else:
		#print("denominator = ZEROOOOO !!!!!!!!!!!!!!!!")
		
	#print('======= ***Returning Estimates *** =======')
	#print(estimates)
	#print('when is this done?')
	
	
	return estimates
	
	
def estimating(theUser, baseSet, organizedReports, reportSet, estimates, unevaluated, pathSet):

	#"unevaluated" is the person we are trying to calculate an estimate for
	#"reportSet" is the set of reports specific to the "unevaluated" person
	
	#this function returns "estimates"
	
	
	
	#first check if the base user has evaluated the "unuevaluated" person 
	#(by checking if they are in baseSet)
	#Never alter an estimate made by the user.
	if unevaluated in baseSet:
		return estimates
	
	
	
	# print('is this applied by user?')
	# for report in reportSet:
		# if report.appliedBy == theUser:
			# print('was applied by user')
			# return estimates
	# print("this shouldn't print if previous line says it was applied by the user")
	#print('is this enevaluated person in the pathset?')
	if unevaluated in pathSet:
		#means we have gone in a loop
		#print('0000000000000000000000000000000000000000000000000yes, we have gone in a loop, and got back at the start0000000000000000000000000000000000000000000000000000000000000000000000')
		#print(unevaluated)
		#print(estimates[])
		estimates = estimateLoop(theUser, baseSet, organizedReports, reportSet, estimates, unevaluated, pathSet, 'no')
		L=0
		U=1
		print(">>>>check convergence of U<<<<")
		#print(abs((estimates[unevaluated]['upper']-L)))
		print(estimates[unevaluated]['upper'])
		while abs((estimates[unevaluated]['lower']-L)) > 0.0000001 and abs((estimates[unevaluated]['upper']-U)) > 0.01:
			
			L=estimates[unevaluated]['lower']
			U=estimates[unevaluated]['upper']
			#print("CHECK THAT i DON'T NEED DEEP copy")
			#print(L)
			
			estimates = estimateLoop(theUser, baseSet, organizedReports, reportSet, estimates, unevaluated, pathSet, 'no')
			print("now.........")
			#print(abs((estimates[unevaluated]['upper']-L)))
			print(estimates[unevaluated]['upper'])
			
		pathSet.remove(unevaluated)
		print("SAYS U CONVERGED!")
		#print(estimates)
	else:
		#means we have not gone in a loop
		#print("................no, so we haven't gone in a loop")
		estimates = estimateLoop(theUser, baseSet, organizedReports, reportSet, estimates, unevaluated, pathSet, 'yes')
		#print(estimates)
		
	#print('returning estiamtes from func 1')
	return estimates
	
def masterTrustFunc(asker):
	#here I'll call all the other functions
	
	
	#scout the network to get all evaluations, and get baseSet
	scout = evalReportsAndMap(asker)
	
	unorganizedReports = scout[0]
	baseSet = copy.deepcopy(scout[1])
	estimates = scout[1]
	
	#organize all reports by who they are about (by identity, actually?)
	organizedReports = organizeReportsByIdentity(unorganizedReports)
	
	#so, below, we get estimates for each person we have reports for
	#only whenever we don't already have estimates for them
	for i in organizedReports:
		if i not in estimates:
			print("$$$$$$$$$$$~~~~LOOK WHAT'S HAPPENING!!!!!~~~~~~~~~~~~~~~~")
			estimates = estimating(asker, baseSet, organizedReports, organizedReports[i], estimates, i, [])
		
	
	return estimates
		
