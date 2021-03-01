########
import pygame
from pygame.locals import *
import random
class NoeudCellule() :
    def __init__(self, pos, murs):
        self.pos=pos
        self.gauche=None
        self.droit=None
        self.murs=murs
        
    def __repr__(self):
        """permet d'afficher un arbre sous forme d'une liste"""
        if self==None:
            return None
        else :
            return str([self.pos, self.gauche, self.droit, self.murs])
        
    def creerfd(self, pos, murs):
        '''crée et retourne un noeud fils droit ayant pour valeur le paramètre cle'''
        assert self.droit is None,"Le Noeud possède déjà un fils droit"
        self.droit=NoeudCellule(pos, murs)
        return self.droit
        
    def creerfg(self, pos, murs):
        '''crée et retourne un noeud fils gauche ayant pour valeur le paramètre cle'''
        assert self.gauche is None,"Le Noeud possède déjà un fils gauche"
        self.gauche=NoeudCellule(pos, murs)
        return self.gauche

'''algorithme récursif, construit un arbre aléatoirement à partir d'un noeud et dictionnaire de coordonnées
   chaque noeud possède un attribut position, et murs, qui varie selon le chemin emprunté
   par défaut, le fils gauche correspond aux noeuds qui évoluent sur l'axe des abcisses
   le fils droit aux noeud qui évoluent sur l'axe des ordonnées'''
