import pygame
from pygame.locals import *
import random

from Scripts import UI


def VerifObj(dico, pos, obj):
    """Fonction permettant de vérifier si le joueur deux coordonnées sont les mêmes,
    elle sera utilisée pour savoir si le joueur est sur la même cellule que l'objet"""
    res=False
    for item in dico:
        if dico.get(obj).pos==pos:
            res=True
    return res


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


class Objet():
    """Class définisant les objets du jeu"""
    def __init__(self, nom, pos):
        self.nom=nom
        self.pos=pos