import pygame
from pygame.locals import *
pygame.init()


#Variables paramètres
framerate=pygame.time.Clock().tick(60)
pygame.key.set_repeat(150,30)

color = (200,200,200)
size = (1500,1500)
#x, y=5,5
#Création de la fenêtre de l'application
fenetre=pygame.display.set_mode((600,600))#fenêtre de taille 640*480

#Chargement des murs
SpriteMaze=(pygame.image.load('Sprites/Walls/Corner.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Upper.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Left.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/None.png').convert_alpha(),
            pygame.image.load('Sprites/Walls/Floor.png').convert_alpha())

#Chargement des sprites personnages
PFront=pygame.image.load('Sprites/Char/PFront.png').convert_alpha()
#PFront=pygame.transform.scale(PFront,(24,24))
PLeft=pygame.image.load('Sprites/Char/PLeft.png').convert_alpha()
#PLeft=pygame.transform.scale(PLeft,(24,24))
PBack=pygame.image.load('Sprites/Char/PBack.png').convert_alpha()
#PBack=pygame.transform.scale(PBack,(24,24))
PRight=pygame.image.load('Sprites/Char/PRight.png').convert_alpha()
#PRight=pygame.transform.scale(PRight,(24,24))
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

btnCampagne=bouton(imgBtnCampagne[0],175,265)
btnCasual=bouton(imgBtnCasual[0],175,355)
btnEndless=bouton(imgBtnEndless[0],175,455)

Camera=pygame.Surface((160,160),pygame.SRCALPHA) #Surface qui sera affiché dans L'UI
Camera=Camera.convert_alpha()
#Définition des surfaces
UC=pygame.Surface(size,pygame.SRCALPHA)
UC.blit(imguc,(300-64,300-32))
#Invisibles
Labyrinth=pygame.Surface(size,pygame.SRCALPHA) #Background (jamais affichée)
Labyrinth=Labyrinth.convert_alpha()
Labyrinth.fill((0,0,0,0))
Gameboard=pygame.Surface(size,pygame.SRCALPHA) #Surface de tous les éléments interractibles. (jamais affichée)
Gameboard=Gameboard.convert_alpha()
Game=pygame.Surface(size,pygame.SRCALPHA) #Concaténation de Labyrinth et Gameboard
Game=Game.convert_alpha()
#Affichées

#SCamera.fill((0,0,0,0))
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
            Game.blit(Labyrinth,(64,64))
            #pygame.display.flip()
        coord_x=0
        coord_y+=32
    #Affichage des bords droit du donjon
    coord_x=Donjon.nx*32
    for y in range(0,coord_y,32):
        Labyrinth.blit(SpriteMaze[2],(coord_x,y))
        Game.blit(Labyrinth,(64,64))
        #pygame.display.flip()
    #Affichage des bords inférieur du donjon
    coord_y=Donjon.ny*32
    for x in range(0,coord_x,32):
        Labyrinth.blit(SpriteMaze[1],(x,coord_y))
        Game.blit(Labyrinth,(64,64))
        #pygame.display.flip()


def reset(Joueur,Donjons,Tresor,x,y,CharacterRect):
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
    Tresor=init_player_tresor(Tresor,CharacterRect,x,y)
    Donjons=[]
    Donjons.append(Grille(x,y))
    #drawdonjon(Donjons[-1])
    return Joueur,Donjons,Tresor.pos[0],Tresor.pos[1],CharacterRect

#Lancement du jeu
game_state = gamestate(Camera)
pygame.display.flip()
print(game_state.Tresor.pos)
while game_state.boucle:
    game_state.gestionnaire_de_scene()
pygame.quit()