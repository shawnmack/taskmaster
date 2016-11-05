#misc
import datetime
import random
import traceback
#data
import csv
import pickle
#gui
import tkinter as tk
from tkinter import scrolledtext, Menu

class category(object):
    def __init__(self,name):
        self.name=name
        self.results=[]
        self.timecreated=str(datetime.datetime.now())
        print('New category instantiated ('+ self.name+')'+ ' at '+self.timecreated+'.')

    def summary(self):
        pass

class user(object):
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.categories=[]
        self.results=[]
        self.timecreated=str(datetime.datetime.now())
        print('New User instantiated ('+ self.username+')'+ ' at '+self.timecreated+'.')

class usersData(object):
    def __init__(self):
        #dataBase=list of users
        self.dataBase=[]
        print('New usersData instance instantiated.')

class TaskMaster(object):
    def load(self):
        print('load method called...')
        try:
        #save state found
            fileObject = open( "programState",'rb')
            self.programState = pickle.load(fileObject)
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

    def save(self):
        file_Name = 'programState'
        fileObject = open(file_Name,'wb')
        pickle.dump(self.programState,fileObject)
        fileObject.close()
        print('Saved.')

    def __init__(self):
        print('Taskmaster class instantiated!')
        #Check to see if saved state exists and load if it exists.
        self.load()
        #If there are no users created prompt user to create a new account.
        if len(self.dataBase.dataBase)==0:
            print('No users found.')
            nameInput=input('Input desired Username.')
        #List current users in command line with prompt to select your account.



#usersData contains user(s) which contain category(s) which contain results(s) which contain categoryComplete(s)


mytest=TaskMaster()
