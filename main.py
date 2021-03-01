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
        del dic[dic.index(noeud.pos)]
    chx=random.choice([1, 2])
    #si le choix=1, créer une cellule sur l'axe x, puis l'axe y
    if chx==1:
        RecursXY(noeud, dic, 1, 0)
        #même procédé mais pour l'axe des ordonnées
        RecursXY(noeud, dic, 0, 1)
    #si le choix=2, créer une cellule sur l'axe y, puis l'axe x, même procédé que si chx==1
    else :
        RecursXY(noeud, dic, 0, 1)
        RecursXY(noeud, dic, 1, 0)

def RecursXY(noeud, dic, x, y):
    posx, posy=noeud.pos[0], noeud.pos[1]
    chx2=random.choice([1, 2])
    #si 2ème choix=1, recule d'une cellule sur l'axe des abcisses
    if noeud.gauche==None:
        if (posx-x, posy-y) in dic and chx2==1:
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfg((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)
            #si le fils gauche est occupé, vérifie le fils droit
        elif (posx+x, posy+y) in dic:
            Recurs(noeud.creerfg((posx+x, posy+y), {'N' : x, 'O' : y}), dic)
        #au cas où une incrémentation serait impossible sur le fils gauche, décrémenter
        elif (posx-x, posy-y) in dic:
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfg((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)
    if noeud.droit==None:
        if (posx-x, posy-y) in dic and chx2==1:
            #si le fils droit est libre, y assigne une position
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfd((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)
        elif (posx+x, posy+y) in dic:
            Recurs(noeud.creerfd((posx+x, posy+y), {'N' : x, 'O' : y}), dic)
        elif (posx-x, posy-y) in dic:
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfd((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)



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
        CoorList=[]
        for x in range(nx): 
            for y in range(ny):
                CoorList.append((x, y))
        item=NoeudCellule(CoorList[0], {'N' : True, 'O' : True})
        Recurs(item, CoorList)
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
		
class Personnage(pygame.sprite.Sprite):
    """Class personnage permettant de lister les attributs
    d'un personnage tel que sa positon ou son inventaire"""
    def __init__(self):
        super().__init__()
        """Création d'un personnage avec sa position et son inventaire"""
        self.inventaire={"Torche":False}
        self.pos=[0,0]
        self.sprite_sheet = pygame.image.load('Sprites/Char/SpriteSheetLink.png').convert_alpha()
        self.spriteslist=[]
        self.mouv=[2, 3, 6, 3, 2, 2, 3, 6, 3, 2]
        
        templist=[]
        for i in range(4):
            image = pygame.Surface([96, 104]).convert_alpha()
            image.blit(self.sprite_sheet, (0, 0), (96*i, 0, 96, 104))
            image= pygame.transform.scale(image,(28,28))
            image.set_colorkey((0,0,0))
            templist.append(image)
        self.spriteslist.append(templist)
        for y in range(4):
            templist=[]
            for x in range(10):
                image = pygame.Surface([96, 104]).convert()
                image.blit(self.sprite_sheet, (0, 0), (96*x, (104*y)+104, 96, 104))
                image= pygame.transform.scale(image,(28,28))
                image.set_colorkey((0,0,0))
                templist.append(image)
            self.spriteslist.append(templist)
            
        self.image=self.spriteslist[0][0]
        self.rect = pygame.Rect(4,4,28,28)
        self.JRect=self.rect
    
    #Méthodes pour modifier les coordonnées du personnage
    def gauche(self, group, screen, charect, camera):
        
        self.pos[0]-=1
        
        for i in range(len(self.mouv)):
            self.image=self.spriteslist[2][i]
            self.JRect=self.JRect.move(-self.mouv[i], 0)
            charect=charect.move(-self.mouv[i], 0)
            screen.fill((0,0,0,0))
            self.rect=self.JRect
            group.draw(screen)
            pygame.display.update(self)
            pygame.time.delay(7*i)
            camera=Update(charect, camera)
        screen.fill((0,0,0,0))
        self.image=self.spriteslist[0][1]
        group.draw(screen)
        pygame.display.update(self)
        return camera, charect
        
    def droite(self, group, screen, charect, camera):
        
        self.pos[0]+=1
        
        for i in range(len(self.mouv)):
            self.image=self.spriteslist[4][i]
            self.JRect=self.JRect.move(self.mouv[i], 0)
            charect=charect.move(self.mouv[i], 0)
            screen.fill((0,0,0,0))
            self.rect=self.JRect
            group.draw(screen)
            pygame.display.update(self)
            pygame.time.delay(7*i)
            camera=Update(charect, camera)
        screen.fill((0,0,0,0))
        self.image=self.spriteslist[0][3]
        group.draw(screen)
        pygame.display.update(self)
        return camera, charect
        
    def haut(self, group, screen, charect, camera):
        
        self.pos[1]-=1
        
        for i in range(len(self.mouv)):
            self.image=self.spriteslist[3][i]
            self.JRect=self.JRect.move(0, -self.mouv[i])
            charect=charect.move(0, -self.mouv[i])
            screen.fill((0,0,0,0))
            self.rect=self.JRect
            group.draw(screen)
            pygame.display.update(self)
            pygame.time.delay(7*i)
            camera=Update(charect, camera)
        screen.fill((0,0,0,0))
        self.image=self.spriteslist[0][2]
        group.draw(screen)
        pygame.display.update(self)
        return camera, charect
        
    def bas(self, group, screen, charect, camera):
        
        self.pos[1]+=1
        
        for i in range(len(self.mouv)):
            self.image=self.spriteslist[1][i]
            self.JRect=self.JRect.move(0, self.mouv[i])
            charect=charect.move(0, self.mouv[i])
            screen.fill((0,0,0,0))
            self.rect=self.JRect
            group.draw(screen)
            pygame.display.update(self)
            pygame.time.delay(7*i)
            camera=Update(charect, camera)
        screen.fill((0,0,0,0))
        self.image=self.spriteslist[0][0]
        group.draw(screen)
        pygame.display.update(self)
        return camera, charect
        
		
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
    global CharacterRect
    def __init__(self,Camera, CharacterRect):
        #Définitions des variables du jeu        
        self.allstate=["intro","endless","UC"] #Liste de toutes les scènes du jeu
        self.etat = self.allstate[0] #Scène actuel du jeu (index à changer selon la scène souhaité au lancement)
        self.boucle= True
        self.Joueur=Personnage()
        self.my_group = pygame.sprite.Group(self.Joueur)
        #self.CharacterRect.center=(0,0)
        self.CharacterRect=CharacterRect
        self.Donjons=[]
        self.x,self.y=10,10
        self.Tresor=None
        self.Tresor=init_player_tresor(self.Tresor,self.CharacterRect,self.x,self.y)
        self.Objets={'Tresor' : self.Tresor.pos}#Dictionnaire des tous les objets présents
        self.Camera=Camera
        self.Camera = pygame.transform.scale(self.Camera,(160,160))
        
        self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect, self.Joueur=reset(self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect, self.Joueur)

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
        #fenetre.blit(SCamera,(0,0))
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
                    self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect, self.Joueur=reset(self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect, self.Joueur)
                    Labyrinth.fill((0,0,0,1))
                    Gameboard.fill((0,0,0,1))
                    Game.fill((0,0,0,1))
                    fenetre.fill((0,0,0))
                    drawdonjon(self.Donjons[-1])
                    Gameboard.blit(PFront,self.CharacterRect)
                    Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                    Game.blit(Labyrinth,(64,64))
                    Game.blit(Gameboard,(64,64))
                    pygame.display.flip()
                    fenetre.blit(Interface,(0,0))
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
                
                murN=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)['N']
                murS=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1]+1, self.Donjons[0].grille)['N']
                murO=self.Donjons[0].GetMurs(self.Joueur.pos[0]+1,self.Joueur.pos[1], self.Donjons[0].grille)["O"]
                murE=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)["O"]
                
                if event.key==K_ESCAPE:
                    Labyrinth.fill((0,0,0))
                    Gameboard.fill((0,0,0))
                    pygame.display.flip()
                    self.etat=self.allstate[0]
                
                if event.key==K_LEFT:
                    if self.Joueur.pos[0]!=0 and murE==False:
                            Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Camera, self.CharacterRect=self.Joueur.gauche(self.my_group, Gameboard, self.CharacterRect, self.Camera)
                        

                if event.key==K_RIGHT:
                    
                    if self.Joueur.pos[0]+1<self.Donjons[0].nx and murO==False:
                            
                            Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Camera, self.CharacterRect=self.Joueur.droite(self.my_group, Gameboard, self.CharacterRect, self.Camera)

                            
                if event.key==K_UP:
                    if self.Joueur.pos[1]!=0 and murN==False:
                            
                            Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Camera, self.CharacterRect=self.Joueur.haut(self.my_group, Gameboard, self.CharacterRect, self.Camera)

            
                if event.key==K_DOWN:
                    if self.Joueur.pos[1]+1<self.Donjons[0].ny and murS==False:
                            Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Camera, self.CharacterRect=self.Joueur.bas(self.my_group, Gameboard, self.CharacterRect, self.Camera)

                if VerifObj(self.Objets, self.Joueur.pos, "Tresor")==True and self.Joueur.inventaire["Tresor"]==False:
                    self.Joueur.inventaire["Tresor"]=True
                    #pygame.quit()
                    self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect, self.Joueur=reset(self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect, self.Joueur)
                    drawdonjon(self.Donjons[-1])
                    Gameboard.fill((0,0,0,1))
                    Gameboard.blit(PFront,self.CharacterRect)
                    Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
        #pygame.transform.scale(Labyrinth,(600,600),fenetre)
        #pygame.transform.scale()
        self.Camera=Update(self.CharacterRect, self.Camera)
        
    def gestionnaire_de_scene(self):
        """Méthode qui permet de basculer d'une scène à l'autre"""
        if self.etat == self.allstate[0]:
            self.intro()
        if self.etat == self.allstate[1]:
            self.endless()
        if self.etat == self.allstate[2]:
            self.uc()
			
