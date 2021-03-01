########
import pygame
from pygame.locals import *
import random

class Cellule:
    """
    définition d'une cellule
    """
    
    def __init__(self,x, y):
        """
        créer une cellule positionnée en (x=colonne, y=ligne)
        """        
        self.x = x
        self.y = y
        #les murs sont dans l'ordre : S, E. 
        #la valeur est à True si un mur est présent, False sinon
        self.murs = {'N': True, 'O': True}
        
########      
class Grille :
    """
    Classe permettant de générer un labyrinthe avec la méthode "arbre binaire"
    """
    def __init__(self, nx, ny):
        """
        construction d'une grille labyrinthique de dimension (nx - largeur, ny - hauteur)
        """
        self.nx = nx
        self.ny = ny
        self.grille = []
        for x in range(nx):
            GrilleCol=[] #Création d'une liste correspondant à une colonne de la grille
            for y in range(ny):
                GrilleCol.append(Cellule(x,y))#Création et ajout des cellules dans la colonne
            self.grille.append(GrilleCol)#Ajout de la colonne à la liste correspondant à la grille
        #On applique l'algorithme de l'arbre binaire pour transformer la grille vierge en labyrinthe
        for x in range(nx): 
            for y in range(ny):
                if (x,y)!=(0,0):
                    if x==0:
                        self.grille[x][y].murs["N"]=False
                    elif y==0:
                        self.grille[x][y].murs["O"]=False
                    else:
                        mur=random.choice(["O","N"])
                        self.grille[x][y].murs[mur]=False
                        
        
    def cellule(self, x, y):
        """
        retourne la cellule (objet de classe Cellule) de la grille de position (x=colonne, y=ligne)
        """
        return self.grille[x][y]
    
       
    def __str__(self):
        """
        retourne une chaine représentant le labyrinthe. Permet de visualiser la grille à l'aide de la fonction print.
        Sert uniquement au développement.
        """
        laby_lignes = []
        
        for y in range(self.ny):
            laby_l=[]
            for x in range(self.nx):
                if self.grille[x][y].murs['N']:
                    laby_l.append('+---')
                else:
                    laby_l.append('+   ')
            laby_l.append('+')
            laby_lignes.append(''.join(laby_l))
            laby_l=[]
            for x in range(self.nx):
                if self.grille[x][y].murs['O']:
                    laby_l.append('|   ')
                else:
                    laby_l.append('    ')
            laby_l.append('|')
            laby_lignes.append(''.join(laby_l))
        laby_lignes.append(''.join('+---' * self.nx+'+'))
        return '\n'.join(laby_lignes)
		
class Personnage():
    """Class personnage permettant de lister les attributs
    d'un personnage tel que sa positon ou son inventaire"""
    def __init__(self):
        """Création d'un personnage avec sa position et son inventaire"""
        self.inventaire={"Torche":False}
        self.pos=[0,0]
    
    def gauche(self):
        self.pos[0]-=1

    def droite(self):
        self.pos[0]+=1
        
    def haut(self):
        self.pos[1]-=1

    def bas(self):
        self.pos[1]+=1
Link=Personnage()
print(Link.pos)
Link.gauche()
Link.gauche()
print(Link.pos)

import pygame
from pygame.locals import *
pygame.init()

