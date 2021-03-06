########
import random

import pygame
from pygame.locals import *

from Scripts.Gamemode import Endless, Intro
from Scripts import Generate,UI,Objet
        
fenetre=pygame.display.set_mode((600,600),pygame.SCALED | pygame.RESIZABLE)#fenêtre de taille 640*480
etat = "intro"
boucle= True

pygame.init()

#Variables paramètres
framerate=pygame.time.Clock().tick(60)
pygame.key.set_repeat(5000,400)
pygame.display.flip()

scene_endless = Endless.gamemode(fenetre)
scene_intro = Intro.gamemode(fenetre)


if __name__ == "__main__":
    while boucle :
        if etat == "QUIT":
            boucle = False
            
        elif etat == "intro":
            etat = scene_intro.Intro_on(fenetre,etat)
            
        elif etat == "to endless":
            scene_endless.reset() 
            etat = "endless"
            
        elif etat == "endless":
            etat = scene_endless.Endless_on(fenetre)
            
        elif etat == "test":
            print("out of menu")
            scene_endless.Game.blit(scene_endless.PFront,(64,64))
            etat = "QUIT"
            
pygame.quit()