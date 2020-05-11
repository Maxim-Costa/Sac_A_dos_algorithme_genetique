"""
Maxim Costa
probleme sac a dos 

V 2.1
"""

# doit etres installer sur l'ordinateur pour fonctionner (import matplotlib.pyplot as plt)
import matplotlib.pyplot as plt

from random import *
from items import ItemName


class Sac(object):
    def __init__(self, v, w):
        self.valeur = v
        self.poid = w
        self.name = OBJETSNAME.pop(randint(0, len(OBJETSNAME)-1))


""" Config general du programme """
POIDMAXOBJET = 20
POIDMINOBJET = 1
VALEURMAXOBJET = 20
VALEURMINOBJET = 1
POIDSAC = 24
SACCAPACITE = 100
""" essey plusieur valeur """
POPULATIONTAILLE = 200
NBGENERATIONMAX = 4000
NBPARENTNEXTGENE = 0.2
MUTATIONCHANCE = 0.08
PARENTCHANCENEXTGENE = 0.05
OBJETSNAME = ItemName.copy()
OBJETS = [Sac(randint(POIDMINOBJET, POIDMAXOBJET), randint(VALEURMINOBJET, VALEURMAXOBJET))
          for i in range(POIDSAC)]
"""***********END********** """

# doit etres installer sur l'ordinateur pour fonctionner (import matplotlib.pyplot as plt)


def GraphPrint(generation, fitnessMeanHistory, fitnessMaxHistory):
    plt.plot(list(range(generation)),
             fitnessMeanHistory, label='Mean Fitness')
    plt.plot(list(range(generation)),
             fitnessMaxHistory, label='Max Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()


def populationDepart(nb):
    """
    input: 
        type: int
        nombre d'element a generer pour former une population

    output:
        list(list(bool))
        return une population type 
    """
    return [[bool(randint(0, 1)) for _ in range(0, len(OBJETS))] for _ in range(nb)]


def fitness(cible):
    """
    input: 
        type: list(bool)
        un element de la population 

    output: 
        type: int
        la valeur de cette element,
        si son poid et superieur au poid max :
            alors on renvoie 0
    """
    PoidToto, ValeurToto = 0, 0
    for gene, obj in enumerate(cible):
        if obj:
            PoidToto += OBJETS[gene].poid
            ValeurToto += OBJETS[gene].valeur
    if PoidToto > SACCAPACITE:
        return 0
    else:
        return ValeurToto


def Mutation(cible):
    """
    input: 
        type: list(bool)
        1 element de la population 

    output: 
        type: list(bool)
        le meme element de la population mais avec un gene au hasard 
    """
    gene = randint(0, len(cible)-1)
    cible[gene] = not cible[gene]
    return cible


def Evolution(population, best):
    """
    input:
        list(list(bool)
        l'ensemble de la population

    mathode :
        part 1:
            On selection au hasard quelque parent non selection pour faire partie de la prochaine generation
        part 2:
            on selection les un % des meilleur parent de le Population actuel et on le mut
        part 3:
            on créer des enfant pour garder la même taille de populations grace a la moitier de deux parent selectionner

    output: 
        list(list(bool)
        la nouvelle generation de cette population
    """
    NbParent = int(NBPARENTNEXTGENE*len(population))
    Parents = population[:NbParent]
    NonParents = population[NbParent:]

    for Parent in NonParents:
        if PARENTCHANCENEXTGENE > random():
            Parents.append(Parent)

    for index, Parent in enumerate(Parents):
        if MUTATIONCHANCE > random():
            Parents[index] = Mutation(Parent)

    Enfants = []
    NbEnfant = len(population) - len(Parents) - 1
    for _ in range(NbEnfant):
        Male = Parents[randint(0, len(Parents)-1)]
        Femelle = Parents[randint(0, len(Parents)-1)]
        NbGene = len(Male)//2
        Enfant = Male[:NbGene] + Femelle[NbGene:]
        if MUTATIONCHANCE > random():
            Enfant = Mutation(Enfant)
        Enfants.append(Enfant)
    Parents.extend(Enfants)
    return Parents+[best]


def outOBJETSPrint():
    for i in OBJETS:
        print(i.name, end=" "*(35-len(i.name)))
    print("\n")
    for i in OBJETS:
        print(i.valeur, end=" "*(35-len(str(i.valeur))))
    print("\n")
    for i in OBJETS:
        print(i.poid, end=" "*(35-len(str(i.poid))))
    print("\n\n")


def outFITNESSPrint(populations):
    space = 6*POIDSAC+30
    print(
        f"{populations[0]}{' '*(space-len(str(populations[0])))}{fitness(populations[0])}")


def sortPOPULATIONS(populations):
    return sorted(populations, key=lambda population: fitness(population), reverse=True)


def main():
    generation = 0
    populations = populationDepart(POPULATIONTAILLE)
    sortPOPULATIONS(populations)
    fitnessMeanHistory = []
    fitnessMaxHistory = []

    for _ in range(NBGENERATIONMAX):

        populations = Evolution(populations, populations[0].copy())
        generation += 1
        populations = sortPOPULATIONS(populations)

        """ *************Save for plt graph***************************** """
        fitnessMeanHistory.append(
            int(round(sum([fitness(x)for x in populations])/len(populations))))
        fitnessMaxHistory.append(fitness(populations[0]))
        """ *************Print info after sorted************************ """
        outFITNESSPrint(populations)
        """ ************************************************************ """

    print("[" + ", ".join([OBJETS[index].name for index,
                           i in enumerate(populations[0]) if i]) + "]")

    # doit etres installer sur l'ordinateur pour fonctionner (import matplotlib.pyplot as plt)
    GraphPrint(generation, fitnessMeanHistory, fitnessMaxHistory)


with open("result.txt", "w+") as outfile:
    print = outfile.write
    main()
