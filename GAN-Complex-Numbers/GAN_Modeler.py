################################################################################################################################################
#                                                                                                                                              #
#   Autor: Dr. A. Schelle (alexej.schelle.ext@iu.org). Copyright : IU Internationale Hochschule GmbH, Juri-Gagarin-Ring 152, D-99084 Erfurt    #
#                                                                                                                                              #
################################################################################################################################################

# PYTHON ROUTINE zur Darstellung von GAN-Netzwerken mit komplexe Zahlen in der Gaußschen Zahlenebene #

import os
import sys
import statistics
import math
import random
import matplotlib.pyplot as plt

# Definition eines Generators für das GAN-Modell

def Generator(length, input_key, train):

    output_key = [0]*length

    for j in range(0, length): # Generiere einen zufälligen binären Schlüssel zum Abgleich mit dem Referenzschlüssel

        output_key[j] = random.randint(0,1)

    return(output_key)

# Definition eines Diskriminators für das GAN-Modell

def Diskriminator(length, input_key, ideal_key):

    difference = [0]*length

    for j in range(0, length):

        difference[j] = math.fabs(ideal_key[j] - input_key[j]) # Berechne die Abweichung zwischen Referenzschlüssel und dynamisch generiertem Schlüssel

    return(difference)

# Definition einer Schaltung für das GAN-Modell

def CNOT(length, input_key): # Definiert eine paarweise Invertierung der Ausgangskonfiguration

    output_key = [0]*length
        
# Here is the main part to integrate the specific LOGIC of the GAN

    for k in range(1, M):

      # NOT-Schaltung      
      #
      #  if (input_key[k] == 0): input_key[k] = 1
      #  else: input_key[k] = 0 
      #

      # CNOT-Schaltung:      

        if (input_key[k] == 0 and input_key[k-1] == 0): input_key[k-1] = 0
        if (input_key[k] == 0 and input_key[k-1] == 1): input_key[k-1] = 1
        if (input_key[k] == 1 and input_key[k-1] == 0): input_key[k-1] = 1
        if (input_key[k] == 1 and input_key[k-1] == 1): input_key[k-1] = 0
      
        output_key[k] = input_key[k]
        
    return output_key

# Definition eines GAN-Modells

def GAN(length, initial_key, reference_key):

    k = 0
    uncertainty = 2

    GAN_Key = [0]*length # Definiere den GAN-Schlüssel mit der Variable GAN_Key als Pythonliste mit der gleichen Anzahl von Elementen wie die anderen Keys 
        
    while(True):

        sum = 0.0
        initial_key = CNOT(length, initial_key)

        if (k == 0): L = Generator(length, initial_key, reference_key) 

        if (k > 0): 

            GAN_Key = Generator(length, L, M)
            initial_key = GAN_Key
            L = CNOT(length, GAN_Key)
        
        M = Diskriminator(length, L, reference_key)

        for j in range(0, length):

            sum = sum + math.fabs(M[j])

        k = k + 1

        if (sum == uncertainty): # Hier wird die Genaugkeit an das GAN festgelegt (Parameter uncertainty)

            return(initial_key)
            break

# Definition einer Funktion zur Generierung eines Referenz-Schlüssels

def GenerateReferenceKey(keysize):

    for j in range(0, keysize): # Generiere einen zufälligen binären Schlüssel als Referenzwert (entspricht externem und unbekanntem Referenzwert)

        R[j] = random.randint(0,1)
    
    return R

# Definition einer Funktion zur Generierung eines Schlüssel-Anfangswerts

def GenerateInitialKey(keysize):

    for j in range(0, keysize): # Generiere einen zufälligen binären Schlüssel als Startwert

        K[j] = random.randint(0,1)

    return K

S = 2500 # Anzahl der GAN-Konfigurationen (Anzahl der komplexen Zahlen in der Gaußschen Zahlenebene)   
M = 16 # Länge des Schlüssels in Einheiten von Bits

K = ['']*M # Definiere den Schlüssel K als Pythonliste mit der gleichen Anzahl von Elementen wie S     
R = ['']*M # Definiere den Schlüssel R als Pythonliste mit der gleichen Anzahl von Elementen wie S  

fS = ['']*S # Definiere eine Python Liste für den kodierten Zeichenstring als verschlüsselte Zahlenfolge
fSS = '' # Definiere eine Python Liste für den dekodierten Zeichenstring als entschlüsselte Zahlenfolge

dkey = [] # Python-Liste zur Speicherung 
ARR_Keys = []
COMPLEX_Keys_Real = []
COMPLEX_Keys_Imag = []

dvalue = 0.0
fvalue = 0.0

print('Number of Key Elements : ', S)

for k in range(0, S):

    print('Generate Key Element Nr. ', k)

    K = GenerateInitialKey(M) # Generiere den ersten Schlüssel als Startwert für das GAN
    R = GenerateReferenceKey(M) # Generiere einen Referenzschlüssel (anfangs dengelichen Keywert)
        
    K = R # Lege eine Anfangsbedingung mit K = R fest     
    ARR_Keys = ARR_Keys + R # Speichere jeweils den Referenzkey, der modulu CNOT den Key K erzeugt

    key = GAN(M, K, R) # Modelliere ein GAN-Netzwerk zur Rekonstruktion eines möglichen Eingangssignale (bisher unbekannt)

    dvalue = 0.0
    fvalue = 0.0

    for l in range(0, len(key)):

        dvalue = dvalue + 2**l*key[l]

    for l in range(0, len(key)):

        fvalue = fvalue + 2**l*R[l]
        
    dkey.append(int(dvalue))

    COMPLEX_Keys_Real.append(int(dvalue))
    COMPLEX_Keys_Imag.append(int(fvalue))

# Darstellung der komplexen Zahlen in der Gaußschen Zahlenebene

plt.figure(1)
plt.hist2d(COMPLEX_Keys_Real, COMPLEX_Keys_Imag, bins = 300)
plt.tick_params(axis='both', which='major', labelsize = 16)
plt.xlabel('Real Part', fontsize = 18)
plt.ylabel('Imaginary Part', fontsize = 18)
plt.savefig('fig_complex.png')