pygame.init()


#Variables paramètres
framerate=pygame.time.Clock().tick(60)
pygame.key.set_repeat(500,400)


size = (1500,1500)

#Création de la fenêtre de l'application
fenetre=pygame.display.set_mode((600,600))#fenêtre de taille 640*480
CharacterRect=pygame.Rect(-64,-64,160,160)

#Chargement des murs
SpriteMaze=(pygame.image.load('Sprites/Walls/Corner.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Upper.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Left.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/None.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Floor.png').convert_alpha())

PFront=pygame.image.load('Sprites/Char/PFront.png').convert_alpha()

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
imguc=pygame.image.load('Sprites/Menu/UI/UC.png').convert_alpha()#image Under Construction
imguc=pygame.transform.scale(imguc,(128,104))

Interface=pygame.image.load('Sprites/Menu/UI/Interface.png').convert_alpha()

#Initialisation des boutons
btnCampagne=bouton(imgBtnCampagne[0],175,265)
btnCasual=bouton(imgBtnCasual[0],175,355)
btnEndless=bouton(imgBtnEndless[0],175,455)


#Définition des surfaces :
#Invisibles
UC=pygame.Surface(size,pygame.SRCALPHA)
UC.blit(imguc,(300-64,300-32))
Labyrinth=pygame.Surface(size,pygame.SRCALPHA) #Background (jamais affichée)
Labyrinth=Labyrinth.convert_alpha()
Labyrinth.fill((0,0,0,0))
Gameboard=pygame.Surface(size,pygame.SRCALPHA) #Surface de tous les éléments interractibles. (jamais affichée)
Gameboard=Gameboard.convert_alpha()
#Affichée
Game=pygame.Surface(size,pygame.SRCALPHA) #Concaténation de Labyrinth et Gameboard
Game=Game.convert_alpha()
Camera=pygame.Surface((160,160),pygame.SRCALPHA) #Surface qui sera affiché dans L'UI
Camera=Camera.convert_alpha()


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
    Gameboard.blit(PFront,(CharacterRect.centerx,CharacterRect.centery))
    Labyrinth.blit(TresorImg,((Tresor.pos[0])*32,(Tresor.pos[1])*32))
    return Tresor

