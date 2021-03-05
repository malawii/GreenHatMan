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
        """crée et retourne un noeud fils droit ayant pour valeur le paramètre cle"""
        assert self.droit is None,"Le Noeud possède déjà un fils droit"
        self.droit=NoeudCellule(pos, murs)
        return self.droit
        
    def creerfg(self, pos, murs):
        """crée et retourne un noeud fils gauche ayant pour valeur le paramètre cle"""
        assert self.gauche is None,"Le Noeud possède déjà un fils gauche"
        self.gauche=NoeudCellule(pos, murs)
        return self.gauche
		
########      
class Grille :
    
    """Classe permettant de générer un labyrinthe avec la méthode 'arbre binaire'"""
    
    def __init__(self, nx, ny):
        
        """construction d'une grille labyrinthique de dimension (nx - largeur, ny - hauteur)"""
        
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
		
"""algorithme récursif, construit un arbre aléatoirement à partir d'un noeud et dictionnaire de coordonnées
   chaque noeud possède un attribut position, et murs, qui varie selon le chemin emprunté"""
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


class gamestate():
    """Objet du jeu, permettant de passer de scène en scène, c'est-à-dire, par exemple, de passer du menu au jeu."""
    #subclass :
    class Personnage(pygame.sprite.Sprite):
        """Class personnage permettant de lister les attributs
        d'un personnage tel que sa positon ou son inventaire"""
        def __init__(self):
            super().__init__()
            """Création d'un personnage avec sa position et son inventaire"""
            self.inventaire={"Torche":False} #Objet non présent & non utilisé, perspective d'évolution.
            self.pos=[0,0]
            self.sprite_sheet = pygame.image.load('Sprites/Char/SpriteSheetLink.png').convert_alpha()
            self.spriteslist=[]
            self.mouv=[2, 3, 6, 3, 2, 2, 3, 6, 3, 2] #list du nombre de pixel à décaler dans la direction du
            #mouvement à chaque sprite de l'animation.

            #Récupération des sprites du personnage depuis la sprites sheet
            #pour s'en servir dans l'animation dans les méthodes haut, bas, gauche et droite.
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

        #Méthodes pour modifier les coordonnées du personnage et animer son mouvement.
        def gauche(self,group):
            #Mise-à-jour de la position du joueur.
            self.pos[0]-=1
            #boucle pour animer le mouvement
            for i in range(len(self.mouv)):
                self.image=self.spriteslist[2][i]
                self.JRect=self.JRect.move(-self.mouv[i], 0)
                game_state.CharacterRect=game_state.CharacterRect.move(-self.mouv[i], 0)
                game_state.Gameboard.fill((0,0,0,0))
                self.rect=self.JRect
                group.draw(game_state.Gameboard)
                pygame.display.update(self)
                pygame.time.delay(7*i)
                game_state.Update()
            game_state.Gameboard.fill((0,0,0,0))
            self.image=self.spriteslist[0][1]
            group.draw(game_state.Gameboard)
            pygame.display.update(self)

        def droite(self, group):

            self.pos[0]+=1
            #boucle pour animer le mouvment
            for i in range(len(self.mouv)):
                self.image=self.spriteslist[4][i]
                self.JRect=self.JRect.move(self.mouv[i], 0)
                game_state.CharacterRect=game_state.CharacterRect.move(self.mouv[i], 0)
                game_state.Gameboard.fill((0,0,0,0))
                self.rect=self.JRect
                group.draw(game_state.Gameboard)
                pygame.display.update(self)
                pygame.time.delay(7*i)
                game_state.Update()
            game_state.Gameboard.fill((0,0,0,0))
            self.image=self.spriteslist[0][3]
            group.draw(game_state.Gameboard)
            pygame.display.update(self)

        def haut(self, group):

            self.pos[1]-=1
            #boucle pour animer le mouvment
            for i in range(len(self.mouv)):
                self.image=self.spriteslist[3][i]
                self.JRect=self.JRect.move(0, -self.mouv[i])
                game_state.CharacterRect=game_state.CharacterRect.move(0, -self.mouv[i])
                game_state.Gameboard.fill((0,0,0,0))
                self.rect=self.JRect
                group.draw(game_state.Gameboard)
                pygame.display.update(self)
                pygame.time.delay(7*i)
                game_state.Update()
            game_state.Gameboard.fill((0,0,0,0))
            self.image=self.spriteslist[0][2]
            group.draw(game_state.Gameboard)
            pygame.display.update(self)

        def bas(self, group):

            self.pos[1]+=1
            #boucle pour animer le mouvment
            for i in range(len(self.mouv)):
                self.image=self.spriteslist[1][i]
                self.JRect=self.JRect.move(0, self.mouv[i])
                game_state.CharacterRect=game_state.CharacterRect.move(0, self.mouv[i])
                game_state.Gameboard.fill((0,0,0,0))
                self.rect=self.JRect
                group.draw(game_state.Gameboard)
                pygame.display.update(self)
                pygame.time.delay(7*i)
                game_state.Update()
            game_state.Gameboard.fill((0,0,0,0))
            self.image=self.spriteslist[0][0]
            group.draw(game_state.Gameboard)
            pygame.display.update(self)
    #adhb
    def test():
        print("gg")
    class bouton():
        """objet définisant un bouton de l'interface graphique Pygame."""
        def __init__(self,sprite,x,y):
            self.sprite=sprite
            self.x=x
            self.y=y
        def draw(self,surface):
            """Afficher le bouton sur la surface souhaité."""
            surface.blit(self.sprite,(self.x,self.y))

        def isOver(self,pos):
            """Méthode permettant de savoir si une position est par dessus le bouton.
            Retourne TRUE si elle l'est et FALSE si elle ne l'est pas"""
            if pos[0]> self.x and pos[0] < self.x+self.sprite.get_width():
                if pos[1]>self.y and pos[1]< self.y + self.sprite.get_height():
                    return True
            return False
	
	#Fonctions transformées en méthodes :
    def Update(self):
        """Fonction permettant de mettre à 'recharger' l'affichage de l'écran."""
        self.fenetre.fill((0,0,0))
        self.Game.blit(self.Labyrinth,(64,64))
        self.Game.blit(self.Gameboard,(64,64))
        sub = self.Game.subsurface(self.CharacterRect)
        self.Camera=pygame.Surface((160,160),pygame.SRCALPHA)
        self.Camera=self.Camera.convert_alpha()
        self.Camera.blit(sub,(0,0))
        self.Camera = pygame.transform.scale(self.Camera,(396,396))
        self.fenetre.blit(self.Camera,(12,12))
        self.fenetre.blit(self.Interface,(0,0))
        pygame.display.flip()
    
    #Affichage du Donjon
    def drawdonjon(self,Donjon):
        def drawint(Donjon): 
            """Fonction permettant de d'afficher une grille sur la surface Background.
            Prend en paramètres un donjon."""
            coord_x=Donjon.pos[0]*32
            coord_y=Donjon.pos[1]*32
            self.Labyrinth.blit(self.SpriteMaze[4],(coord_x,coord_y))#sol
            if Donjon.murs["N"]==True and Donjon.murs["O"]==True:
                self.Labyrinth.blit(self.SpriteMaze[0],(coord_x,coord_y))#coin
            elif Donjon.murs["N"]==False and Donjon.murs["O"]==True :
                self.Labyrinth.blit(self.SpriteMaze[2],(coord_x,coord_y))#gauche
            elif Donjon.murs["O"]==False and Donjon.murs["N"]==True:
                self.Labyrinth.blit(self.SpriteMaze[1],(coord_x,coord_y))#haut
            elif Donjon.murs["O"]==False and Donjon.murs["N"]==False:
                self.Labyrinth.blit(self.SpriteMaze[3],(coord_x,coord_y))#vide
            self.Game.blit(self.Labyrinth,(64,64))
            if Donjon.gauche!=None:
                drawint(Donjon.gauche)
            if Donjon.droit!=None:
                drawint(Donjon.droit)
        drawint(Donjon.grille)


        #Affichage des bords droit du donjon
        coord_x=Donjon.nx*32
        coord_y=Donjon.ny*32
        for y in range(0,coord_y,32):
            self.Labyrinth.blit(self.SpriteMaze[2],(coord_x,y))
            self.Game.blit(self.Labyrinth,(64,64))

        #Affichage des bords inférieur du donjon
        for x in range(0,coord_x,32):
            self.Labyrinth.blit(self.SpriteMaze[1],(x,coord_y))
            self.Game.blit(self.Labyrinth,(64,64))

    
    def VerifObj(self, dico, pos, obj):
        """Fonction permettant de vérifier si le joueur deux coordonnées sont les mêmes,
        elle sera utilisée pour savoir si le joueur est sur la même cellule que l'objet"""
        res=False
        for item in dico:
            if dico.get(obj)==pos:
                res=True
        return res

    
    def init_player_tresor(self):
        """Fonction qui permet de définir la position aléatoire du Trésor. Il est placé aléatoirement dans
        le quart inférieur droit de l'écran.
        Retourne un objet trésor de position aléatoire."""
        self.Tresor=Objet("Trésor", [self.x, self.y])
        tx=random.randint(self.Tresor.pos[0]-(self.Tresor.pos[0]//4), self.Tresor.pos[0])
        ty=random.randint(self.Tresor.pos[1]-(self.Tresor.pos[1]//4), self.Tresor.pos[1])
        self.Tresor.pos[0]=tx-1
        self.Tresor.pos[1]=ty-1
        self.Objets["Tresor"]=self.Tresor.pos
        self.Gameboard.fill((0,0,0,1))
        self.Gameboard.blit(self.PFront,(self.CharacterRect.centerx,self.CharacterRect.centery))
        self.Labyrinth.blit(self.TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
    
    def reset(self):
        """Fonction permettant de Remettre la position du joueur et de son sprite en (0,0),
        réinitialiser son inventaire, et de replacer aléatoirement le trésor.
        Retourne Tous les objets/variables réinintialisées."""
        self.Joueur.inventaire["Tresor"]=False
        self.Joueur.pos[0]=0
        self.Joueur.pos[1]=0
        self.Gameboard.fill((0,0,0,1))
        self.Labyrinth.fill((0,0,0,1))
        self.CharacterRect.x=0
        self.CharacterRect.y=0
        self.Joueur.rect=pygame.Rect(4,4,28,28)
        self.Joueur.JRect=self.Joueur.rect
        self.init_player_tresor()
        self.Donjons=[]
        self.Donjons.append(Grille(self.x,self.y))

    def __init__(self):
        
        
        #Définition de la fenêtre:
        self.size = (1500,1500)
        
        self.fenetre=pygame.display.set_mode((600,600))#fenêtre de taille 640*480
        self.CharacterRect=pygame.Rect(-64,-64,160,160)
        
        #Chargement des murs
        self.SpriteMaze=(pygame.image.load('Sprites/Walls/Corner.png').convert_alpha(),
                    pygame.image.load('Sprites/Walls/Upper.png').convert_alpha(),
                    pygame.image.load('Sprites/Walls/Left.png').convert_alpha(),
                    pygame.image.load('Sprites/Walls/None.png').convert_alpha(),
                    pygame.image.load('Sprites/Walls/Floor.png').convert_alpha())

        self.PFront=pygame.image.load('Sprites/Char/PFront.png').convert_alpha()

        #Chargement Des sprites Items
        self.TresorImg=pygame.image.load('Sprites/Items/diamant.png').convert_alpha()

        #Chargement des interfaces utilisateurs
        self.IntroBG=pygame.image.load('Sprites/Menu/UI/Menu.png').convert_alpha()
        self.imgBtnCampagne=(pygame.image.load('Sprites/Menu/Boutons/Normal/Campagne.png').convert_alpha(),
                     pygame.image.load('Sprites/Menu/Boutons/Clicked/Campagne.png').convert_alpha(),)
        self.imgBtnCasual=(pygame.image.load('Sprites/Menu/Boutons/Normal/Casual.png').convert_alpha(),
                   pygame.image.load('Sprites/Menu/Boutons/Clicked/Casual.png').convert_alpha())
        self.imgBtnEndless=(pygame.image.load('Sprites/Menu/Boutons/Normal/Endless.png').convert_alpha(),
                    pygame.image.load('Sprites/Menu/Boutons/Clicked/Endless.png').convert_alpha())
        self.imguc=pygame.image.load('Sprites/Menu/UI/UC.png').convert_alpha()#image Under Construction
        self.imguc=pygame.transform.scale(self.imguc,(128,104))

        self.Interface=pygame.image.load('Sprites/Menu/UI/Interface.png').convert_alpha()
        #Définition des surfaces:
        #Invisibles
        self.UC=pygame.Surface(self.size,pygame.SRCALPHA)
        self.UC.blit(self.imguc,(300-64,300-32))
        self.Labyrinth=pygame.Surface(self.size,pygame.SRCALPHA) #Background (jamais affichée)
        self.Labyrinth=self.Labyrinth.convert_alpha()
        self.Labyrinth.fill((0,0,0,0))
        self.Gameboard=pygame.Surface(self.size,pygame.SRCALPHA) #Surface de tous les éléments interractibles. (jamais affichée)
        self.Gameboard=self.Gameboard.convert_alpha()

        #Affichée
        self.Game=pygame.Surface(self.size,pygame.SRCALPHA) #Concaténation de Labyrinth et Gameboard
        self.Game=self.Game.convert_alpha()
        self.Camera=pygame.Surface((160,160),pygame.SRCALPHA) #Surface qui sera affiché dans L'UI
        self.Camera=self.Camera.convert_alpha()
        
        #Initialisation des boutons
        self.btnCampagne=self.bouton(self.imgBtnCampagne[0],175,265)
        self.btnCasual=self.bouton(self.imgBtnCasual[0],175,355)
        self.btnEndless=self.bouton(self.imgBtnEndless[0],175,455)
        
        #Définitions des variables du jeu        
        self.allstate=["intro","endless","UC"] #Liste de toutes les scènes du jeu
        self.etat = self.allstate[1] #Scène actuel du jeu (index à changer selon la scène souhaité au lancement)
        self.boucle= True
        self.Joueur=self.Personnage()
        self.my_group = pygame.sprite.Group(self.Joueur)
        self.Donjons=[]
        self.x,self.y=5,5
        self.Tresor=None
        self.Objets={}#Dictionnaire des tous les objets présents, seul le trésor y est présent pour le moment
        self.init_player_tresor()
        self.Camera = pygame.transform.scale(self.Camera,(160,160))
        
        #self.Joueur,self.Donjons,self.Tresor.pos[0],self.Tresor.pos[1],self.CharacterRect, self.Joueur=
        self.reset()
        #self.Joueur,self.Donjons,self.Tresor,self.x,self.y,self.CharacterRect,self.Joueur)



	#Méthode de scène :
    def uc(self):
        self.UC.fill((0,0,0))
        self.UC.blit(self.imguc,(300-64,300-52))
        self.fenetre.blit(self.UC,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==QUIT: #Appuie sur la croix.
                self.boucle = False #Sortie de boucle
            if event.type==MOUSEBUTTONDOWN:
                #Sortie de scènes = "Déchargement"
                self.Labyrinth.fill((0,0,0))
                self.Gameboard.fill((0,0,0))
                pygame.display.flip()
                self.etat=self.allstate[0]
    
    def intro(self):
        self.Labyrinth.fill((0,0,0,1))
        self.Gameboard.fill((0,0,0,1))
        self.Labyrinth.blit(self.IntroBG,(0,0))
        self.btnEndless.draw(self.Gameboard)
        self.btnCampagne.draw(self.Gameboard)
        self.btnCasual.draw(self.Gameboard)
        self.fenetre.blit(self.Labyrinth,(0,0))
        self.fenetre.blit(self.Gameboard,(0,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            
            if event.type==QUIT:
                self.boucle = False
            if event.type==MOUSEBUTTONDOWN:
                if self.btnEndless.isOver(pos):
                    #ligne ci-dessous à mettre en commentaire si on souhaite garder le même laby en endless
                    #lorsqu'on retourne au menu
                    self.reset()
                    self.Labyrinth.fill((0,0,0,1))
                    self.Gameboard.fill((0,0,0,1))
                    self.Game.fill((0,0,0,1))
                    self.fenetre.fill((0,0,0))
                    self.drawdonjon(self.Donjons[-1])
                    self.Gameboard.blit(self.PFront,self.CharacterRect)
                    self.Labyrinth.blit(self.TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                    self.Game.blit(self.Labyrinth,(64,64))
                    self.Game.blit(self.Gameboard,(64,64))
                    pygame.display.flip()
                    self.fenetre.blit(self.Interface,(0,0))
                    self.etat=self.allstate[1]
                
                if self.btnCampagne.isOver(pos):
                    self.etat=self.allstate[2]
                if self.btnCasual.isOver(pos):
                    self.etat=self.allstate[2]
                
            if event.type == pygame.MOUSEMOTION:
                if self.btnEndless.isOver(pos):
                    self.btnEndless.sprite=self.imgBtnEndless[1]
                elif self.btnCampagne.isOver(pos):
                    self.btnCampagne.sprite=self.imgBtnCampagne[1]
                elif self.btnCasual.isOver(pos):
                    self.btnCasual.sprite=self.imgBtnCasual[1]
                else:
                    self.btnEndless.sprite=self.imgBtnEndless[0]
                    self.btnCampagne.sprite=self.imgBtnCampagne[0]
                    self.btnCasual.sprite=self.imgBtnCasual[0]
                    
        
        
    def endless(self):
        """Definition qui correspond à la scène de jeu du mode endless(qui se répète)"""
       
        for event in pygame.event.get():
            if event.type==QUIT:
                self.boucle = False
            if event.type==KEYDOWN:
                
                #Récupération des informations sur les murs aux alentours
                murN=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)['N']
                murS=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1]+1, self.Donjons[0].grille)['N']
                murO=self.Donjons[0].GetMurs(self.Joueur.pos[0]+1,self.Joueur.pos[1], self.Donjons[0].grille)["O"]
                murE=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)["O"]
                
                if event.key==K_ESCAPE: #Touche échap
                    self.Labyrinth.fill((0,0,0))
                    self.Gameboard.fill((0,0,0))
                    pygame.display.flip()
                    self.etat=self.allstate[0]
                
                if event.key==K_LEFT: #flèche gauche
                    if self.Joueur.pos[0]!=0 and murE==False:
                            self.Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Joueur.gauche(self.my_group)
                        

                if event.key==K_RIGHT: #flèche droite
                    
                    if self.Joueur.pos[0]+1<self.Donjons[0].nx and murO==False:
                            
                            self.Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Joueur.droite(self.my_group)

                            
                if event.key==K_UP: #flèche haut
                    if self.Joueur.pos[1]!=0 and murN==False:
                            
                            self.Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Joueur.haut(self.my_group)

            
                if event.key==K_DOWN: #flèche bas
                    if self.Joueur.pos[1]+1<self.Donjons[0].ny and murS==False:
                            
                            self.Gameboard.fill((0,0,0,0))
                            #Labyrinth.blit(TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
                            self.Joueur.bas(self.my_group)

                if self.VerifObj(self.Objets, self.Joueur.pos, "Tresor")==True and self.Joueur.inventaire["Tresor"]==False:
                    self.Joueur.inventaire["Tresor"]=True #Rempli l'inventaire.
                    #retirer le commentaire ci-dessous pour fermer le jeu lors de la récupération du trésor.
                    #pygame.quit()
                    self.reset()
                    self.drawdonjon(self.Donjons[-1])
                    self.Gameboard.fill((0,0,0,1))
                    self.Gameboard.blit(self.PFront,self.CharacterRect)
                    self.Labyrinth.blit(self.TresorImg,((self.Tresor.pos[0])*32,(self.Tresor.pos[1])*32))
        self.Update()
        
    def gestionnaire_de_scene(self):
        """Méthode qui permet de basculer d'une scène à l'autre"""
        if self.etat == self.allstate[0]:
            self.intro()
        if self.etat == self.allstate[1]:
            self.endless()
        if self.etat == self.allstate[2]:
            self.uc()