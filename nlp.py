import operator
import sys
import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class TryNode():  
    def __init__(self, char):   
        self.char = char
        self.children = []
        self.wordFinished = False; 
            
class Corpus():
        def getStringArrayFromCorpus(self, fileName): 
            corpus = self.getCorpus("sentence/NLP-Application/Big.txt")
            corpusArray = corpus.split(' ')
            return corpusArray  
        def getCorpus(self, fileName):
            with open('sentence/NLP-Application/Big.txt', 'r') as myfile:
                data = myfile.read().replace('\n', ' ')
            return data       
        def makeUnigramMap(self):
            for string in self.corpusArray:
                self.unigramMap[string] = self.unigramMap.get(string, 0) + 1               
        def makeBigramMap(self):         
            size = len(self.corpusArray)
            for i in range(size - 1):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1]
                self.bigramMap[string] = self.bigramMap.get(string, 0) + 1              
        def makeTrigramMap(self):           
            size = len(self.corpusArray)           
            for i in range(size - 2):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1] + ' ' + self.corpusArray[i + 2]
                self.trigramMap[string] = self.trigramMap.get(string, 0) + 1             
        def makeNgramMap(self):   
            size = len(self.corpusArray)  
            for i in range(size - 3):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1] + ' ' + self.corpusArray[i + 2] + ' ' + self.corpusArray[i + 3]
                self.ngramMap[string] = self.ngramMap.get(string, 0) + 1              
        def makeNextWordsListMap(self):   
            for string in self.corpusArray:
                self.nextWordsListMap[string] = set()      
            size = len(self.corpusArray)  
            for i in range(size - 1):
                self.nextWordsListMap[self.corpusArray[i]].add(self.corpusArray[i + 1])        
        def getNextWordsPrediction(self, screenText,textBox1):  
            screenTextArray = screenText.split()
            size = len(screenTextArray) 
            probabilityMap = dict()
            # Unigram Case
            if(size == 0):             
                for key, value in self.unigramMap.items():
                    probabilityMap[str(key)] = float(value)
            # Bigram Case
            elif(size == 1):
                denString = screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.unigramMap.get(denString))            
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString                
                    if(self.bigramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.bigramMap.get(search))                
                    value = self.calculateProbability(num, den)               
                    probabilityMap[numString] = value
            # Trigram Case
            elif(size == 2):
                denString = screenTextArray[size - 2] + ' ' + screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.bigramMap.get(denString))           
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString              
                    if(self.trigramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.trigramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    probabilityMap[numString] = value
            # Ngram Case
            else:
                denString = screenTextArray[size - 3] + ' ' + screenTextArray[size - 2] + ' ' + screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.trigramMap.get(denString))          
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString              
                    if(self.ngramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.ngramMap.get(search))                  
                    value = self.calculateProbability(num, den)
                    probabilityMap[numString] = value
            # get max of 3 words only to show on screen
            size = min(3, len(probabilityMap))
            # get top 3 words
            sortedProbabilityMap = dict(sorted(probabilityMap.items(), key = operator.itemgetter(1), reverse = True)[:size])    
            # print these words
            for key in sortedProbabilityMap.keys():
                print(key, end='     ')
                textBox1.insert(INSERT, key+"     ")        
            print()
            print('-------------------------------------------------------------------')
            textBox1.insert(INSERT, '\n-------------------------------------------------------------------')
            textBox1.config(state=DISABLED)
        
        def calculateProbability(self, num, den):
            return float(float(num) / float(den))      
        def addWordsToTrie(self):    
            size = len(self.corpusArray)  
            for i in range(size):      
                word = str(self.corpusArray[i])
                node = self.root 
                for char in word:         
                    charFound = False        
                    for child in node.children:            
                        if char == child.char:
                            node = child
                            charFound = True
                            break             
                    if not charFound:
                        newNode = TryNode(char)
                        node.children.append(newNode)
                        node = newNode         
                node.wordFinished = True            
        def getLastWordFromSentence(self, screenText):           
            screenTextArray = screenText.split()
            size = len(screenTextArray)           
            return screenTextArray[size - 1]           
        def getAllWordsAfterPrefix(self, node, prefix):
            self.getLargestCommonPrefix(node, prefix)       
        def getLargestCommonPrefix(self, root, word):            
            node = root
            prefix = ""           
            for char in word:               
                charFound = False               
                for child in node.children:                 
                    if char == child.char:
                        node = child
                        charFound = True
                        prefix = prefix + child.char
                        break                
                if not charFound:
                    return self.DFSOnTrie(node, prefix)            
            return self.DFSOnTrie(node, prefix)         
        def DFSOnTrie(self, node, prefixNow):        
            if node.wordFinished:
                self.wordList.append(prefixNow)        
            for child in node.children:
                self.DFSOnTrie(child, prefixNow + child.char)             
        def getTopFrequentWords(self,textBox1):           
            frequencyMap = dict()           
            for word in self.wordList:             
                frequencyMap[word] = self.unigramMap.get(word)             
            size = min(3, len(frequencyMap))        
            sortedFrequencyMap = dict(sorted(frequencyMap.items(), key = operator.itemgetter(1), reverse = True)[:size])        
            for key in sortedFrequencyMap.keys():
                print(key, end='     ')
                textBox1.insert(INSERT, key+"     ")        
            print()
            print('-------------------------------------------------------------------')
            textBox1.insert(INSERT, '\n-------------------------------------------------------------------')
            textBox1.config(state=DISABLED)       
        def clearWordList(self):            
            self.wordList = []         
        def __init__(self):       
            self.unigramMap = dict()
            self.bigramMap = dict()
            self.trigramMap = dict()
            self.ngramMap = dict()
            self.nextWordsListMap = dict()       
            self.root = TryNode('*')
            self.corpusArray = self.getStringArrayFromCorpus('Big.txt')        
            self.makeUnigramMap()
            self.makeBigramMap()
            self.makeTrigramMap()
            self.makeNgramMap()
            self.makeNextWordsListMap()
            self.addWordsToTrie()       
            # To store results everytime a button is pressed.
            self.wordList = []
