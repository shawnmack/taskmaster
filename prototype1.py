#misc
import datetime
import random
import traceback
#data
import csv
import pickle
#gui
import tkinter as tk
from tkinter import scrolledtext

class categoryComplete(object):
    def __init__(self,name,comments,score):
        self.score=score
        self.comments=comments
        self.name = name
        self.timecreated=str(datetime.datetime.now())
        print('Category completed('+ self.name+')'+ ' at '+self.timecreated+'.')

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

    def logIn(self):
        win=tk.Tk()
        userVar=tk.StringVar()
        passVar=tk.StringVar()
        ent1=tk.Entry(textvariable=userVar,width=20)
        ent2=tk.Entry(textvariable=passVar,width=20,show='*')

        def forgotPass():
            print('forgot butt press')

        def attemptCreate():
        #check if username exists
            print(ent1.get())
            available=True
            for x in self.dataBase.dataBase:
                if x.username == ent1.get():
                    print('Username already exists, select another.')

                    available=False
            #func#shitty password


            if available == True:
                ##fix##first time called it always creates a user with a blank username regardless of what is in the entry widget
                print('Duplicate username not found. Acceptable password. Creating new account.')
                ###probably need an try except here?
                newUser=user(ent1.get(),ent2.get())
                self.dataBase.dataBase.append(newUser)
                win.destroy()
                self.logIn()
        def newAccount():
            tk.Label(text='Username:').grid(row=1,column=0)
            userVar=tk.StringVar()
            ent1=tk.Entry(textvariable=userVar,width=20)
            ent1.grid(row=1,column=1)
            tk.Label(text='Password:').grid(row=2,column=0)
            passVar=tk.StringVar()
            ent2=tk.Entry(textvariable=passVar,width=20,show='*')
            ent2.grid(row=2,column=1)

            ###add button with '?' or something similiar so user can request password policy
            createButt=tk.Button(command=attemptCreate,text='Create Account')
            createButt.grid(row=3,column=1)

            win.mainloop()

        forgotButt=tk.Button(command=forgotPass,text='Reset Password')
        forgotButt.grid(row=0,column=0)
        newButt=tk.Button(command=newAccount,text='Create New Account')
        newButt.grid(row=0,column=2)
        tk.Label(text='Username:').grid(row=1,column=0)


        ent1.grid(row=1,column=1)
        tk.Label(text='Password:').grid(row=2,column=0)


        ent2.grid(row=2,column=1)
        #add button with '?' or something similiar so user can request password policy etc.
        def authenticate():
            print('auth butt pressed.')
            usernameFound=False
            for x in self.dataBase.dataBase:
                if x.username == ent1.get():
                    usernameFound=True
            if usernameFound==True:
                for x in self.dataBase.dataBase:
                    if x.username == ent1.get() and x.password == ent2.get():
                        print('Username and password entered correctly. '+ent1.get()+' is logging on.')
                        self.currentUser=x
                        self.loggedIn=True
                        win.destroy()
                        return
            else:
                print('Username not found.')

        logButt=tk.Button(command=authenticate,text='Login')
        logButt.grid(row=3,column=1)


        win.mainloop()

    def __init__(self):

        self.programState=None
        self.load()
        self.loggedIn=False
        self.currentUser=None
        self.logIn()
        self.cGUIlist=[]
        if self.loggedIn==True:
            sW=30
            sL=3

            categories=self.currentUser.categories
            self.liveCategories=categories
            self.win=tk.Tk()
            tvar1=tk.StringVar()
            ent1=tk.Entry(textvariable=tvar1)

            def updateGUI():

                ent1.grid(row=0,column=0)
                butt1.grid(row=0,column=1)
                catRow=3
                self.cGUIlist=None

                def createCatGUI(catRow,category):
                    if self.cGUIlist == None:
                        self.cGUIlist=[]
                    sW=30
                    sL=3
                    myInt=tk.IntVar()
                    myString=tk.StringVar()
                    myEnt=tk.Entry(self.win,textvariable=myInt,width=3,text='')
                    scroll=scrolledtext.ScrolledText(self.win, width=sW, height=sL, wrap=tk.WORD)

                    def buttPress():
                        inputt = scroll.get("1.0",'end-1c')
                        change=False
                        for z in self.liveCategories:
                            if z.name == myLab.cget('text'):
                                z.results.append(categoryComplete(myLab.cget('text'),inputt,myEnt.get))
                                for x in self.liveCategories:
                                    index=0
                                    if x.name==z.name:
                                        self.liveCategories.pop(index)
                                        updateGUI()
                                        return
                                    else:
                                        index=index+1



                    myLab=tk.Label(text=x.name)
                    self.cGUIlist.append(myLab)
                    self.cGUIlist.append(myEnt)
                    self.cGUIlist.append(scroll)
                    myButt=tk.Button(self.win,command=buttPress,text='Finish')
                    self.cGUIlist.append(myButt)
                    catRow=catRow+2

                for x in self.liveCategories:
                    print(x.name+' is being created in the GUI.')
                    createCatGUI(catRow,x)
                switch=False
                cRow=catRow
                cCol=0
                if self.cGUIlist != None:
                    for x in self.cGUIlist:
                        if switch==False:
                            x.grid(row=cRow,column=cCol)
                            switch=True
                        else:
                            x.grid(row=cRow,column=cCol+1)
                            cRow=cRow+1
                            switch=False
                catRow=3

                print('GUI updated.')
                self.win.mainloop()
                ent1.focus()

            def newCategory():
                newCatName=tvar1.get()
                categories.append(category(newCatName))
                print('New category Object("'+newCatName+'") created.')
                ent1.delete(0,'end')
                updateGUI()


            butt1=tk.Button(command=newCategory,text='New Category')

            ent1.grid(column=0,row=0)
            butt1.grid(column=1,row=0)

            self.win.mainloop()


test=TaskMaster()