def Recurs(noeud, dic):
    posx, posy=noeud.pos[0], noeud.pos[1]
    #si le noeud n'a pas été parcouru, le supprime du dictionnaire
    if noeud.pos in dic:
        del dic[noeud.pos]
    chx=random.choice([1, 2])
    #si le choix=1, créer une cellule sur l'axe x, puis l'axe y
    if chx==1:
        chx2=random.choice([1, 2])
        #si 2ème choix=1, recule d'une cellule sur l'axe des abcisses
        if chx2==1:
            if (posx-1, posy) in dic.values() and noeud.gauche==None:
                noeud.murs["O"]=False
                Recurs(noeud.creerfg((posx-1, posy), {'N' : True, 'O' : True}), dic)
            #si le fils gauche est occupé, vérifie le fils droit
            if (posx-1, posy) in dic.values() and noeud.droit==None:
                #si le fils droit est libre, y assigne une position
                noeud.murs["O"]=False
                Recurs(noeud.creerfd((posx-1, posy), {'N' : True, 'O' : True}), dic)
        if (posx+1, posy) in dic.values() and noeud.gauche==None:
            Recurs(noeud.creerfg((posx+1, posy), {'N' : True, 'O' : False}), dic)
        #au cas où une incrémentation serait impossible sur le fils gauche, décrémenter
        if (posx-1, posy) in dic.values() and noeud.gauche==None:
            noeud.murs["O"]=False
            Recurs(noeud.creerfg((posx-1, posy), {'N' : True, 'O' : True}), dic)
        #si incrémentation et décrémentation impossible , réessayer sur le fils droit
        if (posx+1, posy) in dic.values() and noeud.droit==None:
            Recurs(noeud.creerfd((posx+1, posy), {'N' : True, 'O' : False}), dic)
        if (posx-1, posy) in dic.values() and noeud.droit==None:
            noeud.murs["O"]=False
            Recurs(noeud.creerfd((posx-1, posy), {'N' : True, 'O' : True}), dic)
        #même procédé mais pour l'axe des ordonnées
        chx2=random.choice([1, 2])
        if chx2==1:
            if (posx, posy-1) in dic.values() and noeud.droit==None:
                noeud.murs["N"]=False
                Recurs(noeud.creerfd((posx, posy-1), {'N' : True, 'O' : True}), dic)
            if (posx, posy-1) in dic.values() and noeud.gauche==None:
                noeud.murs["N"]=False
                Recurs(noeud.creerfg((posx, posy-1), {'N' : True, 'O' : True}), dic)
        if (posx, posy+1) in dic.values() and noeud.droit==None:
            Recurs(noeud.creerfd((posx, posy+1), {'N' : False, 'O' : True}), dic)
        if (posx, posy-1) in dic.values() and noeud.droit==None:
            noeud.murs["N"]=False
            Recurs(noeud.creerfd((posx, posy-1), {'N' : True, 'O' : True}), dic)
        if (posx, posy+1) in dic.values() and noeud.gauche==None:
            Recurs(noeud.creerfg((posx, posy+1), {'N' : False, 'O' : True}), dic)
        if (posx, posy-1) in dic.values() and noeud.gauche==None:
            noeud.murs["N"]=False
            Recurs(noeud.creerfg((posx, posy-1), {'N' : True, 'O' : True}), dic)
    #si le choix=2, créer une cellule sur l'axe y, puis l'axe x, même procédé que si chx==1
    else :
        chx2=random.choice([1, 2])
        if chx2==1:
            if (posx, posy-1) in dic.values() and noeud.droit==None:
                noeud.murs["N"]=False
                Recurs(noeud.creerfd((posx, posy-1), {'N' : True, 'O' : True}), dic)
            if (posx, posy-1) in dic.values() and noeud.gauche==None:
                noeud.murs["N"]=False
                Recurs(noeud.creerfg((posx, posy-1), {'N' : True, 'O' : True}), dic)
        if (posx, posy+1) in dic.values() and noeud.droit==None:
            Recurs(noeud.creerfd((posx, posy+1), {'N' : False, 'O' : True}), dic)
        if (posx, posy-1) in dic.values() and noeud.droit==None:
            noeud.murs["N"]=False
            Recurs(noeud.creerfd((posx, posy-1), {'N' : True, 'O' : True}), dic)
        if (posx, posy+1) in dic.values() and noeud.gauche==None:
            Recurs(noeud.creerfg((posx, posy+1), {'N' : False, 'O' : True}), dic)
        if (posx, posy-1) in dic.values() and noeud.gauche==None:
            noeud.murs["N"]=False
            Recurs(noeud.creerfg((posx, posy-1), {'N' : True, 'O' : True}), dic)
            
        chx2=random.choice([1, 2])
        if chx2==1:
            if (posx-1, posy) in dic.values() and noeud.gauche==None:
                noeud.murs["O"]=False
                Recurs(noeud.creerfg((posx-1, posy), {'N' : True, 'O' : True}), dic)
            if (posx-1, posy) in dic.values() and noeud.droit==None:
                noeud.murs["O"]=False
                Recurs(noeud.creerfd((posx-1, posy), {'N' : True, 'O' : True}), dic)
        if (posx+1, posy) in dic.values() and noeud.gauche==None:
            Recurs(noeud.creerfg((posx+1, posy), {'N' : True, 'O' : False}), dic)
        if (posx-1, posy) in dic.values() and noeud.gauche==None:
            noeud.murs["O"]=False
            Recurs(noeud.creerfg((posx-1, posy), {'N' : True, 'O' : True}), dic)
        if (posx+1, posy) in dic.values() and noeud.droit==None:
            Recurs(noeud.creerfd((posx+1, posy), {'N' : True, 'O' : False}), dic)
        if (posx-1, posy) in dic.values() and noeud.droit==None:
            noeud.murs["O"]=False
            Recurs(noeud.creerfd((posx-1, posy), {'N' : True, 'O' : True}), dic)        

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
        CoorDico={}
        for x in range(nx): 
            for y in range(ny):
                CoorDico[(x, y)]=(x, y)
        item=NoeudCellule(CoorDico[(0, 0)], {'N' : True, 'O' : True})
        Recurs(item, CoorDico)
        self.grille = item
                        
    def GetMurs(self, x, y, arbre):
        
        coordo=(x, y)
        
        def parcours(coord, arbre):
            if arbre.pos==coord:
                global resu
                resu=arbre.murs
            if arbre.gauche!=None:
                parcours(coord, arbre.gauche)
            if arbre.droit!=None:
                parcours(coord, arbre.droit)
        parcours(coordo, arbre)
        return resu
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
        self.inventaire={"Torche":False, "Tresor":False}
        self.pos=[0,0]
    
    def gauche(self):
        self.pos[0]-=1

    def droite(self):
        self.pos[0]+=1
        
    def haut(self):
        self.pos[1]-=1

    def bas(self):
        self.pos[1]+=1

class Objet():
    def __init__(self, nom, pos):
        self.nom=nom
        self.pos=pos
def VerifObj(dico, pos, obj):
    res=False
    for item in dico:
        if dico.get(obj)==pos:
            res=True
    return res
	
pygame.init()

