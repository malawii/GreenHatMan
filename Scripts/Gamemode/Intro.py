import pygame
from pygame.locals import *
import random

from Scripts import UI

class gamemode():
    def __init__(self,fenetre):
        self.IntroBG=pygame.image.load('Sprites/Menu/UI/Menu.png').convert_alpha()
        
        self.imgBtnCampagne=(pygame.image.load('Sprites/Menu/Boutons/Normal/Campagne.png').convert_alpha(),
                        pygame.image.load('Sprites/Menu/Boutons/Clicked/Campagne.png').convert_alpha(),)
        self.imgBtnCasual=(pygame.image.load('Sprites/Menu/Boutons/Normal/Casual.png').convert_alpha(),
                      pygame.image.load('Sprites/Menu/Boutons/Clicked/Casual.png').convert_alpha())
        self.imgBtnEndless=(pygame.image.load('Sprites/Menu/Boutons/Normal/Endless.png').convert_alpha(),
                       pygame.image.load('Sprites/Menu/Boutons/Clicked/Endless.png').convert_alpha())
                    
        self.btnCampagne=UI.bouton(self.imgBtnCampagne[0], self.imgBtnCampagne[1], 175,265)
        self.btnCasual=UI.bouton(self.imgBtnCasual[0], self.imgBtnCasual[1],175,355)
        self.btnEndless=UI.bouton(self.imgBtnEndless[0], self.imgBtnEndless[1], 175,455)
        
        self.size = (1500,1500)
        
        self.Fond = pygame.Surface(self.size,pygame.SRCALPHA)
        self.Fond = self.Fond.convert_alpha()
        self.Fond.fill((0,0,0,0))
        self.Fond.blit(self.IntroBG,(0,0))
            
        self.Interactible = pygame.Surface(self.size,pygame.SRCALPHA)
        self.Interactible = self.Interactible.convert_alpha()
        self.Interactible.fill((0,0,0,0))
        self.btnCampagne.draw(self.Interactible)
        self.btnCasual.draw(self.Interactible)
        self.btnEndless.draw(self.Interactible)
        
        fenetre.blit(self.Fond,(0,0))
        fenetre.blit(self.Interactible,(0,0))
        pygame.display.flip()
        
        
        
    def Intro_on(self, fenetre,etat):
        """Affichage du menu de démarrage du jeu
        Args: Labyrinth(Surface), Gameboard(Surface), Game(Surface), fenetre(pygame screen), btnEndless, btnCampagne, btnCasual (btn),IntroBG, TresorImg, Interface (img), boucle, Donjons, PFront, CharacterRect, Tresor,  
        Agrs : fenetre
        Returns:
        """
        fenetre.blit(self.Fond,(0,0))
        fenetre.blit(self.Interactible,(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            self.pos=pygame.mouse.get_pos()
            
            if event.type==QUIT:
                return "QUIT"
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE: #Touche échap
                    return "QUIT"
                if event.key == pygame.K_f: #Fullscreen en appuyant sur f
                    pygame.display.toggle_fullscreen()
            
            if event.type==MOUSEBUTTONDOWN:
                if self.btnEndless.isOver(self.pos):
                    #lancement de endless
                    return "to endless"
                if self.btnCampagne.isOver(self.pos):
                    return "QUIT"
                if self.btnCasual.isOver(self.pos):
                    return "QUIT"
            #Surligner le bouton survolé
            if event.type == pygame.MOUSEMOTION:
                if self.btnEndless.isOver(self.pos):
                    self.Interactible.fill((0,0,0,0))
                    self.btnCampagne.draw(self.Interactible)
                    self.btnCasual.draw(self.Interactible)
                    self.btnEndless.drawOver(self.Interactible)
                    pygame.display.flip()
                    
                elif self.btnCampagne.isOver(self.pos):
                    self.Interactible.fill((0,0,0,0))
                    self.btnCampagne.drawOver(self.Interactible)
                    self.btnCasual.draw(self.Interactible)
                    self.btnEndless.draw(self.Interactible)
                    pygame.display.flip()
                elif self.btnCasual.isOver(self.pos):
                    self.Interactible.fill((0,0,0,0))
                    self.btnCampagne.draw(self.Interactible)
                    self.btnCasual.drawOver(self.Interactible)
                    self.btnEndless.draw(self.Interactible)
                else:
                    self.Interactible.fill((0,0,0,0))
                    self.btnCampagne.draw(self.Interactible)
                    self.btnCasual.draw(self.Interactible)
                    self.btnEndless.draw(self.Interactible)
                
        return "intro"                