# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:40:11 2024

@author: oawar
"""
import random
import time
import datetime

def stringTaker(mode): #use for "exceptions/rules" maybe move this to a new class
    names = []
    print("Enter stop when finished")
    while True:
        name = input(f"Enter {mode}:\t")
        if name =="stop":
            break
        names.append(name)
    return names

def teamTaker(): #maybe move this to a new class
    numTeams = int(input("Number of teams?:\t"))
    teams = []
    for i in range(int(numTeams)):
        print(f"Team {i+1}")
        team = stringTaker("name")
        teams.append(team)
    return teams

class Santa():
    def __init__(self, santas):#must be initialized with santas
        self.santas = santas
        self.teams = False
        if type(santas[0]) is list:
            self.teams = True
        self.dontGet = dict()
        self.picked = set()
        self.rulePicked = set()
        self.chosen = dict()
        #nameExtract
        self.names = set()
        if self.teams:
            for i in range(len(self.santas)):
                for j in range(len(self.santas[i])):
                    self.names.add(self.santas[i][j])
        else:
            self.names = set(self.santas.copy())
        for i in self.names:
            self.dontGet[i] = {i}
        if self.teams:
            self.teamRule()
    
    def start(self):
        self.start = time.perf_counter()
        
    def timeLogger(self):
        self.timeLog = time.perf_counter()
        #print(self.timeLog - self.start) #for testing
        if self.timeLog - self.start > 5:
            raise Exception("Assignment Impossible")
    
    def teamRule(self):
        assert self.teams,"teamRule called but no teams"
        for i in range(len(self.santas)):
            for j in self.santas[i]:
                self.dontGet[j].update(self.santas[i])
    
    def exceptions(self,rules = []):#can be called without rules if past is not considered
        #prob only use for the input after all other rules from old are collected
        ruleMaker = stringTaker("rule") #comment for testing
        #ruleMaker = [] #for testing
        self.rules = ruleMaker + rules
        for i in self.rules:#grab the = and put them in self.chosen
            assert len(i.split()) == 3,"Rule length problem"
            applied,n,person = i.split()
            if (applied not in self.names) or (person not in self.names):
                continue
            if "=" in i:
                self.chosen[applied] = person
                self.rulePicked.add(person)
                self.dontGet.pop(applied)
            else:
                self.dontGet[applied].add(person)
                
    def assignments(self):
        cantGet = {k: v for k, v in sorted(self.dontGet.items(), key=lambda item: len(item[1]), reverse=True)}
        self.start()
        while True:
            self.picked = self.rulePicked.copy()
            try:
                for i in cantGet:
                    canGet = self.names.copy()
                    for asignd in self.picked:
                        canGet.remove(asignd)
                    for notAllowed in cantGet[i]:
                        canGet.discard(notAllowed)
                    n = random.choice(list(canGet))
                    self.chosen[i] = n
                    self.picked.add(n)
                break
            except IndexError:
                self.timeLogger()
                continue

class fileHandling():
    def __init__(self,groupName):
        self.groupName = groupName
        data = []
        self.numYears = 0
        self.past = True
        try:
            with open("SecretSantaLog_" + self.groupName +".txt","r+") as logFile:
                info = logFile.read().replace(":","").split("Secret Santa ")[1:]
                self.numYears = len(info)
                for i in range(self.numYears):
                    data.append(info[i].strip().split("\n"))
            self.data = data
        except FileNotFoundError:
            self.data = data
            self.past = False
            
    def dataHandling(self):
        infoDict = dict()
        for i in self.data:
            infoYear = i.pop(0)
            i.pop(0) # can assign this to get old names
            infoDict[infoYear] = list()
            for j in i:
                infoDict[infoYear].append(j.replace("=","!"))
        return infoDict
    
    def fileWriting(self,names,assignments):
        currentYear = str(datetime.datetime.today().year)
        #currentYear = input("What year?:\t")#only for testing
        asstringments = ""
        for i in assignments:
            picked = f"{i} = {assignments[i]}\n"
            asstringments += picked
        with open("SecretSantaLog_" + self.groupName +".txt","a") as logFile:
            logFile.write(f"Secret Santa {currentYear}:\n{names}\n{asstringments}\n")

def main():
    print("Welcome to Secret Santa")
    rules = []
    
    fManager = fileHandling(input("What is the name of your group?:\t"))
    if fManager.past:
        oldData = fManager.dataHandling()
        for i in oldData:
            prompt = input(f"Allow participants to be assigned the same person as they were in {i}? (yes/no):\t")
            if prompt =="no":
                rules += oldData[i]
    
    prompt = input("Do you have teams? (yes/no):\t")
    if prompt == "yes":
        participants = teamTaker()
    else:
        participants = stringTaker("name")
        
    hat = Santa(participants)
    hat.exceptions(rules)
    hat.assignments()
    peopledict = hat.chosen
    fManager.fileWriting(participants, peopledict)
    for i in peopledict:
        with open(i+".txt","w") as outfile:
            outfile.write("You are "+peopledict[i]+"'s Secret Santa.")
    input("Press enter to quit")
main()
