#!/usr/bin/env python
# *-* coding: UTF-8 *-*

"""
    [Index].[Spatiu][Spatiu][Numele Teoremei]
    [Numele scurt]
    [Rand nou]
    [Rand nou]
    [Teorema]
    [Rand nou]
    [Rand nou]

Exemplu:
    1.  The Irrationality of the Square Root of 2
        SQRT_2_IRRATIONAL


     |- ~rational(sqrt(&2))


"""


import os
import re
from sys import argv


def numara_aparitii(opt, patt, repw, teorema):
    contor = 0
    i = 0
    copie = str(teorema)
    linii = []
    liniecurenta = 0
    inceplinie = 0
    while i+len(patt) <= len(copie):
        turn = 0
        if copie[i] == '\n':
            liniecurenta += 1
            inceplinie = -1
        if 'i' in opt:
            if copie[i:i+len(patt)].lower() == patt.lower():
                if 'e' in opt:
                    if ((i-1 < 0 or not copie[i-1].isalnum()) and
                       (i+len(patt) > len(copie) or
                       not copie[i+len(patt)].isalnum())):
                        turn += 1
                        linii.append((liniecurenta, inceplinie,
                                     inceplinie+len(repw)))
                else:
                    turn += 1
                    linii.append((liniecurenta, inceplinie,
                                 inceplinie+len(repw)))
                if 's' in opt and turn > 0:
                    copie = copie[:i]+repw+copie[i+len(patt):]
                    i = i+len(repw)-1
                    inceplinie += (len(repw)-1)
                contor += turn
        else:
            if copie[i:i+len(patt)] == patt:
                if 'e' in opt:
                    if ((i-1 < 0 or not copie[i-1].isalnum()) and
                       (i+len(patt) > len(copie) or
                       not copie[i+len(patt)].isalnum())):
                        turn += 1
                        linii.append((liniecurenta, inceplinie,
                                     inceplinie+len(repw)))
                else:
                    turn += 1
                    linii.append((liniecurenta, inceplinie,
                                 inceplinie+len(repw)))
                if 's' in opt and turn > 0:
                    copie = copie[:i]+repw+copie[i+len(patt):]
                    i = i+len(repw)-1
                    inceplinie += (len(repw)-1)
                contor += turn
        i += 1
        inceplinie += 1
    return (contor, copie, linii)


def extrage_bloc_formula_din_fisier(*args):
    if not os.path.isfile(args[len(args)-1]):
        print "Not a file!"
    else:
        if len(args) < 5:
            opt = args[1]
            patt = args[2]
            repw = patt
            nume = args[3]
        else:
            if len(args) < 6:
                opt = args[1]
                patt = args[2]
                repw = args[3]
                nume = args[4]
        fisier = open(nume, "r")
        continut = fisier.read()
        linii = continut.splitlines()
        start = -1
        teorema = ""
        contor = 0
        continutmodificat = ""
        for i in range(len(linii)):
            matchObj = re.match(r'[ ]\d+[.][ ]{2}', linii[i], re.X)
            if matchObj:
                if start != -1:
                    pereche = numara_aparitii(opt, patt, repw, teorema)
                    contor += pereche[0]
                    continutmodificat += pereche[1]
                    if pereche[0] > 0 and 'c' not in opt:
                        linsunt = pereche[1].splitlines()
                        for ln in pereche[2]:
                            print (os.path.abspath(args[len(args)-1])+":" +
                                   str(i-len(linsunt)+1+ln[0])+":" +
                                   (linsunt[ln[0]])[:ln[1]]+"\033[1;32m" +
                                   (linsunt[ln[0]])[ln[1]:ln[2]]+"\033[1;m" +
                                   (linsunt[ln[0]])[ln[2]:])
                    teorema = linii[i]+'\n'
                    start = i
                else:
                    start = i
                    teorema = linii[i]+'\n'
            else:
                teorema += linii[i]+'\n'
        if 'c' in opt:
            print os.path.abspath(args[len(args)-1])+":",
            print contor, "aparitii"
        fisier.close()
        fisier = open(nume, "w")
        fisier.write(continutmodificat)
        fisier.close()


def afis_recursiv(*args):

    """Recursiv cauta in fiecare fisier avand argumentele"""

    argument = args[len(args)-1]
    if os.path.isdir(os.path.abspath(argument)):
        for fisier in os.listdir(argument):
            if os.path.isdir(os.path.join(argument, fisier)):
                afis_recursiv(list(args[:len(args)-1]) +
                              [os.path.join(argument, fisier)])
            else:
                argnoi = list(args[:len(args)-1]) + [
                                os.path.join(argument, fisier)]
                extrage_bloc_formula_din_fisier(*argnoi)
    else:
        print "Not a folder!"


def getKey(item):

    """Folosit la ordonarea descrescatoare"""

    return item[1]


def get_file_dct(nume):
    fisier = open(nume, "r")
    continut = fisier.read()
    dictionar = {}
    for linie in continut.splitlines():
        for cuvant in linie.split():
            if cuvant.isalnum():
                if cuvant not in dictionar:
                    dictionar[cuvant] = 1
                else:
                    dictionar[cuvant] += 1
    lista = []
    for item in dictionar.items():
        lista.append(item)
    lista = sorted(lista, key=getKey, reverse=True)
    for i in range(5):
        print lista[i]
    fisier.close()


if __name__ == "__main__":
    if len(argv) < 4:
        print "Argumente: [opt] [string] [file]"
        print "Argumente: [opt+s] [string] [repwith] [file]"
    else:
        if 't' in argv[1]:
            get_file_dct(argv[len(argv)-1])
        else:
            if 'r' in argv[1]:
                afis_recursiv(*argv)
            else:
                extrage_bloc_formula_din_fisier(*argv)

