import pygame as pg
from pygame.locals import *
import random


class Poderes(pg.sprite.Sprite):
    #CLASSSE PRINCIPAL DOS PODERES
    def __init__(self,tipo,imagem,TELA_LARGURA,TELA_ALTURA):
        super(Poderes,self).__init__()
        self.tipo = tipo
        self.velocidade = 7
        self.surf = pg.image.load(imagem).convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center=(
            TELA_LARGURA+50, random.randint(0,TELA_ALTURA)
            )
        )

    #ATUALIZA POSICAO DO POWERUP
    def update(self):
        self.rect.move_ip(-self.velocidade,0)
        if self.rect.right < 0:
            self.kill()


class Vida(Poderes): # RECUPERAR VIDA
    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__('VIDA',"Poderes/vida.png",TELA_LARGURA,TELA_ALTURA)
        #DEFINE O VALOR RECUPERADO, SPRITE E HITBOX DO POWERUP
        self.vida = 20 


class Dose(Poderes): # RECUPERAR DOSE
    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__('DOSE',"Poderes/dose.png",TELA_LARGURA,TELA_ALTURA)
        self.dose = 15  
      

        
        