class Predict:          
    def nextFunction(self, textBox, nwp,textBox1):
        print('Top words predicted are: ')
        textBox1.config(state=NORMAL)
        textBox1.delete("1.0", 'end-1c')
        textBox1.insert(INSERT, "Top words predicted are: \n")
        nwp.getNextWordsPrediction(textBox.get("1.0", 'end-1c'),textBox1)
    def completionFunction(self, textBox, nwp,textBox1):       
        print('Any of the following words you want: ')
        textBox1.config(state=NORMAL)
        textBox1.delete("1.0", 'end-1c')
        textBox1.insert(INSERT, "Any of the following words you want: \n")
        prefix = nwp.getLastWordFromSentence(textBox.get("1.0", 'end-1c'))
        nwp.getAllWordsAfterPrefix(nwp.root, prefix)
        nwp.getTopFrequentWords(textBox1)
        nwp.clearWordList()
    def correctionFunction(self, textBox, nwp,textBox1):      
        print('Did you mean? ')
        textBox1.config(state=NORMAL)
        textBox1.delete("1.0", 'end-1c')
        textBox1.insert(INSERT, "Did you mean? \n")
        lastWord = nwp.getLastWordFromSentence(textBox.get("1.0", 'end-1c'))
        nwp.getAllWordsAfterPrefix(nwp.root, lastWord)
        nwp.getTopFrequentWords(textBox1)
        nwp.clearWordList()
                
    def __init__(self):                
        nwp = Corpus()       
        main = tk.Tk()
        main.resizable(True, True)
        frame = tk.Frame(main, width = 880, height = 800)
        frame.pack()
        self.canvas = tk.Canvas(frame,width = 780, height = 700) 
        self.canvas.pack()
        main.title("NLP Application")  
        l3 = Label(main, text="Enter the message here: \n",font = ('times new roman',12,'bold'))
        l3.place(x=40,y=80,height = 30)
        textBox = tk.Text(self.canvas)
        textBox.place(x = 40, y = 110, height = 160, width = 700)       
        l5 = Label(main, text="Output Suggestions: \n",font = ('times new roman',12,'bold'))
        l5.place(x=40,y=430,height = 30)
        textBox1 = tk.Text(self.canvas)
        textBox1.place(x = 40, y = 460, height = 160, width = 700)
        textBox1.config(state=DISABLED)
        nextButton = tk.Button(main, text = 'Next',activeforeground='white',activebackground='black', command = lambda: self.nextFunction(textBox, nwp,textBox1))
        nextButton.place(x = 260, y = 330, height = 30, width = 120)       
        completeButton = tk.Button(main, text = 'Complete',activeforeground='white',activebackground='black', command = lambda: self.completionFunction(textBox, nwp,textBox1))
        completeButton.place(x = 390, y = 330, height = 30, width = 120)      
        correctButton = tk.Button(main, text = 'Correct',activeforeground='white',activebackground='black', command = lambda: self.correctionFunction(textBox, nwp,textBox1))
        correctButton.place(x = 325, y = 380, height = 30, width = 120)                
        main.mainloop()
        
class Driver:
    Predict()
