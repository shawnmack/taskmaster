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
            self.liveCategories=[]
            self.win=tk.Tk()
            menubar=Menu(self.win)
            self.win.config(menu=menubar)
            fileMenu=Menu(menubar)
            def newCat():

                #clear all widgets??
                tvar1=tk.StringVar()
                catEnt=tk.Entry(textvariable=tvar1)
                def createCat():
                    newCatName=tvar1.get()
                    newCat=category(newCatName)
                    self.currentUser.categories.append(newCat)
                    self.liveCategories.append(newCat)
                    print('New category Object("'+newCatName+'") created.')
                    catEnt.delete(0,'end')


                catButt=tk.Button(text='Create',command=createCat)

                catEnt.grid(row=0,column=0)
                catButt.grid(column=1,row=0)
            def quit():
                self.win.quit()
                self.win.destroy()
                exit()
            def workflow():
                #clear all widgets?
                self.win.destroy()
                self.win=tk.Tk()
                for x in self.liveCategories:
                    frame=tk.Frame(self.win)
                    fLab=tk.Label(frame,text=x.name)
                    self.cGUIlist.append(fLab)
                    fLab.pack()
                    myInt=tk.IntVar()
                    fEnt=tk.Entry(frame,textvariable=myInt,width=3,text='')
                    self.cGUIlist.append(fEnt)
                    fEnt.pack()
                    fScroll=scrolledtext.ScrolledText(frame, width=30, height=3, wrap=tk.WORD)
                    self.cGUIlist.append(fScroll)
                    fScroll.pack()
                    def catComplete():
                        categoryComplete(fLab.cget('text'),'official comment',fEnt.get())
                        index=0
                        for x in self.liveCategories:
                            if fLab.cget('text')==x.name:
                                self.liveCategories.pop(index)
                                index=index+1
                        frame.destroy()
                    fButt=tk.Button(frame, text="Finish",command=catComplete)
                    self.cGUIlist.append(fButt)
                    fButt.pack()
                    frame.pack()
                self.win.mainloop()
                #create a new list to hold all the widgets
                #loop through livecategories and create 4 new widgets for each remaining Category
            fileMenu.add_command(label='Create New Category', command=newCat)
            fileMenu.add_command(label='Workflow Mode', command=workflow)
            fileMenu.add_command(label='Exit', command=quit)

            menubar.add_cascade(label="File",menu=fileMenu)
            self.win.mainloop()
    """
        if self.loggedIn==True:
            sW=30
            sL=3

            categories=self.currentUser.categories
            self.liveCategories=categories
            catRow=3
            self.win=tk.Tk()
            tvar1=tk.StringVar()
            ent1=tk.Entry(textvariable=tvar1)

            def updateGUI():

            def deleteCat():

            def newCategory():
                newCatName=tvar1.get()
                newCat=category(newCatName)
                categories.append(newCat)
                print('New category Object("'+newCatName+'") created.')
                ent1.delete(0,'end')
                self.categories.append(newCat)
                self.liveCategories.append(newCat)


                for x in liveCategories:
                    self.cGUIlist.append(tk.Label(text=x.name))
                    self.cGUIlist.append(tk.Entry(self.win,textvariable=myInt,width=3,text=''))
                    self.cGUIlist.append(scrolledtext.ScrolledText(self.win, width=sW, height=sL, wrap=tk.WORD))
                    self.cGUIlist.append(tk.Buttontext=x.name))1




"""
test=TaskMaster()
