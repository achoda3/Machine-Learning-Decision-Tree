from functools import total_ordering
from os import read
import random
import sys
import csv
import math
import collections
from anytree import Node, RenderTree
from random import choice

class example:
    def __init__(self, array):
        self.Alt = array[0]
        for i in range(1,11):
            array[i] = array[i].lstrip()

        self.Bar = array[1]
        self.Fri = array[2]
        self.Hun = array[3]
        self.Pat = array[4]
        self.Price = array[5]
        self.Rain = array[6]
        self.Res = array[7]
        self.Type = array[8]
        self.Est = array[9]
        self.Wait = array[10]
    
    def getAttrib(self, attrib):
        if attrib == 'Alt':
            return self.Alt
        elif attrib == 'Bar':
            return self.Bar
        elif attrib == 'Fri':
            return self.Fri
        elif attrib == 'Hun':
            return self.Hun
        elif attrib == 'Pat':
            return self.Pat
        elif attrib == 'Price':
            return self.Price
        elif attrib == 'Rain':
            return self.Rain
        elif attrib == 'Res':
            return self.Res
        elif attrib == 'Type':
            return self.Type
        else:
            return self.Est

    def getWait(self):
        return self.Wait

def B(q):
    return -( q * math.log( q , 2) + ( 1 - q ) * math.log( 1 - q , 2))

def pluralityValue(examples):
    countYes = 0
    countNo = 0
    for ex in examples:
        currExample = ex
        if currExample.getWait() == 'Yes':
            countYes = countYes + 1
        else:
            countNo = countNo + 1
    if countYes > countNo:
        return 'retYes'
    elif countNo > countYes:
        return 'retNo'
    else:
        retVal = choice(['retYes', 'retNo'])
        return retVal

def sameClass(examples):
    countYes = 0
    countNo = 0
    for ex in examples:
        currExample = ex
        if currExample.getWait() == 'Yes':
            countYes = countYes + 1
        else:
            countNo = countNo + 1
    if countYes == 0:
        return 'No'
    elif countNo == 0:
        return 'Yes'
    else:
        return 'Neither'

def importance(attribute, examples):
    countAtt = []
    numberOfExamples=0
    for ex in examples:
        numberOfExamples = numberOfExamples + 1
        currVal = ex.getAttrib(attribute)
        checkExist = False
        for row in countAtt:
            if row[0] == currVal:
                row[1] = row[1] + 1
                if ex.getWait() == 'Yes':
                    row[2] = row[2] + 1
                checkExist = True
        if checkExist == False:
            countAtt.append([])
            countAtt[len(countAtt) - 1].append(currVal)
            countAtt[len(countAtt) - 1].append(1)
            if ex.getWait() == 'Yes':
                countAtt[len(countAtt) - 1].append(1)
            else:
                countAtt[len(countAtt) - 1].append(0)
    sum = 0
    for row in countAtt:
        #print(row)
        if(row[2] / row[1]) != 1 and (row[2] / row[1]) != 0:
            sum = ( row[1] / numberOfExamples ) * B( row[2] / row[1]) + sum
    return 1-sum
    
def allValues(attribute, examples):
    allValues = []
    for ex in examples:
        currVal = ex.getAttrib(attribute)
        #print("currVal")
        #print(currVal)
        checkExist = False
        for row in allValues:
            if row == currVal:
                checkExist = True
        if checkExist == False:
            allValues.append(currVal)
                
    return allValues

def decisionTreeLearning(examples, attributes, parent_examples, parentNode, allExamples):
    if len(examples) == 0:
        return (pluralityValue(parent_examples), parentNode)
    elif sameClass(examples) == 'Yes':
        return ('retYes', parentNode)
    elif sameClass(examples) == 'No':
        return ('retNo', parentNode)
    elif len(attributes) == 0:
        return (pluralityValue(examples), parentNode)
    else:
        max = 0
        for a in attributes:
            curr = importance(a, examples)
            if curr > max:
                max = curr
                A = a
        if parentNode.name == 'Top':
            startNode = Node(A)
        else:
            startNode = Node(A, parent=parentNode)
            #print(allValues(A, examples))
        for value in allValues(A, allExamples):
            newNode = value
            addNode = Node(newNode, parent=startNode)
            #print(A)
            exs = []
            for ex in examples:
                if ex.getAttrib(A) == value:
                    exs.append(ex)
            newAttrib = [x for x in attributes if x != A]
            subtree = decisionTreeLearning(exs, newAttrib, examples, addNode, allExamples)
            if subtree[0] == 'retYes':
                addNode.name = value + " => Yes"
            elif subtree[0] == 'retNo':
                addNode.name = value + " => No"
            else:
                newNode = value
            #addNode = Node(newNode, parent=startNode)
        return (A, startNode)
            
    
            

        

        

attributes = ['Alt', 'Bar', 'Fri', 'Hun', 'Pat', 'Price', 'Rain', 'Res', 'Type', 'Est']
examples = []
file = sys.argv[1]

with open(file) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        examples.append(example(row))

#print(importance('Pat', examples))
passNode = Node('Top')
#print(passNode.name)
retVal = decisionTreeLearning(examples, attributes, examples, passNode, examples)
#print(pluralityValue(examples))
for pre, fill, node in RenderTree(retVal[1]):
    print("%s%s" % (pre, node.name))
