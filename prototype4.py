#miscModules
import datetime
import random
import traceback
import time
import os
#data
import csv
import pickle
#gui
import tkinter as tk
from tkinter import scrolledtext


class categoryEntry(object):

    def __init__(self,category):
        self.score=None
        self.assCat = category
        self.comments=None
        self.name = category.name
        self.timeStarted = datetime.datetime.now()
        self.totalSeconds = []
        self.completedSeconds = 0
        self.assCat.assUser.inProgress = True
        self.assCat.assUser.currentTask = self
        self.assCat.started = True
        self.opTime = 0
        self.completedTime = None
        self.samedayOverride = False
        print('Category entry('+ self.name+')'+ ' at '+str(self.timeStarted)+'.')
        if(self.assCat.type == "Binary"):
            print('Intializing ' + self.assCat.name + " task.")
        elif(self.assCat.type == "Open-ended"):
            print('Intializing ' + self.assCat.name + " timed task. " + str(self.assCat.remainingGoal) +' minutes remaining.')
        elif(self.assCat.type == "One-shot"):
            print('Intializing ' + self.assCat.name + " one time task.")
        elif(self.assCat.type == "Buffer"):
            print('Intializing ' + self.assCat.name + " buffer task. " + str(self.opTime) + ' minutes thusfar today.')

    def finishedSummary(self):
        sumString = self.name + ' completed in ' + str(int(self.completedSeconds/60)) + ' minutes. Score of ' + str(self.score) + '.' + '\n\t' + self.comments
        return sumString

    def startAgain(self):
        self.timeStarted = datetime.datetime.now()
        self.assCat.assUser.currentTask = self
        self.assCat.assUser.inProgress = True

    def updateEntry(self):

        if(self.assCat.type == "Binary"):
        ##UPDATING TYPE 1 BINARY task completion is not based on a fixed amount of time
            doneStatus = input("Is this task completely done? Y/N")
            if(doneStatus == 'y' or doneStatus =='Y'):
                self.assCat.startedCat = self
                self.score = input('Score(out of 100)')
                self.comments = input('Write any constructive commentary or reflection:')
                endTime = datetime.datetime.now() - self.timeStarted
                self.totalSeconds.append(endTime.seconds)
                for x in self.totalSeconds:
                    self.completedSeconds = self.completedSeconds + x
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
                self.assCat.completed = True
                for x in self.assCat.assUser.categories:
                    if(self.assCat.name == x.name):
                        self.assCat.assUser.retiredCategories.append(x)
                        self.assCat.assUser.categories.remove(x)
                        for z in self.assCat.assUser.onecat:
                            if(self.assCat.name == z.name):
                                self.assCat.assUser.onecat.remove(z)
                print(self.assCat.name + ' task completed in ' + str(self.completedSeconds/60) + ' minutes.')
                self.assCat.assUser.refreshOrder()
                self.assCat
            elif(doneStatus == 'n' or doneStatus =='N'):
                stopTime = datetime.datetime.now()
                elapsedTime =  stopTime - self.timeStarted
                self.totalSeconds.append(elapsedTime.seconds)
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
                self.assCat.startedCat = self
        elif(self.assCat.type == "Open-ended"):
        ###Open-ended type completion is based on a goal amount of time
            self.assCat.startedCat = self
            endTime = datetime.datetime.now()
            timeElapsed = endTime - self.timeStarted
            self.opTime = self.opTime + int(timeElapsed.seconds/60)
            if(self.opTime >= self.assCat.remainingGoal):
                self.assCat.complete = True
                print('Goal reached.')
                self.score = input('Score(out of 100)')
                self.comments = input('Write any constructive commentary or reflection:')
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
                self.assCat.completed = True
                for x in self.assCat.assUser.categories:
                    if(self.assCat.name == x.name):
                        self.assCat.assUser.retiredCategories.append(x)
                        self.assCat.assUser.categories.remove(x)
                        for z in self.assCat.assUser.twocat:
                            if(self.assCat.name == z.name):
                                self.assCat.assUser.twocat.remove(z)
                self.totalSeconds = opTime
                self.assCat.assUser.refreshOrder()
            else:
                self.assCat.remainingGoal = self.assCat.remainingGoal - int(timeElapsed.seconds/60)
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
                self.assCat.startedCat = self

        elif(self.assCat.type == "One-shot"):
        ###One-shot tasks they are completed and not saved, i.e a to do list of one time things
            doneStatus = input("Is this task completely done? Y/N")
            if(doneStatus == 'y' or doneStatus =='Y'):
                self.assCat.startedCat = self
                self.assCat.complete = True
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
                self.assCat.completed = True
                for x in self.assCat.assUser.categories:
                    if(self.assCat.name == x.name):
                        self.assCat.assUser.categories.remove(x)
                        for z in self.assCat.assUser.threecat:
                            if(self.assCat.name == z.name):
                                self.assCat.assUser.threecat.remove(z)
                self.assCat.assUser.refreshOrder()
            elif(doneStatus == 'N' or doneStatus =='N'):
                self.assCat.startedCat = self
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
        elif(self.assCat.type == "Buffer"):
            if(self.assCat.buffType == 1):
            ##non-timed buffer activity, retired when finished and returned the next day
                self.assCat.startedCat = self
                self.assCat.complete = True
                self.assCat.assUser.currentTask = None
                self.assCat.assUser.inProgress = False
                self.assCat.completed = True
                self.score = 'N/A'
                self.comments ='Completed'
                for x in self.assCat.assUser.categories:
                    if(self.assCat.name == x.name):
                        self.assCat.assUser.retiredCategories.append(x)
                        self.assCat.assUser.categories.remove(x)
                        for z in self.assCat.assUser.fourcat:
                            if(self.assCat.name == z.name):
                                self.assCat.assUser.fourcat.remove(z)
                self.assCat.assUser.refreshOrder()
            elif(self.assCat.buffType == 2):
            ##timed buffer activity, never gets retired just counted, always displayed
                    self.assCat.started = True
                    endTime = datetime.datetime.now()
                    timeElapsed = endTime - self.timeStarted
                    self.opTime = self.opTime + int(timeElapsed.seconds/60)
                    self.assCat.startedCat = self
                    self.assCat.assUser.currentTask = None
                    self.assCat.assUser.inProgress = False
                    self.assCat.assUser.refreshOrder()

