import pygame
from pygame.locals import *
import random

from Scripts import Generate,Objet,UI

class gamemode():
    
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
       
    def init_player_tresor(self):
        """Fonction qui permet de définir la position aléatoire du Trésor. Il est placé aléatoirement dans le quart inférieur droit de l'écran."""
        Tresor=Objet.Objet("Trésor", [self.x, self.y])
        tx=random.randint(Tresor.pos[0]-(Tresor.pos[0]//4), Tresor.pos[0])
        ty=random.randint(Tresor.pos[1]-(Tresor.pos[1]//4), Tresor.pos[1])
        Tresor.pos[0]=tx-1
        Tresor.pos[1]=ty-1
        self.Objets["Tresor"]=Tresor
        self.Gameboard.fill((0,0,0,1))
        self.Gameboard.blit(self.PFront,(self.CharacterRect.x,self.CharacterRect.y))
        self.SurfItems.blit(self.TresorImg,((self.Objets["Tresor"].pos[0])*32,(self.Objets["Tresor"].pos[1])*32))
    
    def reset(self):
        """Fonction permettant de Remettre la position du joueur et de son sprite en (0,0), réinitialiser son inventaire, et de replacer aléatoirement le trésor."""
        self.Joueur.inventaire["Tresor"]=False #retirer le trésor  de l'inventaire du joueur
        self.Joueur.pos[0]=0 #remmetre le joueur en 0,0
        self.Joueur.pos[1]=0
        self.Gameboard.fill((0,0,0,1)) #clear les surfaces
        self.SurfItems.fill((0,0,0,1))
        self.Labyrinth.fill((0,0,0,1))
        self.CharacterRect.x=0 #remettre les rect en coordonnée de la grille 0,0
        self.CharacterRect.y=0 
        self.Joueur.rect=pygame.Rect(4,4,28,28)
        self.Joueur.JRect=self.Joueur.rect
        self.init_player_tresor() #recharger le trésor
        self.Donjons=[] #vider la liste des donjons (à ne pas faire hors Endless!)
        self.Donjons.append(Generate.Grille(self.x,self.y))#Générer une nouvelle grille
        self.drawdonjon(self.Donjons[-1]) #afficher la grille 
        self.Game.blit(self.Labyrinth,(64,64))
        self.Game.blit(self.SurfItems,(64,64))
        self.Game.blit(self.Gameboard,(64,64))
        
    def Update(self, fenetre):
        """fonction qui permet de rafraichir l'image"""
        self.Game.fill((0,0,0,0))
        self.Game.blit(self.Labyrinth,(64,64))
        self.Game.blit(self.SurfItems,(64,64))
        self.Game.blit(self.Gameboard,(64,64))
        sub = self.Game.subsurface(self.CharacterRect)
        self.Camera = pygame.transform.scale(self.Camera,(160,160))
        self.Camera.fill((0,0,0,0))
        self.Camera.blit(sub,(0,0))
        self.Camera = pygame.transform.scale(self.Camera,(396,396))
        fenetre.blit(self.Camera,(12,12))
        fenetre.blit(self.Interface,(0,0))
        

        
    def __init__(self, fenetre):
        fenetre.fill((0,0,0,0))
    
        self.SpriteMaze=(pygame.image.load('Sprites/Walls/Corner.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Upper.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Left.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/None.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Floor.png').convert_alpha())
        
        self.PFront=pygame.image.load('Sprites/Char/PFront.png').convert_alpha()
        self.TresorImg=pygame.image.load('Sprites/Items/diamant.png').convert_alpha()
        self.Interface=pygame.image.load('Sprites/Menu/UI/Interface.png').convert_alpha()
        
        self.size = (1500,1500)
        self.x,self.y = 10,10
        
        self.CharacterRect=pygame.Rect(-64,-64,160,160)
        
        self.Donjons=[]
        self.Donjons.append(Generate.Grille(self.x,self.y))
        
        self.Joueur = Objet.Personnage()
        self.my_group = pygame.sprite.Group(self.Joueur)
       
        self.Objets={}
        
        self.Labyrinth=pygame.Surface(self.size,pygame.SRCALPHA) #Background (jamais affichée) Immuable.
        self.Labyrinth=self.Labyrinth.convert_alpha()
        self.Labyrinth.fill((0,0,0,0))
        
        
        self.SurfItems=pygame.Surface(self.size,pygame.SRCALPHA) #Surface des objets interactibles (ramassables) type diamant. (jamais affichée)
        self.SurfItems=self.SurfItems.convert_alpha()
        self.SurfItems.fill((0,0,0,0))
        
        self.Gameboard=pygame.Surface(self.size,pygame.SRCALPHA) #Surface de tous les dynamiques types personnage. (jamais affichée)
        self.Gameboard=self.Gameboard.convert_alpha()
        self.Gameboard.fill((0,0,0,0))
        
        
        self.Game=pygame.Surface(self.size,pygame.SRCALPHA) #Concaténation de Labyrinth, SurfItems, Gameboard.
        self.Game=self.Game.convert_alpha()
        
        self.Camera=pygame.Surface((160,160),pygame.SRCALPHA) #Surface qui sera affiché dans L'UI. 160 correspond à un rayon de 5 cellules.
        self.Camera=self.Camera.convert_alpha()
        
        self.reset()
        
        pygame.display.flip()


    
    def Endless_on(self, fenetre):
        pygame.key.set_repeat(200)
        """Fonction pour afficher le mode de jeu Endless et gérer ses événements
        Args: fenetre (pygame window)
        Returns: str (Etat, changement de scene)
        """
        fenetre.fill((0,0,0,0))
        self.Update(fenetre)
        self.Camera=pygame.Surface((160,160),pygame.SRCALPHA)
        sub = self.Game.subsurface(self.CharacterRect)
        
        fenetre.blit(self.Camera,(12,12))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==QUIT:
                return "QUIT"
            if event.type==KEYDOWN:
                
                #Récupération des informations sur les murs aux alentours
                murN=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)['N']
                murS=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1]+1, self.Donjons[0].grille)['N']
                murO=self.Donjons[0].GetMurs(self.Joueur.pos[0]+1,self.Joueur.pos[1], self.Donjons[0].grille)["O"]
                murE=self.Donjons[0].GetMurs(self.Joueur.pos[0],self.Joueur.pos[1], self.Donjons[0].grille)["O"]
                
                if event.key==K_ESCAPE: #Touche échap
                    return "intro"
                
                if event.key == pygame.K_f: #fullscreen/windowed en appuyant sur f
                    pygame.display.toggle_fullscreen()
                
                if event.key==K_LEFT: #flèche gauche
                    #aller vers la gauche
                    if self.Joueur.pos[0]!=0 and murE==False:
                        #boucle d'animation
                        for i in range(len(self.Joueur.mouv)):
                            if pygame.event.peek(): #empécher les événements d'arriver dans la file pendant l'annimation.
                                pygame.event.clear()
                              
                            self.Joueur.image=self.Joueur.spriteslist[2][i]#changement du sprite actif
                            self.Joueur.JRect=self.Joueur.JRect.move(-self.Joueur.mouv[i], 0)#déplacement du rect du joueur
                            self.CharacterRect=self.CharacterRect.move(-self.Joueur.mouv[i], 0)#déplacement du rect autour du joueur
                            #Clear les surfaces qui seront modifiées
                            self.Gameboard.fill((0,0,0,0))
                            self.Game.fill((0,0,0,0))
                            fenetre.fill((0,0,0,0))
                            #afficher le sprite actif
                            self.my_group.draw(self.Gameboard)
                            self.Joueur.rect=self.Joueur.JRect
                            
                            #rafraichissement de l'image
                            self.Update(fenetre)
                            pygame.time.delay(7*i)
                            pygame.display.flip()
                        #affichage du sprite idle
                        self.Joueur.image=self.Joueur.spriteslist[0][1]
                        self.Gameboard.fill((0,0,0,0))
                        self.my_group.draw(self.Gameboard)
                        self.Update(fenetre)
                        
                        pygame.display.flip()
                        self.Joueur.pos[0]-=1
                        

                if event.key==K_RIGHT: #flèche droite
                    #aller vers la droite
                    if self.Joueur.pos[0]+1<self.Donjons[0].nx and murO==False:
                        #boucle d'animation
                        for i in range(len(self.Joueur.mouv)):
                            if pygame.event.peek():#empécher les événements d'arriver dans la file pendant l'annimation.
                                pygame.event.clear()
                            self.Joueur.image=self.Joueur.spriteslist[4][i]#changement du sprite actif
                            self.Joueur.JRect=self.Joueur.JRect.move(self.Joueur.mouv[i], 0)#déplacement du rect du joueur
                            self.CharacterRect=self.CharacterRect.move(self.Joueur.mouv[i], 0)#déplacement du rect autour du joueur
                            #Clear les surfaces qui seront modifiées
                            self.Gameboard.fill((0,0,0,0))
                            self.Game.fill((0,0,0,0))
                            fenetre.fill((0,0,0,0))
                            #afficher le sprite actif
                            self.my_group.draw(self.Gameboard)
                            self.Joueur.rect=self.Joueur.JRect
                            #rafraichissement de l'image
                            self.Update(fenetre)
                            pygame.time.delay(7*i)
                            pygame.display.flip()
                        #affichage du sprite idle    
                        self.Joueur.image=self.Joueur.spriteslist[0][3]
                        self.Gameboard.fill((0,0,0,0))
                        self.my_group.draw(self.Gameboard)
                        self.Update(fenetre)
                        
                        pygame.display.flip()
                        self.Joueur.pos[0]+=1
                        
                            
                if event.key==K_UP: #flèche haut
                    #aller vers le haut
                    if self.Joueur.pos[1]!=0 and murN==False:
                        #boucle d'animation
                        for i in range(len(self.Joueur.mouv)):
                            if pygame.event.peek():#empécher les événements d'arriver dans la file pendant l'annimation.
                                pygame.event.clear()
                            self.Joueur.image=self.Joueur.spriteslist[3][i]#changement du sprite actif
                            self.Joueur.JRect=self.Joueur.JRect.move(0,-self.Joueur.mouv[i])#déplacement du rect du joueur
                            self.CharacterRect=self.CharacterRect.move(0,-self.Joueur.mouv[i])#déplacement du rect autour du joueur
                            #Clear les surfaces qui seront modifiées
                            self.Gameboard.fill((0,0,0,0))
                            self.Game.fill((0,0,0,0))
                            fenetre.fill((0,0,0,0))
                            #afficher le sprite actif
                            self.my_group.draw(self.Gameboard)
                            self.Joueur.rect=self.Joueur.JRect
                            #rafraichissement de l'image
                            self.Update(fenetre)
                            pygame.time.delay(7*i)
                            pygame.display.flip()
                        #affichage du sprite idle  
                        self.Joueur.image=self.Joueur.spriteslist[0][2]
                        self.Gameboard.fill((0,0,0,0))
                        self.my_group.draw(self.Gameboard)
                        self.Update(fenetre)
                        
                        pygame.display.flip()
                        self.Joueur.pos[1]-=1

            
                if event.key==K_DOWN: #flèche bas
                    #aller vers le bas
                    if self.Joueur.pos[1]+1<self.Donjons[0].ny and murS==False:
                        
                        #boucle d'animation
                        for i in range(len(self.Joueur.mouv)):
                            if pygame.event.peek():#empécher les événements d'arriver dans la file pendant l'annimation.
                                pygame.event.clear()
                            self.Joueur.image=self.Joueur.spriteslist[1][i]#changement du sprite actif
                            self.Joueur.JRect=self.Joueur.JRect.move(0,self.Joueur.mouv[i])#déplacement du rect du joueur
                            self.CharacterRect=self.CharacterRect.move(0,self.Joueur.mouv[i])#déplacement du rect autour du joueur
                            #Clear les surfaces qui seront modifiées
                            self.Gameboard.fill((0,0,0,0))
                            self.Game.fill((0,0,0,0))
                            fenetre.fill((0,0,0,0))
                            #afficher le sprite actif
                            self.my_group.draw(self.Gameboard)
                            self.Joueur.rect=self.Joueur.JRect
                            #rafraichissement de l'image
                            self.Update(fenetre)
                            pygame.time.delay(7*i)
                            pygame.display.flip()
                        #affichage du sprite idle  
                        self.Joueur.image=self.Joueur.spriteslist[0][0]
                        self.Gameboard.fill((0,0,0,0))
                        self.my_group.draw(self.Gameboard)
                        self.Update(fenetre)
                        
                        pygame.display.flip()
                        self.Joueur.pos[1]+=1

                if Objet.VerifObj(self.Objets, self.Joueur.pos, "Tresor")==True and self.Joueur.inventaire["Tresor"]==False:
                    self.Joueur.inventaire["Tresor"]=True #Rempli l'inventaire.
                    #retirer le commentaire ci-dessous pour fermer le jeu lors de la récupération du trésor.
                    #return "QUIT"
                    self.reset()
                    pygame.event.clear()
        return "endless"