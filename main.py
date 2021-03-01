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
    #Méthodes pour modifier les coordonnées du personnage
    def gauche(self):
        self.pos[0]-=1

    def droite(self):
        self.pos[0]+=1
        
    def haut(self):
        self.pos[1]-=1

    def bas(self):
        self.pos[1]+=1
		
class bouton():
    def __init__(self,sprite, x, y):
        self.sprite=sprite
        self.x=x
        self.y=y
        
    def draw(self,surface):
        surface.blit(self.sprite,(self.x,self.y))
        
    def isOver(self,pos):
        if pos[0]> self.x and pos[0] < self.x+self.sprite.get_width():
            if pos[1]>self.y and pos[1]< self.y + self.sprite.get_height():
                return True
        return False
		
class Objet():
    """Class définisant les objets du jeu"""
    def __init__(self, nom, pos):
        self.nom=nom
        self.pos=pos
def VerifObj(dico, pos, obj):
    """Fonction permettant de vérifier si le joueur deux coordonnées sont les mêmes,
    elle sera utilisée pour savoir si le joueur est sur la même cellule que l'objet"""
    res=False
    for item in dico:
        if dico.get(obj)==pos:
            res=True
    return res
	
class gamestate():
    """Objet du jeu, permettant de passer de scène en scène, c'est-à-dire, par exemple, de passer du menu au jeu."""
        
    def __init__(self):
        #Définitions des variables du jeu        
        self.allstate=["intro","endless","UC"] #Liste de toutes les scènes du jeu
        self.etat = self.allstate[0] #Scène actuel du jeu (index à changer selon la scène souhaité au lancement)
        self.boucle= True
        self.Joueur=Personnage()
        self.CharacterRect=pygame.Rect(7,7,24,24)
        self.Donjons=[]
        self.x,self.y=5,1
        self.Tresor=None
        self.Tresor=init_player_tresor(self.Tresor,self.CharacterRect,self.x,self.y)
        self.Objets={'Tresor' : self.Tresor.pos}#Dictionnaire des tous les objets présents
        
        self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect=reset(self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect)

    def uc(self):
        UC.fill((0,0,0))
        UC.blit(imguc,(300-64,300-52))
        fenetre.blit(UC,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            #pygame prend le premier évènement de la file
            if event.type==QUIT:
                #l'évènement QUIT correspond au clic sur la croix
                self.boucle = False #permet de quitter la boucle
            if event.type==MOUSEBUTTONDOWN:

                Labyrinth.fill((0,0,0))
                Gameboard.fill((0,0,0))
                pygame.display.flip()
                self.etat=self.allstate[0]
    
    def intro(self):
        #fenetre.fill((0,0,0))
        Labyrinth.fill((0,0,0,1))
        Gameboard.fill((0,0,0,1))
        Labyrinth.blit(IntroBG,(0,0))
        btnEndless.draw(Gameboard)
        btnCampagne.draw(Gameboard)
        btnCasual.draw(Gameboard)
        fenetre.blit(Labyrinth,(0,0))
        fenetre.blit(Gameboard,(0,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            
            #pygame prend le premier évènement de la file
            if event.type==QUIT:
                #l'évènement QUIT correspond au clic sur la croix
                self.boucle = False #permet de quitter la boucle
            if event.type==MOUSEBUTTONDOWN:
                if btnEndless.isOver(pos):
                    #ligne à mettre en commentaire si on souhaite garder le même laby en endless lorsqu'on retourne au menu:
                    self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect=reset(self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect)

                    Labyrinth.fill((0,0,0,1))
                    Gameboard.fill((0,0,0,1))
                    drawdonjon(self.Donjons[-1])
                    Gameboard.blit(PFront,self.CharacterRect)
                    Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                    fenetre.blit(Labyrinth,(0,0))
                    fenetre.blit(Gameboard,(0,0))
                    pygame.display.flip()
                    self.etat=self.allstate[1]
                
                if btnCampagne.isOver(pos):
                    self.etat=self.allstate[2]
                if btnCasual.isOver(pos):
                    self.etat=self.allstate[2]
                
            if event.type == pygame.MOUSEMOTION:
                if btnEndless.isOver(pos):
                    btnEndless.sprite=imgBtnEndless[1]
                elif btnCampagne.isOver(pos):
                    btnCampagne.sprite=imgBtnCampagne[1]
                elif btnCasual.isOver(pos):
                    btnCasual.sprite=imgBtnCasual[1]
                else:
                    btnEndless.sprite=imgBtnEndless[0]
                    btnCampagne.sprite=imgBtnCampagne[0]
                    btnCasual.sprite=imgBtnCasual[0]
                    
        
        
    def endless(self):
        """Definition qui correspond à la scène de jeu du mode endless(qui se répète)"""
        
       
        for event in pygame.event.get():
            #pygame prend le premier évènement de la file
            if event.type==QUIT:
                #l'évènement QUIT correspond au clic sur la croix
                self.boucle = False #permet de quitter la boucle
            if event.type==KEYDOWN:
                
                if event.key==K_ESCAPE:
                    Labyrinth.fill((0,0,0,1))
                    Gameboard.fill((0,0,0,1))
                    pygame.display.flip()
                    self.etat=self.allstate[0]
                
                if event.key==K_LEFT:
                    if self.Joueur.pos[0]!=0 and self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)["O"]==False:
                            Gameboard.fill((0,0,0,0))
                            Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.CharacterRect=self.CharacterRect.move(-32,0)
                            Gameboard.blit(PLeft,self.CharacterRect)
                            self.Joueur.gauche()


                if event.key==K_RIGHT:
                    
                    if self.Joueur.pos[0]+1<self.Donjons[0].nx and self.Donjons[0].GetMurs(self.Joueur.pos[0]+1,self.Joueur.pos[1], self.Donjons[0].grille)["O"]==False:
                            
                            Gameboard.fill((0,0,0,0))
                            Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.CharacterRect=self.CharacterRect.move(32,0)
                            Gameboard.blit(PRight,self.CharacterRect)
                            
                            self.Joueur.droite()

                            
                if event.key==K_UP:
                    if self.Joueur.pos[1]!=0 and self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)['N']==False:
                            
                            Gameboard.fill((0,0,0,0))
                            Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.CharacterRect=self.CharacterRect.move(0,-32)
                            Gameboard.blit(PBack,self.CharacterRect)
                            self.Joueur.haut()

            
                if event.key==K_DOWN:
                    if self.Joueur.pos[1]+1<self.Donjons[0].ny and self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1]+1, self.Donjons[0].grille)['N']==False:
                            Gameboard.fill((0,0,0,0))
                            Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.CharacterRect=self.CharacterRect.move(0,32)
                            Gameboard.blit(PFront,self.CharacterRect)
                            self.Joueur.bas()

                if VerifObj(self.Objets, self.Joueur.pos, "Tresor")==False and self.Joueur.inventaire["Tresor"]==False:
                    Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                else:
                    self.Joueur.inventaire["Tresor"]=True
                    #pygame.quit()
                    self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect=reset(self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect)
                    Gameboard.fill((0,0,0,1))
                    Gameboard.blit(PFront,self.CharacterRect)
                    Gameboard.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
        #pygame.transform.scale(Labyrinth,(600,600),fenetre)
        #pygame.transform.scale()
        fenetre.blit(Labyrinth,(0,0))
        fenetre.blit(Gameboard,(0,0))
        pygame.display.flip()
    def gestionnaire_de_scene(self):
        """Méthode qui permet de basculer d'une scène à l'autre"""
        if self.etat == self.allstate[0]:
            self.intro()
        if self.etat == self.allstate[1]:
            self.endless()
        if self.etat == self.allstate[2]:
            self.uc()
			