def Update(Charac, cam):
    """Fonction permettant de mettre à 'recharger' l'affichage de l'écran."""
    fenetre.fill((0,0,0))
    Game.blit(Labyrinth,(64,64))
    Game.blit(Gameboard,(64,64))
    sub = Game.subsurface(Charac)
    cam=pygame.Surface((160,160),pygame.SRCALPHA)
    cam=Camera.convert_alpha()
    cam.blit(sub,(0,0))
    cam = pygame.transform.scale(cam,(396,396))
    fenetre.blit(cam,(12,12))
    fenetre.blit(Interface,(0,0))
    pygame.display.flip()
    return cam

#Affichage du Donjon
def drawdonjon(Donjon):
    def drawint(Donjon): 
        """Fonction permettant de d'afficher une grille sur la surface Background.
        Prend en paramètres un donjon."""
        coord_x=Donjon.pos[0]*32
        coord_y=Donjon.pos[1]*32
        Labyrinth.blit(SpriteMaze[4],(coord_x,coord_y))#sol
        if Donjon.murs["N"]==True and Donjon.murs["O"]==True:
            Labyrinth.blit(SpriteMaze[0],(coord_x,coord_y))#coin
        elif Donjon.murs["N"]==False and Donjon.murs["O"]==True :
            Labyrinth.blit(SpriteMaze[2],(coord_x,coord_y))#gauche
        elif Donjon.murs["O"]==False and Donjon.murs["N"]==True:
            Labyrinth.blit(SpriteMaze[1],(coord_x,coord_y))#haut
        elif Donjon.murs["O"]==False and Donjon.murs["N"]==False:
            Labyrinth.blit(SpriteMaze[3],(coord_x,coord_y))#empty
        Game.blit(Labyrinth,(64,64))
        if Donjon.gauche!=None:
            drawint(Donjon.gauche)
        if Donjon.droit!=None:
            drawint(Donjon.droit)
    drawint(Donjon.grille)
    

    #Affichage des bords droit du donjon
    coord_x=Donjon.nx*32
    coord_y=Donjon.ny*32
    for y in range(0,coord_y,32):
        Labyrinth.blit(SpriteMaze[2],(coord_x,y))
        Game.blit(Labyrinth,(64,64))
    #Affichage des bords inférieur du donjon
    for x in range(0,coord_x,32):
        Labyrinth.blit(SpriteMaze[1],(x,coord_y))
        Game.blit(Labyrinth,(64,64))

def reset(Joueur,Donjons,Tresor,x,y,CharacterRect, JoueuRect):
    """Fonction permettant de Remettre la position du joueur et de son sprite en (0,0),
    réinitialiser son inventaire, et de replacer aléatoirement le trésor.
    Retourne Tous les objets/variables réinintialisées."""
    
    Joueur.inventaire["Tresor"]=False
    Joueur.pos[0]=0
    Joueur.pos[1]=0
    Gameboard.fill((0,0,0,1))
    Labyrinth.fill((0,0,0,1))
    CharacterRect.x=0
    CharacterRect.y=0
    JoueuRect.rect=pygame.Rect(4,4,28,28)
    JoueuRect.JRect=JoueuRect.rect
    Tresor=init_player_tresor(Tresor,CharacterRect,x,y)
    Donjons=[]
    Donjons.append(Grille(x,y))
    
    return Joueur,Donjons,Tresor.pos[0],Tresor.pos[1],CharacterRect, JoueuRect

#Lancement du jeu
game_state = gamestate(Camera, CharacterRect)
pygame.display.flip()
while game_state.boucle:
    game_state.gestionnaire_de_scene()
pygame.quit()