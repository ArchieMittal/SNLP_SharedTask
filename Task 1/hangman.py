# -*- coding: utf-8 -*-

import codecs

import numpy as np
import string
import editdistance
import pickle
from string import ascii_lowercase
import random
from collections import defaultdict
import csv
import math
        

def trainModel():
    unigramCount = 0
    bigramCount = 0
    firstCount = 0
    trainingFile = open("train.txt", encoding="utf8")
    firstProb = np.zeros((26,1), dtype = float)
    unigramProb = np.zeros((26,1), dtype=float)
    bigramProb = np.zeros((27,26), dtype = float)
    trigramProb = np.zeros((27,26,26), dtype = float)
    for line in trainingFile:
        word = line.strip()

        try:
            firstProb[ord(word[0]) - 97] = firstProb[ord(word[0]) - 97] + 1
            firstCount = firstCount + 1
        except:
            continue
        
        for ch in word:
            try:
                unigramProb[ord(ch) - 97] = unigramProb[ord(ch) - 97] + 1
                unigramCount = unigramCount + 1
            except:
                continue
        for i in range(1, len(word)):
            try:
                bigramProb[ord(word[i]) - 97][ord(word[i - 1]) - 97] = bigramProb[ord(word[i]) - 97][ord(word[i - 1]) - 97] + 1
                bigramProb[26][ord(word[i -1]) - 97] = bigramProb[26][ord(word[i -1]) - 97] + 1
            except:
                continue
        for i in range(2, len(word)):
            try:
                trigramProb[ord(word[i]) - 97][ord(word[i-1] - 97)][ord(word[i-2]) - 97] = trigramProb[ord(word[i]) - 97][ord(word[i-1] - 97)][ord(word[i-2]) - 97] + 1
            except:
                continue

   
    '''for i in range(26):    
        firstProb[i] = firstProb[i] / firstCount
        
    for i in range(26):
        unigramProb[i] = unigramProb[i] / unigramCount

    for i in range(26):
        for j in range(26):
            for k in range(26):
                trigramProb[i][j][k] = trigramProb[i][j][k] / bigramProb[j][k]

    for i in range(26):
        for j in range(26):
            bigramProb[i][j] = bigramProb[i][j] / bigramProb[26][j]'''
   
    return firstProb, unigramProb, bigramProb, trigramProb