import pygame
from pygame.locals import *
pygame.init()


#Variables paramètres
framerate=pygame.time.Clock().tick(60)
pygame.key.set_repeat(150,30)

color = (200,200,200)
size = (600,600)
#x, y=5,5
#Création de la fenêtre de l'application
fenetre=pygame.display.set_mode(size)#fenêtre de taille 640*480

#Chargement des murs
SpriteMaze=(pygame.image.load('Sprites/Walls/Corner.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Upper.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Left.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/None.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Floor.png').convert_alpha())

#Chargement des sprites personnages
PFront=pygame.image.load('Sprites/Char/PFront.png').convert_alpha()
PFront=pygame.transform.scale(PFront,(24,24))
PLeft=pygame.image.load('Sprites/Char/PLeft.png').convert_alpha()
PLeft=pygame.transform.scale(PLeft,(24,24))
PBack=pygame.image.load('Sprites/Char/PBack.png').convert_alpha()
PBack=pygame.transform.scale(PBack,(24,24))
PRight=pygame.image.load('Sprites/Char/PRight.png').convert_alpha()
PRight=pygame.transform.scale(PRight,(24,24))
#Chargement Des sprites Items
TresorImg=pygame.image.load('Sprites/Items/diamant.png').convert_alpha()
#Chargement des interfaces utilisateurs
IntroBG=pygame.image.load('Sprites/Menu/UI/Menu.png').convert_alpha()
imgBtnCampagne=(pygame.image.load('Sprites/Menu/Boutons/Normal/Campagne.png').convert_alpha(),
             pygame.image.load('Sprites/Menu/Boutons/Clicked/Campagne.png').convert_alpha(),)
imgBtnCasual=(pygame.image.load('Sprites/Menu/Boutons/Normal/Casual.png').convert_alpha(),
           pygame.image.load('Sprites/Menu/Boutons/Clicked/Casual.png').convert_alpha())