color = (200,200,200)
size = (800,600)
try:
    Donjon = Grille(10,10)
    print(Donjon)
    Joueur=Personnage()

    fenetre=pygame.display.set_mode(size)#fenêtre de taille 640*480
    Labyrinth=pygame.Surface(size,pygame.SRCALPHA)
    Labyrinth.convert_alpha()
    Gameboard=pygame.Surface(size)
    Gameboard=Gameboard.convert_alpha()

    
    #Chargement des murs
    #coin=pygame.image.load('Sprites/Walls/Corner.png').convert_alpha()
    #haut=pygame.image.load('Sprites/Walls/Upper.png').convert_alpha()
    #gauche=pygame.image.load('Sprites/Walls/Left.png').convert_alpha()
    murs=[pygame.image.load('Sprites/Walls/Corner.png').convert_alpha(),
          pygame.image.load('Sprites/Walls/Upper.png').convert_alpha(),
          pygame.image.load('Sprites/Walls/Left.png').convert_alpha()]
    #murs=[coin,haut,gauche]
    #Chargement des sprites du personnage
    PFront=pygame.image.load('Sprites/Char/PFront.png').convert_alpha()
    PFront=pygame.transform.scale(PFront,(24,24))
    PLeft=pygame.image.load('Sprites/Char/PLeft.png').convert_alpha()
    PLeft=pygame.transform.scale(PLeft,(24,24))
    PBack=pygame.image.load('Sprites/Char/PBack.png').convert_alpha()
    PBack=pygame.transform.scale(PBack,(24,24))
    PRight=pygame.image.load('Sprites/Char/PRight.png').convert_alpha()
    PRight=pygame.transform.scale(PRight,(24,24))
    CharacterRect=pygame.Rect(7,7,24,24)
    
    #Affichage du Donjon
    coord_x = 0
    coord_y = 0
    for i in range(Donjon.ny):
        for j in range(Donjon.nx):
            if Donjon.cellule(j,i).murs["N"]==True & Donjon.cellule(j,i).murs["O"]==True:
                Labyrinth.blit(murs[0],(coord_x,coord_y))
            elif Donjon.cellule(j,i).murs["N"]==False :
                Labyrinth.blit(murs[2],(coord_x,coord_y))
            elif Donjon.cellule(j,i).murs["O"]==False:
                Labyrinth.blit(murs[1],(coord_x,coord_y))
            coord_x+=32
        coord_x=0
        coord_y+=32
    #Affichage des bords droit du donjon
    coord_x=Donjon.nx*32
    for y in range(0,coord_y,32):
        Labyrinth.blit(murs[2],(coord_x,y))
    
    #Affichage des bords inférieur du donjon
    coord_y=Donjon.ny*32
    for x in range(0,coord_x,32):
        Labyrinth.blit(murs[1],(x,coord_y))
    
    Gameboard.blit(PFront,CharacterRect)
    fenetre.blit(Gameboard,(0,0))
    fenetre.blit(Labyrinth,(0,0))
    pygame.display.flip()

    continuer=True
    #boucle perpétuelle qui permet de garder la fenêtre ouverte
    while continuer:
        for event in pygame.event.get():
            #pygame prend le premier évènement de la file
            if event.type==QUIT:
                #l'évènement QUIT correspond au clic sur la croix
                continuer = False #permet de quitter la boucle
            if event.type==KEYDOWN:
                if event.key==K_LEFT:
                    if Joueur.pos[0]!=0:
                        if Donjon.cellule(Joueur.pos[0],Joueur.pos[1]).murs["O"]==False:
                            Gameboard.fill((0,0,0))
                            CharacterRect=CharacterRect.move(-32,0)
                            Gameboard.blit(PLeft,CharacterRect)
                            fenetre.blit(Gameboard,(0,0))
                            fenetre.blit(Labyrinth,(0,0))
                            Joueur.gauche()

                if event.key==K_RIGHT:
                    
                    if Joueur.pos[0]+1<Donjon.nx:
                        if Donjon.cellule(Joueur.pos[0]+1,Joueur.pos[1]).murs["O"]==False:
                            
                            Gameboard.fill((0,0,0))
                            CharacterRect=CharacterRect.move(32,0)
                            Gameboard.blit(PRight,CharacterRect)
                            fenetre.blit(Gameboard,(0,0))
                            fenetre.blit(Labyrinth,(0,0))
                            Joueur.droite()
                            
                if event.key==K_UP:
                    if Joueur.pos[1]!=0:
                        if Donjon.cellule(Joueur.pos[0],Joueur.pos[1]).murs['N']==False:
                        
                            Gameboard.fill((0,0,0))
                            CharacterRect=CharacterRect.move(0,-32)
                            Gameboard.blit(PBack,CharacterRect)
                            fenetre.blit(Gameboard,(0,0))
                            fenetre.blit(Labyrinth,(0,0))
                            Joueur.haut()
            
                if event.key==K_DOWN:
                    if Joueur.pos[1]+1<Donjon.ny:
                        if Donjon.cellule(Joueur.pos[0],Joueur.pos[1]+1).murs['N']==False:

                            Gameboard.fill((0,0,0))
                            CharacterRect=CharacterRect.move(0,32)
                            Gameboard.blit(PFront,CharacterRect)
                            fenetre.blit(Gameboard,(0,0))
                            fenetre.blit(Labyrinth,(0,0))
                            Joueur.bas()
                            
            pygame.display.flip()
                
finally:
    pygame.quit()