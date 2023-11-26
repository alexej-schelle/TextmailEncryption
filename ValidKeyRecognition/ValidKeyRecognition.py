################################################################################################################################################
#                                                                                                                                              #
#   Autor: Dr. A. Schelle (alexej.schelle.ext@iu.org). Copyright : IU Internationale Hochschule GmbH, Juri-Gagarin-Ring 152, D-99084 Erfurt    #
#                                                                                                                                              #
################################################################################################################################################

# PYTHON ROUTINE zum Vergleich von Dezimalcodes durch ein GAN-basiertes künstliches neuronales Netzwerk #

import os
import sys
import math
import random
import statistics

# Definition von Funktionen zur Verschlüsselung b kongruent a mod 52 durch GAN

def letters_to_value(x): # Definiere eine Funktion zur Abbildung von Strings auf Zahlen a kongruent b mod 52
    
    x_value = 0

    if (x == '0') : x_value = 0
    if (x == '1') : x_value = 1
    if (x == '2') : x_value = 2
    if (x == '3') : x_value = 3
    if (x == '4') : x_value = 4
    if (x == '5') : x_value = 5
    if (x == '6') : x_value = 6
    if (x == '7') : x_value = 7
    if (x == '8') : x_value = 8
    if (x == '9') : x_value = 9
    
    return x_value

def value_to_letters(x): # Definiere eine Funktion zur Abbildung von Zahlen auf Strings a kongruent b mod 52
     
    x_value = ''

    if (x == 0) : x_value = '0'
    if (x == 1) : x_value = '1'
    if (x == 2) : x_value = '2'
    if (x == 3) : x_value = '3'
    if (x == 4) : x_value = '4'
    if (x == 5) : x_value = '5'
    if (x == 6) : x_value = '6'
    if (x == 7) : x_value = '7'
    if (x == 8) : x_value = '8'
    if (x == 9) : x_value = '9'

    return x_value

def Generator(length, train):

    output_key = [0.0]*(length+1)

    for j in range(0, length): # Generiere einen zufälligen binären Schlüssel

        if (train[j] != 0.00): output_key[j] = random.randint(0,1)

    return(output_key)
    
def Diskriminator(length, input_key, ideal_key):

    difference = [0.0]*(length + 1)

    for j in range(0, length):

        difference[j] = math.fabs(int(ideal_key[j]) - int(input_key[j]))

    return(difference)

def CNOT(length, input_key): # Defines a pairwise CNOT-Operation

    output_key = [0.0]*length
    
    output_key[1] = 1.0
    output_key[2] = 1.0
        
    for k in range(0, M):

        if (input_key[k] == 1 and input_key[k-1] == 0): input_key[k-1] = 1        
        if (input_key[k] == 1 and input_key[k-1] == 1): input_key[k-1] = 0        

        output_key[k] = input_key[k]
        output_key[k-1] = input_key[k-1]

    return output_key

def GAN(length, initial_key, reference_key):

    k = 0

    while(True):

        sum = 0.0

        initial_key = CNOT(length, initial_key)

        if (k == 0): L = Generator(length, initial_key) 
        if (k > 0): L = Generator(length, M) 
        
        M = Diskriminator(length, L, reference_key)

        for j in range(0, length):

            sum = sum + M[j]

        k = k + 1

        if (sum == 0.0):

            return(initial_key)

            break

def GenerateReferenceKey(keysize):

    for j in range(0, keysize): # Generiere einen zufälligen binären Schlüssel als Referenzwert (entspricht externem und unbekanntem Referenzwert)

        K[j] = random.randint(0,1)
    
    return K
    
def GenerateInitialKey(keysize):

    for j in range(0, keysize): # Generiere einen zufälligen binären Schlüssel als Startwert

        K[j] = random.randint(0,1)

    return K

alphabet = ['0','1','2','3','4','5','6','7','8','9'] # Definiere eine Pythonliste mit Elementen aus dem deutschen Alphabet

with open("KeyDeclaration.txt") as file: # Importiere den Zeichenstring aus dem externen File mit Bezeichnung KeyDeclaration.txt

    S = file.read()
    
M = 16 # Länge des Schlüssels in Einheiten von Bits

K = ['']*M # Definiere den Schlüssel K als Pythonliste mit der gleichen Anzahl von Elementen wie S     
R = ['']*M # Definiere den Schlüssel R als Pythonliste mit der gleichen Anzahl von Elementen wie S  

fS = ['']*len(S) # Definiere eine Python Liste für den kodierten Zeichenstring als verschlüsselte Zahlenfolge
fSS = '' # Definiere eine Python Liste für den dekodierten Zeichenstring als entschlüsselte Zahlenfolge

dkey = []
dvalue = 0.0

print('Number of Key Elements: ', len(S))

trials = 10000000
difference = 0.0

for k in range(0, trials):

    print('Comparing Generated Key Element Nr. ', k)
    difference = 0.0

    K = GenerateInitialKey(M) # Generiere den ersten Schlüssel als Startwert für das GAN
    R = GenerateReferenceKey(M) # Generiere einen Referenz Schlüssel
    
    key = GAN(M, K, R) # Modelliere ein GAN-Netzwerk zur Rekonstruktion eines möglichen Eingangssignale (bisher unbekannt)
    
    for l in range(0, len(Diskriminator(len(S), key, S))):

        difference = difference + Diskriminator(len(S), key, S)[l]

    if (difference == 0.0): # Für übereinstimmende Schlüsselwerte (Dezimalcodes) wird Validität bestätigt

        print(key)
        break
        
print(' ')
print('Originaler Dezimalcode: ', S)
print(' ')
print('Referenzcode: ', key)

#########################################################
#                                                       #
#   TO DOs:                                             #
#                                                       #
#   1: Source Code anpassen für eine Vielzahl von       # 
#      Dezimalcodes                                     #
#   2: Teste die Skalierungseigenschaft als Funktion    #
#      der Bit-Größe                                    #
#   3: Komplexität der CNOT-Schaltung erhöhen           #
#                                                       #
#########################################################