class category(object):

    def __init__(self,name,catType,user):
        self.name = name
        self.timecreated = str(datetime.datetime.now())
        self.assUser = user
        self.entries = []
        self.completed = False
        self.started = False
        self.startedCat = None
        if(catType == 1):
            self.type = "Binary"
            user.categories.append(self)
            user.onecat.append(self)
        elif(catType == 2):
            self.type = "Open-ended"
            self.goal = int(input('What is the desired number of minutes for this task per day?(in minutes)'))
            self.remainingGoal = self.goal
            user.categories.append(self)
            user.twocat.append(self)
        elif(catType == 3):
            self.type = "One-shot"
            user.categories.append(self)
            user.threecat.append(self)
        elif(catType == 4):
            self.type = "Buffer"
            self.buffType = int(input('Input 1 for instant one-shot or 2 for open ended.'))
            self.timeLength = 0
            user.categories.append(self)
            user.fourcat.append(self)
        print('New '+ self.type + ' category instantiated (' + self.name + ')' + ' at ' + self.timecreated + '.')

    def listString(self):
        if(self.type == "Binary"):
            lString = self.name
        elif(self.type == "Open-ended"):
            lString = self.name + ' ' + str(self.remainingGoal) + ' minute(s) remaining.'
        elif(self.type == "One-shot"):
            lString = self.name
        elif(self.type == "Buffer"):
            lString = self.name
        return lString

    def startEntry(self):
            self.entries.append(categoryEntry(self))



class user(object):

    def __init__(self,username):
        self.username=username
        self.categories=[]
        self.onecat=[]
        self.twocat=[]
        self.threecat=[]
        self.fourcat=[]
        self.results=[]
        self.retiredCategories=[]
        self.timecreated=str(datetime.datetime.now())
        self.inProgress = False
        self.currentTask = None
        self.dayOver = False
        self.lastClosingTime = None
        self.todayStartTime = None
        print('New User instantiated ('+ self.username+')'+ ' at '+self.timecreated+'.')

    def completeCat(self,catName):
        for x in self.categories:
            if(catName == x.name):
                pass

    def refreshOrder(self):
        self.categories = []
        for x in self.onecat:
            self.categories.append(x)
        for x in self.twocat:
            self.categories.append(x)
        for x in self.threecat:
            self.categories.append(x)
        for x in self.fourcat:
            self.categories.append(x)

    def endDay(self):

        for x in self.retiredCategories:
            if(x.type == 'Binary'):
                x.completed = False
                x.started = False
                x.startedCat = None
                self.onecat.append(x)

        for x in self.retiredCategories:
            if(x.type == 'Open-ended'):
                x.completed = False
                x.started = False
                x.startedCat = None
                self.twocat.append(x)

        for x in self.retiredCategories:
            if(x.type == 'One-shot'):
                x.completed = False
                x.started = False
                x.startedCat = None
                self.threecat.append(x)

        for x in self.retiredCategories:
            if(x.type == 'Buffer'):
                x.completed = False
                x.started = False
                x.startedCat = None
                self.fourcat.append(x)

        self.retiredCategories = []
        self.refreshOrder()
        self.dayOver = True
        self.lastClosingTime = datetime.datetime.now()

    def startNewDay(self):
        todayStartTime = datetime.datetime.now()
        sleepTime = todayStartTime - self.lastClosingTime
        print(str(int(sleepTime.seconds/60))+' hours ' + str(int(int(sleepTime.seconds)/3600)) + ' minutes '+ str(int(int(sleepTime.seconds)%3600)) + ' seconds since program closed.')

