import random
import glob
import shutil
import os


# Jet de des
def diceRoll():
    return random.randint(1,4) + random.randint(1,6)

# Vide du dossier 'Partie'
def clearPartie():
    path = 'Partie'
    for card in os.listdir(path):
        os.remove(os.path.join(path, card))

# Preparation de la partie de Shadow Hunters
def prepSH(players):
    #Nombre de joueurs et joueur qui commence
    N = len(players)
    
    # Tirage au sort des personnages
    A = ['Allie']#, 'Agnes']
    C = ['Charles']#, 'Catherine']
    D = ['Daniel']#, 'David']
    
    E = ['Emi']#, 'Ellen']
    F = ['Franklin']#, 'Fu-ka']
    G = ['Georges']#, 'Gregor']
    
    L = ['Loup-Garou']#, 'Liche']
    M = ['Metamorphe']#, 'Momie']
    V = ['Vampire']#, 'Valkyrie']
    
    neutres = [random.choice(A), random.choice(C), random.choice(D)]
    hunters = [random.choice(E), random.choice(F), random.choice(G)]
    shadows = [random.choice(L), random.choice(M), random.choice(V)]

    if N == 8:
        del neutres[random.randint(0,2)]
    elif N == 7:
        del hunters[random.randint(0,2)]
        del shadows[random.randint(0,2)]
    elif N == 6:
        del neutres[random.randint(0,2)]
        del hunters[random.randint(0,2)]
        del shadows[random.randint(0,2)]
    elif N == 5:
        neutres = [random.choice(neutres)]
        del hunters[random.randint(0,2)]
        del shadows[random.randint(0,2)]
    elif N == 4:
        neutres = []
        del hunters[random.randint(0,2)]
        del shadows[random.randint(0,2)]
    elif N == 3:
        neutres = [random.choice(neutres)]
        hunters = [random.choice(hunters)]
        shadows = [random.choice(shadows)]
    elif N == 2:
        neutres = []
        hunters = [random.choice(hunters)]
        shadows = [random.choice(shadows)]
    elif N == 1:
        neutres = []
        hunters = [random.choice(hunters)]
        shadows = []

    persos = neutres + hunters + shadows
    
    # Joueur qui commence
    first = players[random.randint(0, N-1)]

    # Copie des personnages selectionnes
    src_dir = "Personnages"
    dst_dir = "Partie"
    for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
        perso = jpgfile[12:].split('.')[0]
        if perso in persos:
            shutil.copy(jpgfile, dst_dir)
    
    # Repartition anonyme des personnages
    path = 'Partie'
    for card in os.listdir(path):
        playerIndex = random.randint(0, N-1)
        os.rename(os.path.join(path,card), os.path.join(path, players[playerIndex]+'.jpg'))
        del players[playerIndex]
        
    return first
        