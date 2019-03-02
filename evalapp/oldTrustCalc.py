#trust aggregation
#Should now handle conflicting reports properly!

import shelve

#setting up some "user profile" type things to test:

##b={'name':'Bob'}
##c={'name':'Carol'}
##d={'name':'Dan'}
##e={'name':'Eline'}
##f={'name':'Fred'}
##g={'name':'Gloria'}
##h={'name':'Henry'}
##i={'name':'Isabelle'}
##b.setdefault('can trust',{'Dan':.6, 'Eline':.8, 'Carol':.6})
##c.setdefault('can trust',{'Fred':.7, 'Gloria':.9})
##d.setdefault('can trust',{'Henry':.3, 'Bob':.85})
##e.setdefault('can trust',{'Isabelle':.6, 'Henry':.9})

a={'name':'a','can trust':{'Bob':.5,'Carol':.8}}

##userProfileDatabase = [a,b,c,d,e,f,g,h,i]

shelfUserProfileDatabase = shelve.open('myDatabase')
##shelfUserProfileDatabase['userProfileDatabase'] = userProfileDatabase
##shelfUserProfileDatabase.close()

userProfileDatabase = list(shelfUserProfileDatabase['userProfileDatabase'])
shelfUserProfileDatabase.close()


#and now here's the function:
#input an asker, and how much to trust the asker,
#and return the reply
#a dictionary of how much they should trust everyone

listOfReports = []   #just to initialize

def whoToTrustReports(asker, trustInAnswer):
        asked = asker.get('can trust','none to ask') #the people asked are the people who the asker can trust
        
        if asked != 'none to ask':  #if there is someone to ask!
            #then get their report(s)
            #asker asks each person they know who to trust:
            for reportAbout in list(asked.keys()):
                #^reportAbout is who the report is about
                thisReport = {'report about': str(reportAbout), 'reported trust': asked[reportAbout], 'trustworthiness of report': trustInAnswer}
                listOfReports.append(thisReport)
                if trustInAnswer*asked[reportAbout] > 0.1:
                    #must be above threshold for us to care!
                    for n in userProfileDatabase:
                        #^look through the database of users
                        if n['name'] == reportAbout:
                            #^find the user profiles for the people asked
                            #get them to ask the people they know for reports:
                            x = whoToTrustReports(n, trustInAnswer*asked[reportAbout])
                            if type(x) == dict:
                                listOfReports.append(x)


        return listOfReports

def organizeReportsByName(unorganizedReports):
    #turns a bunch of reports into
    #one set of reports about each person
    #at top level just two keys
    #     1) 'report(s) about'
    #     2) 'report(s)'
    organizedReports = {}  #initializing
    for each in unorganizedReports:
        #reports = []  #initializing
        if each['report about'] in organizedReports:
            organizedReports[each['report about']].append({'reported trust':each['reported trust'], 'trustworthiness of report': each['trustworthiness of report']})
        else:
            organizedReports.setdefault(each['report about'], [{'reported trust':each['reported trust'], 'trustworthiness of report': each['trustworthiness of report']}])
    return organizedReports

def weightedCalc(organizedReports):
    weightedTrustList = {} #initializing
    for each in organizedReports:  #for each person
        myNumerator = 0 #initializing
        myDenominator = 0
        for n in organizedReports[each]:
            myNumerator += n['reported trust']*n['trustworthiness of report']
            myDenominator += n['trustworthiness of report']
        weightedTrust = myNumerator/myDenominator
        weightedTrustList.setdefault(each, weightedTrust)
    return weightedTrustList
#print(whoToTrustReports(a, 1))
who = whoToTrustReports(a, 1)
org = organizeReportsByName(who)

#print(userProfileDatabase)
#print(org)
print(weightedCalc(org))