color = (200,200,200)
size = (1280,720)
try:
    x, y=39,22 
    Donjon = Grille(x,y)
    Joueur=Personnage()
    Tresor=Objet("Trésor", [x, y])

    fenetre=pygame.display.set_mode(size)#fenêtre de taille 640*480
    Labyrinth=pygame.Surface(size,pygame.SRCALPHA)
    Labyrinth.convert_alpha()
    Gameboard=pygame.Surface(size)
    Gameboard=Gameboard.convert_alpha()

    
    #Chargement des murs
    coin=pygame.image.load('Sprites/Walls/Corner.png').convert_alpha()
    haut=pygame.image.load('Sprites/Walls/Upper.png').convert_alpha()
    gauche=pygame.image.load('Sprites/Walls/Left.png').convert_alpha()
    vide=pygame.image.load('Sprites/Walls/None.png').convert_alpha()
    sol=pygame.image.load('Sprites/Walls/Floor.png').convert_alpha()
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
    TresorImg=pygame.image.load('Sprites/Items/diamant.png').convert_alpha()
    #Affichage du Donjon
    coord_x = 0
    coord_y = 0
    for i in range(Donjon.ny):
        for j in range(Donjon.nx):
            Labyrinth.blit(sol,(coord_x,coord_y))
            if Donjon.GetMurs(j,i, Donjon.grille)["N"]==True and Donjon.GetMurs(j,i, Donjon.grille)["O"]==True:
                Labyrinth.blit(coin,(coord_x,coord_y))
            elif Donjon.GetMurs(j,i, Donjon.grille)["N"]==False and Donjon.GetMurs(j,i, Donjon.grille)["O"]==True :
                Labyrinth.blit(gauche,(coord_x,coord_y))
            elif Donjon.GetMurs(j,i, Donjon.grille)["O"]==False and Donjon.GetMurs(j,i, Donjon.grille)["N"]==True:
                Labyrinth.blit(haut,(coord_x,coord_y))
            elif Donjon.GetMurs(j,i, Donjon.grille)["O"]==False and Donjon.GetMurs(j,i, Donjon.grille)["N"]==False:
                Labyrinth.blit(vide,(coord_x,coord_y))
            coord_x+=32
            fenetre.blit(Labyrinth,(0,0))
            pygame.display.flip()
            pygame.time.delay(5)
        coord_x=0
        coord_y+=32
    #Affichage des bords droit du donjon
    coord_x=Donjon.nx*32
    for y in range(0,coord_y,32):
        Labyrinth.blit(gauche,(coord_x,y))
    
    #Affichage des bords inférieur du donjon
    coord_y=Donjon.ny*32
    for x in range(0,coord_x,32):
        Labyrinth.blit(haut,(x,coord_y))
    
    #Définition de la position du trésor
    x=random.randint(Tresor.pos[0]-(Tresor.pos[0]//4), Tresor.pos[0])
    y=random.randint(Tresor.pos[1]-(Tresor.pos[1]//4), Tresor.pos[1])
    Tresor.pos[0]=x-1
    Tresor.pos[1]=y-1
        
    Objets={'Tresor' : Tresor.pos}
        
    Gameboard.fill((0,0,0,0))
    Gameboard.blit(PFront,CharacterRect)
    Gameboard.blit(TresorImg,((x-1)*32,(y-1)*32))
    fenetre.blit(Labyrinth,(0,0))
    fenetre.blit(Gameboard,(0,0))
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
                        if Donjon.GetMurs(Joueur.pos[0],Joueur.pos[1], Donjon.grille)["O"]==False:
                            
                            Gameboard.fill((0,0,0,0))
                            CharacterRect=CharacterRect.move(-32,0)
                            Gameboard.blit(PLeft,CharacterRect)
                            Joueur.gauche()

                if event.key==K_RIGHT:
                    
                    if Joueur.pos[0]+1<Donjon.nx :
                        if Donjon.GetMurs(Joueur.pos[0]+1,Joueur.pos[1], Donjon.grille)["O"]==False:
                            
                            Gameboard.fill((0,0,0,0))
                            CharacterRect=CharacterRect.move(32,0)
                            Gameboard.blit(PRight,CharacterRect)
                            Joueur.droite()
                            
                if event.key==K_UP:
                    if Joueur.pos[1]!=0:
                        if Donjon.GetMurs(Joueur.pos[0],Joueur.pos[1], Donjon.grille)['N']==False:
                            
                            Gameboard.fill((0,0,0,0))
                            CharacterRect=CharacterRect.move(0,-32)
                            Gameboard.blit(PBack,CharacterRect)
                            Joueur.haut()
            
                if event.key==K_DOWN:
                    if Joueur.pos[1]+1<Donjon.ny:
                        if Donjon.GetMurs(Joueur.pos[0],Joueur.pos[1]+1, Donjon.grille)['N']==False:
                            
                            Gameboard.fill((0,0,0,0))
                            CharacterRect=CharacterRect.move(0,32)
                            Gameboard.blit(PFront,CharacterRect)
                            Joueur.bas()
                            
                if VerifObj(Objets, Joueur.pos, "Tresor")==False and Joueur.inventaire["Tresor"]==False:
                    Gameboard.blit(TresorImg,((x-1)*32,(y-1)*32))
                else:
                    Joueur.inventaire["Tresor"]=True
                    continuer=False
                
                fenetre.blit(Labyrinth,(0,0))
                fenetre.blit(Gameboard,(0,0))
            pygame.display.flip()
                
finally:
    pygame.quit()