class usersData(object):

    def __init__(self):
        #dataBase=list of users
        self.dataBase=[]
        print('New usersData instance instantiated.')
        self.stayLogged = False
        self.stayLoggedUser = None

class TaskMaster(object):

    def load(self):
        print('load method called...')
        try:
        #save state found
            fileObject = open( "database",'rb')
            self.dataBase = pickle.load(fileObject)
            print("gamestate successfully loaded...")
        except:
        #save state not found
                traceback.print_exc()
                print("--exception--(most likely that save file doesn't exist)")
                self.dataBase=usersData()
        try:
            print('Attempting to recreate gamestate...')
            pass
        except:
            print('Exception occured in creating gamestate.')
            pass

    def loadSpecial(self):
        userToKeep = self.currentUser.username
        print('loadSpecial called. Here is the current directory contents:')
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            print(f)

        dbName = input('Which save file to load?')
        try:
        #save state found
            fileObject = open(dbName,'rb')
            self.dataBase = pickle.load(fileObject)
            print("gamestate successfully loaded...")
            for x in self.dataBase.dataBase:
                if(x.username == userToKeep):
                    self.currentUser = x
        except:
            traceback.print_exc()
            print('loadSpecial failed! Run for the hills!')

    def save(self):
        file_Name = 'database'
        fileObject = open(file_Name,'wb')
        pickle.dump(self.dataBase,fileObject)
        fileObject.close()
        print('Saved.')

    def saveSpecial(self):
        file_Name = 'database'

        while(file_Name == 'database'):
            file_Name = input('saveSpecial called. Input desired filename for current program state.(It cannot be \'database\' =]).')

        fileObject = open(file_Name,'wb')
        pickle.dump(self.dataBase,fileObject)
        fileObject.close()
        print('Saved.')

    def logIn(self):

        def attemptCreate(newUser):
        #check if username exists
            available=True
            for x in self.dataBase.dataBase:
                if x.username == newUser:
                    print('Username already exists, select another.')
                    available=False
                    attemptCreate(input('Input desired name'))
                    pass

            if available == True:
                ##fix##first time called it always creates a user with a blank username regardless of what is in the entry widget
                print('Duplicate username not found. Creating new profile.')
                ###probably need an try except here?
                newProfile=user(newUser)
                self.dataBase.dataBase.append(newProfile)
                self.logIn()

        print('Current Profiles:')
        if(len(self.dataBase.dataBase)>0):
            for x in self.dataBase.dataBase:
                print(x.username)
        accountYN = input('Do you want to use an existing profile? Y/N')
        if(accountYN == 'Y' or accountYN == 'y'):
            inputtedUser=input('Input user name')
            for x in self.dataBase.dataBase:
                if(str(inputtedUser) == str(x.username)):
                    self.loggedIn = True
                    self.currentUser = x
                else:
                    print('Username not found. Let\'s try again.')
                    self.logIn()
                    pass
        elif(accountYN =='N' or accountYN == 'n'):
            desiredName=input('Creating new profile. Input desired name.')
            attemptCreate(desiredName)

    def __init__(self):
        self.loggedIn=False
        self.load()
        self.currentUser=None
        if(self.dataBase.stayLogged == True):
            self.currentUser = self.dataBase.stayLoggedUser
            self.loggedIn = True
        else:
            while(self.loggedIn == False):
                self.logIn()
        if(self.currentUser.dayOver == True):
            print('Starting new day.')
            self.currentUser.startNewDay()
        if self.loggedIn==True:

            print(self.currentUser.username+' is logged in!')
            self.save()

            def defineNewCat():
                print('Defining new category. Input number for desired type.')
                catNumber = input('1. Binary \n2. Open-ended \n3. One-Shot \n4. Buffer')
                catName = input('Input category name.')
                newCat = category(catName,int(catNumber),self.currentUser)
                self.save()

            def userSummary():
                print('----Completed----')
                for x in self.currentUser.retiredCategories:
                        print(x.startedCat.finishedSummary())
                print('-----------------')

            def developerMode():
                commandInt=int(input('Options(input int):\n1.Save program state in alternate file.(under current user)\n2.Load alternate program state from filename.'))
                if(commandInt == 1):
                    self.saveSpecial()
                elif(commandInt == 2):
                    self.loadSpecial()
                ##fix completed category entries
                ##manually input some fake results

            def lastExit():
                self.currentUser.endDay()

            def populateActiveList():
                cInt = 1
                ####populating full list with no tasks currently started
                if(self.currentUser.inProgress == False):

                    for x in self.currentUser.onecat:
                        if(x.completed == False):
                            print(str(str(cInt) + ' ' + x.listString()))
                            cInt = cInt + 1
                    for x in self.currentUser.twocat:
                        if(x.completed == False):
                            print(str(str(cInt) + ' ' + x.listString()))
                            cInt = cInt + 1
                    for x in self.currentUser.threecat:
                        if(x.completed == False):
                            print(str(str(cInt) + ' ' + x.listString()))
                            cInt = cInt + 1
                    print('-Buffers-')
                    for x in self.currentUser.fourcat:
                        if(x.completed == False):
                            buffString= str(str(cInt) + ' ' + x.listString())
                            if(x.started == True):
                                buffString = str(buffString + ' ' + str(x.startedCat.opTime) + ' minute(s).')
                            print(buffString)
                            cInt = cInt + 1
                else:

                    ####skipping other non-buffer tasks and only printing active task
                    print(str(cInt) + " " + self.currentUser.currentTask.name + ' is currently in progress.')
                    cInt = cInt + 1
                print("**Options**")
                print(str(cInt)+' Define or edit categories')
                cInt = cInt + 1
                print(str(cInt)+' Exit')
                cInt = cInt + 1
                print(str(cInt)+' Today\'s Summary and Details')
                cInt = cInt + 1
                print(str(cInt)+' Developer Mode')
                cInt = cInt + 1
                print(str(cInt)+' Final Exit(End Day)')
                cInt = cInt + 1
                ######processing user input command off of populated list
                commandInt = int(input('Input command.'))
                if(self.currentUser.inProgress == False):
                    if(commandInt == len(self.currentUser.categories)+1):
                        defineNewCat()
                        commandInt=9999999999999
                    if(commandInt == len(self.currentUser.categories)+3):
                        userSummary()
                    if(commandInt == len(self.currentUser.categories)+4):
                        developerMode()
                    if(commandInt == len(self.currentUser.categories)+5):
                        lastExit()
                    if(commandInt == len(self.currentUser.categories)+2):
                        self.loggedIn=False
                    cInt = 0
                    for x in (range(len(self.currentUser.categories))):
                        if(cInt + 1 == commandInt and self.currentUser.categories[x].started == False):
                            self.currentUser.categories[x].startEntry()
                        elif(cInt + 1 == commandInt and self.currentUser.categories[x].started == True):
                            self.currentUser.categories[x].startedCat.startAgain()
                        cInt = cInt + 1
                else:

                    if(self.currentUser.inProgress == False):
                        if(commandInt == len(self.currentUser.categories)+1):
                            defineNewCat()
                            commandInt=9999999999999
                        if(commandInt == len(self.currentUser.categories)+2):
                            self.loggedIn=False
                        if(commandInt == len(self.currentUser.categories)+3):
                            userSummary()
                        if(commandInt == len(self.currentUser.categories)+4):
                            developerMode()
                        if(commandInt == len(self.currentUser.categories)+5):
                            print('End current task then reselect this option')
                        if(commandInt == 1):
                            self.currentUser.currentTask.updateEntry()
                    else:
                        if(commandInt == 2):
                            defineNewCat()
                        if(commandInt == 3):
                            self.loggedIn = False
                        if(commandInt == 4):
                            userSummary()
                        if(commandInt == 5):
                            developerMode()
                        if(commandInt == 1):
                            self.currentUser.currentTask.updateEntry()

            if(len(self.currentUser.categories)<1):
                print('It looks like you don\'t have any categories defined. Let\'s make some!')
                defineNewCat()
                self.save()

            while(self.loggedIn == True):
                populateActiveList()

            print('Exiting program.')
            print('By default this account is staying logged in.')

            self.dataBase.stayLogged = True
            self.dataBase.stayLoggedUser = self.currentUser
            self.save()

test=TaskMaster()