def getCharacter(maskedWord, guesses):
    
    probabilities = []
    predictedChars = []

    temp = firstProb

    if(maskedWord[0] == '_'):
        maxProb = (max(temp))
        char = chr(temp.argmax() + 97)
        while char in guesses and maxProb != -1:
            temp[temp.argmax()] = -1
            maxProb = (max(temp))
            char = chr(temp.argmax() + 97)
        if maxProb != -1:
            probabilities.append(maxProb)
            predictedChars.append(char)
   
    for i in range(2, len(maskedWord)-2):
        maxProb = 0.0
        if maskedWord[i-2] != '_' and maskedWord[i-1]!= '_' and maskedWord[i] == '_' and maskedWord[i+1] != '_' and maskedWord[i+2] != '_':
            for j in range(26):
                
                if chr(j + 97) not in guesses:
                    prob = trigramProb[j][ord(maskedWord[i-1]) - 97][ord(maskedWord[i-2]) - 97] * 5 * trigramProb[ord(maskedWord[i+2]) - 97][ord(maskedWord[i+1]) - 97][j] + 3 * bigramProb[j][ord(maskedWord[i-1]) - 97] * bigramProb[ord(maskedWord[i+1]) - 97][j]
                  
                    if prob > maxProb:
                        maxProb = prob
                        char = chr(j + 97)
        
        elif maskedWord[i-2] != '_' and maskedWord[i-1]!= '_' and maskedWord[i] == '_' and maskedWord[i+1] != '_':
            for j in range(26):
                
                if chr(j + 97) not in guesses:
                    prob = trigramProb[j][ord(maskedWord[i-1]) - 97][ord(maskedWord[i-2]) - 97] * 1.2 + 3 * bigramProb[j][ord(maskedWord[i-1]) - 97] * bigramProb[ord(maskedWord[i+1]) - 97][j]
                    
                    if prob > maxProb:
                        maxProb = prob
                        char = chr(j + 97)
        elif maskedWord[i-1]!= '_' and maskedWord[i] == '_' and maskedWord[i+1] != '_' and maskedWord[i+2] != '_':
            for j in range(26):
                
                if chr(j + 97) not in guesses:
                    prob = trigramProb[ord(maskedWord[i+2]) - 97][ord(maskedWord[i+1]) - 97][j] * 1.2 + 3 * bigramProb[j][ord(maskedWord[i-1]) - 97] * bigramProb[ord(maskedWord[i+1]) - 97][j]
                   
                    if prob > maxProb:
                        maxProb = prob
                        char = chr(j + 97)
        elif(maskedWord[i-1] != '_' and maskedWord[i] == '_' and maskedWord[i+1] != '_'):
    
            for j in range(26):
                
                if chr(j + 97) not in guesses:
                    prob = 3 * bigramProb[j][ord(maskedWord[i-1]) - 97] * bigramProb[ord(maskedWord[i+1]) - 97][j]
                  
                    if prob > maxProb:
                        maxProb = prob
                        char = chr(j + 97)
            if maxProb == 0:
                continue
        elif maskedWord[i-1]!= '_' and maskedWord[i] == '_':
            #print ("2")
            for j in range(26):
                
                if chr(j + 97) not in guesses:
                    prob = 3 * bigramProb[j][ord(maskedWord[i-1]) - 97] 
                   
                    if prob > maxProb:
                        maxProb = prob
                        char = chr(j + 97)
        elif(maskedWord[i] == '_' and maskedWord[i+1] != '_'):
            #print ("3")
            for j in range(26):
                if chr(j + 97) not in guesses:
                    prob = 3 * bigramProb[ord(maskedWord[i+1]) - 97][j]
                    if prob > maxProb:
                        maxProb = prob
                        char = chr(j + 97)
        else:
            continue
        
        probabilities.append(maxProb)
        predictedChars.append(char)
  
    if probabilities:
        winchar = max(probabilities)
      
        return predictedChars[probabilities.index(winchar)]
    else:
        predictedChar = getRandomChar(guesses)
        return predictedChar


def getRandomChar(guesses):
    letters = []
    highPriorityLetters = ['u','a','e','o','i','y','c','p']
    for c in ascii_lowercase:
        letters.append(c)
    random.shuffle(letters)
    letters = highPriorityLetters + letters
    for l in letters:
        if l not in guesses:
            return l


def startHangman(word):
    guesses = []
    wrongGuess = 0
    maskedWord = ['_']*len(word)
    
    while wrongGuess < 8 and '_' in maskedWord:
        predictedCharacter = getCharacter(maskedWord, guesses)
        
        if predictedCharacter not in guesses:
           
            guesses.append(predictedCharacter)
        if predictedCharacter in word:
            
            for i in range(0, len(word)):
                if word[i] == predictedCharacter:
                   
                    maskedWord[i] = predictedCharacter
        else:
            wrongGuess += 1
    return maskedWord, guesses


def loss(solution, prediction):
    # find the levenshtein distance between the two words
    return editdistance.eval(solution, prediction)


firstProb, unigramProb, bigramProb, trigramProb = trainModel()

if __name__ == "__main__":
    
    count = 0
    distance = 0.0
    cc = 0
    with open("testt.txt","r") as infile :
        with open('output.tsv', 'w') as tsvfile:
            spamwriter = csv.writer(tsvfile, delimiter='\t')
            spamwriter.writerow(["Id","Output","PredictedCharacters"])
            for word in infile:
                
                word = word.strip().split(',')[1]
                
                count += 1
                if count == 1 :
                    continue
                print (count)
                predictedWord = ""
                maskedWord, guesses = startHangman(word)
               
                for item in maskedWord :
                    predictedWord+=item
                    
                if predictedWord != word:
                    print (predictedWord,word,guesses)
                    
                else:
                    cc+=1
                distance += loss(word, predictedWord)
                
                spamwriter.writerow([count-1,predictedWord,guesses])
               
    print (distance/(count-1))
    print (cc)

