################################################################################################################################################
#                                                                                                                                              #
#   Autor: Dr. A. Schelle (alexej.schelle.ext@iu.org). Copyright : IU Internationale Hochschule GmbH, Juri-Gagarin-Ring 152, D-99084 Erfurt    #
#                                                                                                                                              #
################################################################################################################################################

# PYTHON ROUTINE zum Auffinden von spezifischen Zahlen- oder Textstrukturen durch ein GAN-basiertes künstliches neuronales Netzwerk #

# Bemerkung: Im vorliegenden Source Code ist ein einfaches Beispiel zur Modellierung eines GAN zum Auffinden von "Nullstrukturen" implementiert, d. h. das GAN erkennt Schlüssel, bei denen alle Werte auf Null stehen

import os
import sys
import math
import random
import statistics

# Definition von Funktionen zur Verschlüsselung b kongruent a mod 52 durch GAN

def Generator(length, input_key, train):

    output_key = [0.0]*(length+1)

    for j in range(0, length): # Generiere einen zufälligen binären Schlüssel

        if (train[j] != 0.00): output_key[j] = random.randint(0,1)
        else: output_key[j] = input_key[j]

    return(output_key)
    
def Diskriminator(length, input_key, ideal_key):

    difference = [0.0]*(length + 1)

    for j in range(0, length):

        difference[j] = math.fabs(ideal_key[j] - input_key[j])

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
    GAN_Key = ['']*length # Definiere den GAN-Schlüssel GAN_Key als Pythonliste mit der gleichen Anzahl von Elementen wie die anderen Keys 
   
    while(True):

        sum = 0.0

        initial_key = CNOT(length, initial_key)

        if (k == 0): L = Generator(length, initial_key, GAN_Key) 
        if (k > 0): L = CNOT(length, Generator(length, L, M)) # Bemerkung: Hier hat noch die CNOT-Funktion gefehlt.
    
        M = Diskriminator(length, L, reference_key)

        for j in range(0, length):

            sum = sum + M[j]

        k = k + 1
        
        if (sum == 0.0):

            return(GAN_Key)
            break

        else:

            GAN_Key = L

def GenerateReferenceKey(keysize):

    for j in range(0, keysize): # Generiere einen zufälligen binären Schlüssel als Referenzwert (entspricht externem und unbekanntem Referenzwert)

        K[j] = random.randint(0,1)
    
    return K
    
def GenerateInitialKey(keysize):

    for j in range(0, keysize): # Generiere einen zufälligen binären Schlüssel als Startwert

        K[j] = random.randint(0,1)

    return K

alphabet = ['0','1','2','3','4','5','6','7','8','9'] # Definiere eine Pythonliste mit Elementen aus dem deutschen Alphabet

M = 64 # Länge des Schlüssels in Einheiten von Bits

K = ['']*M # Definiere den Schlüssel K als Pythonliste mit der gleichen Anzahl von Elementen wie S     
R = ['']*M # Definiere den Schlüssel R als Pythonliste mit der gleichen Anzahl von Elementen wie S  

dkey = []
dvalue = 0.0

iterations = 10000000

for k in range(0, iterations):

    print('Generate Key Element Nr. ', k)

    R = GenerateReferenceKey(M) # Generiere den ersten Schlüssel als Startwert für das GAN
    K = GenerateInitialKey(M) # Generiere einen Referenzschlüssel

    dkey = GAN(M, K, R) # Modelliere ein GAN-Netzwerk zur Rekonstruktion eines möglichen Eingangssignals (bisher unbekannt)
    dvalue = 0.0

    for l in range(0, M):

        dvalue = dvalue + (float(dkey[l]) - float(R[l]))
    
    print(dvalue)

    if (dvalue == 0.00): 
        
        print(dkey)

        break
        
#########################################################
#                                                       #
#   TO DOs:                                             #
#                                                       #
#   1: Source Code anpassen für komplexere              # 
#      Zahlenstrukturen                                 #
#   2: Anpassung für Analyse von Textstrukturen         #
#   3: Schaltung entsprechend anpassen                  #
#                                                       #
#########################################################