imgBtnEndless=(pygame.image.load('Sprites/Menu/Boutons/Normal/Endless.png').convert_alpha(),
            pygame.image.load('Sprites/Menu/Boutons/Clicked/Endless.png').convert_alpha())
imguc=pygame.image.load('Sprites/Menu/UI/UC.png').convert_alpha()
imguc=pygame.transform.scale(imguc,(128,104))

btnCampagne=bouton(imgBtnCampagne[0],175,265)
btnCasual=bouton(imgBtnCasual[0],175,355)
btnEndless=bouton(imgBtnEndless[0],175,455)

#Définition des surfaces
UC=pygame.Surface(size,pygame.SRCALPHA)
UC.blit(imguc,(300-64,300-32))

Labyrinth=pygame.Surface(size,pygame.SRCALPHA) #Background
Labyrinth=Labyrinth.convert_alpha()
Labyrinth.fill((0,0,0,0))
Gameboard=pygame.Surface(size,pygame.SRCALPHA) #Surface de tous les éléments interractibles.
Gameboard=Gameboard.convert_alpha()

#Définition de la position du trésor
def init_player_tresor(Tresor,CharacterRect,x,y):
    """Fonction qui permet de définir la position aléatoire du Trésor. Il est placé aléatoirement dans
    le quart inférieur droit de l'écran.
    Retourne un objet trésor de position aléatoire."""
    Tresor=Objet("Trésor", [x, y])
    tx=random.randint(Tresor.pos[0]-(Tresor.pos[0]//4), Tresor.pos[0])
    ty=random.randint(Tresor.pos[1]-(Tresor.pos[1]//4), Tresor.pos[1])
    Tresor.pos[0]=tx-1
    Tresor.pos[1]=ty-1
    Gameboard.fill((0,0,0,1))
    Gameboard.blit(PFront,CharacterRect)
    Gameboard.blit(TresorImg,((Tresor.pos[0])*32,(Tresor.pos[1])*32))
    return Tresor

#Affichage du Donjon
def drawdonjon(Donjon):
    """Fonction permettant de d'afficher une grille sur la surface Background.
    Prend en paramètres un donjon."""
    
    coord_x = 0
    coord_y = 0
    for i in range(Donjon.ny):
        for j in range(Donjon.nx):
            Labyrinth.blit(SpriteMaze[4],(coord_x,coord_y))#sol
            if Donjon.GetMurs(j,i, Donjon.grille)["N"]==True and Donjon.GetMurs(j,i, Donjon.grille)["O"]==True:
                Labyrinth.blit(SpriteMaze[0],(coord_x,coord_y))#coin
            elif Donjon.GetMurs(j,i, Donjon.grille)["N"]==False and Donjon.GetMurs(j,i, Donjon.grille)["O"]==True :
                Labyrinth.blit(SpriteMaze[2],(coord_x,coord_y))#gauche
            elif Donjon.GetMurs(j,i, Donjon.grille)["O"]==False and Donjon.GetMurs(j,i, Donjon.grille)["N"]==True:
                Labyrinth.blit(SpriteMaze[1],(coord_x,coord_y))#haut
            elif Donjon.GetMurs(j,i, Donjon.grille)["O"]==False and Donjon.GetMurs(j,i, Donjon.grille)["N"]==False:
                Labyrinth.blit(SpriteMaze[3],(coord_x,coord_y))#empty
            coord_x+=32
			
        coord_x=0
        coord_y+=32
    #Affichage des bords droit du donjon
    coord_x=Donjon.nx*32
    for y in range(0,coord_y,32):
        Labyrinth.blit(SpriteMaze[2],(coord_x,y))

    #Affichage des bords inférieur du donjon
    coord_y=Donjon.ny*32
    for x in range(0,coord_x,32):
        Labyrinth.blit(SpriteMaze[1],(x,coord_y))



def reset(Joueur,Donjons,Tresor,x,y,CharacterRect):
    """Fonction permettant de Remettre la position du joueur et de son sprite en (0,0),
    réinitialiser son inventaire, et de replacer aléatoirement le trésor.
    Retourne Tous les objets/variables réinintialisées."""
    Joueur.inventaire["Tresor"]=False
    Joueur.pos[0]=0
    Joueur.pos[1]=0
    Gameboard.fill((0,0,0,1))
    Labyrinth.fill((0,0,0,1))
    CharacterRect.x=7
    CharacterRect.y=7
    Tresor=init_player_tresor(Tresor,CharacterRect,x,y)
    Donjons=[]
    Donjons.append(Grille(x,y))
    drawdonjon(Donjons[-1])
    return Joueur,Donjons,Tresor.pos[0],Tresor.pos[1],CharacterRect

#Lancement du jeu
game_state = gamestate()
pygame.display.flip()
while game_state.boucle:
    game_state.gestionnaire_de_scene()
pygame.quit()