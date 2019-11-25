from pycipher import Vigenere
import random
import string
import re
import sys
import collections
from ngram_score import ngram_score
from itertools import permutations

def ic_calculate(ctext):
    max_avgIC = 0
    max_KLEN = 0
    # Calculate the AVG I.C.
    for KLEN in range(1, 20):
        list_output = []
        for count in range(0, KLEN):
            output = ctext[count]
            for i in range(count+1, len(ctext)):
                if (i % KLEN == count):
                    output += ctext[i]
            list_output.append(output)

        # Find avg IC 
        sumIC = 0
        for output in list_output:
            
            N            = len(output)
            freqs        = collections.Counter( output )
            alphabet     =  map(chr, range( ord('A'), ord('Z')+1))
            freqsum      = 0.0

            # Do the math
            for letter in alphabet:
                freqsum += freqs[ letter ] * ( freqs[ letter ] - 1 )

            if (N == 1): continue
            IC = freqsum / ( N*(N-1) )
            sumIC += IC 

        avgIC = sumIC / len(list_output)
        if avgIC > max_avgIC:
            max_avgIC = avgIC
            max_KLEN = KLEN

    return max_KLEN
    # print "\nMAX AVG IC = ",max_avgIC," and key length = ",max_KLEN,"\n"

def resolver(ctext):
    ctext = re.sub(r'[^A-Z]','',ctext.upper())

    fitness = ngram_score('quadgrams.txt') # load quadgram statistics
    
    KLEN = ic_calculate(ctext)

    parentkey = list('A'*(KLEN))
    maxscore = -99e9
    parentscore = maxscore

    deciphered = Vigenere(parentkey).decipher(ctext)
    parentscore = fitness.score(deciphered)

    result = ""

    while 1:
        count = 0
        for count in range(0, KLEN):
            for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ',1):
                child = parentkey[:]
                child[count] = ''.join(i)
                deciphered = Vigenere(child).decipher(ctext)
                score = fitness.score(deciphered)
                if score > parentscore:
                    parentscore = score
                    parentkey = child[:]

        if parentscore>maxscore:
            maxscore = parentscore

        ss = Vigenere(parentkey)

        plaintext = ss.decipher(ctext)
        if plaintext == result:
            break
        else: 
            result = plaintext
    
    key = ''.join(parentkey)
    out = dict(key=key, text=result)
    return out