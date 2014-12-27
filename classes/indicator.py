import pygame, os
from functions import *

class ammoIndicator():
    def __init__(self):
        self.ammoNumber = 0 #define storage of shields
        self.cubeTemplate = pygame.image.load(os.path.join("Resources",\
                                                           "bulletInd.gif"))
        self.cubeTemplate = self.cubeTemplate.convert()
        self.surface = None #location to store our surface
        self.displayedAmmo = 0#number of shields displayed
        self.font = pygame.font.Font(None,18)
        self.fontSurface = self.font.render("Ammo: ",True,(255,255,255))
    def getSurface(self): #prepare and output a surface with the shields
        if self.surface and self.displayedAmmo == self.ammoNumber:
            return self.surface #if we don't need to make a surface return the
        #old one
        elif not self.surface: #make a surface if we need one
            self.surface = pygame.Surface(((155+self.fontSurface.get_width()),10))
            self.surface.fill((0,0,0)) #fill with the bg color
        self.surface.fill((0,0,0))
        count = self.fontSurface.get_width() + 5
        self.surface.blit(self.fontSurface,(0,0))
        for x in range(self.ammoNumber): #build surface
            self.surface.blit(self.cubeTemplate,(count,0))
            count += 15
        self.displayedAmmo = self.ammoNumber #we are displaying the number
        return self.surface
    def setAmmo(self,ammo):
        self.ammoNumber = ammo

#class to layout and return a surface containing the shields indicator
class shieldIndicator():
    def __init__(self):
        self.shieldNumber = 0 #define storage of shields
        self.cubeTemplate = pygame.image.load(os.path.join("Resources",\
                                                           "blue square.bmp"))
        self.cubeTemplate = self.cubeTemplate.convert()
        self.surface = None #location to store our surface
        self.displayedShields = 0#number of shields displayed
        self.font = pygame.font.Font(None,18)
        self.fontSurface = self.font.render("Shields: ",True,(255,255,255))
    def getSurface(self): #prepare and output a surface with the shields
        if self.surface and self.displayedShields == self.shieldNumber:
            return self.surface #if we don't need to make a surface return the
        #old one
        elif not self.surface: #make a surface if we need one
            self.surface = pygame.Surface(((105+self.fontSurface.get_width()),10))
            self.surface.fill((0,0,0)) #fill with the bg color
        self.surface.fill((0,0,0))
        count = self.fontSurface.get_width() + 5
        self.surface.blit(self.fontSurface,(0,0))
        for x in range(self.shieldNumber): #build surface
            self.surface.blit(self.cubeTemplate,(count,0))
            count += 35
        self.displayedShields = self.shieldNumber #we are displaying the number
        return self.surface
    def setShield(self,shield):
        self.shieldNumber = shield

#class to layout and create the bar
class progressIndicator():
    def __init__(self,color,label):
        self.percent = 0 #define storage of percent
        self.surface = None #location to store our surface
        self.displayedPercent = 0#number of percentage displayed
        self.label = label
        self.font = pygame.font.Font(None,18)
        self.fontSurface = self.font.render(self.label,True,(255,255,255))
        self.color = color
    def getSurface(self): #prepare and output a surface with the shields
        if self.surface and self.percent == self.displayedPercent:
            return self.surface #if we don't need to make a surface return the
        #old one
        elif not self.surface: #make a surface if we need one
            self.surface = pygame.Surface(((105+self.fontSurface.get_width()),15))
        self.surface.fill((0,0,0))
        self.surface.blit(self.fontSurface,(0,0))
        box = pygame.rect.Rect((self.fontSurface.get_width()+5,0,100,10))
        boxFill = box.move(1,1)
        boxFill.width = ((self.percent/100.0)*99)-1
        boxFill.height -= 1
        pygame.draw.rect(self.surface,self.color,box,1)
        if self.percent != 0:
            pygame.draw.rect(self.surface,self.color,boxFill)
        self.displayedPercent = self.percent #we are displaying the number
        return self.surface
    def setPercentage(self,percent):
        self.percent = percent
        debug(str(self.percent))
