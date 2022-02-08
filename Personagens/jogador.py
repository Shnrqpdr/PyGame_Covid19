import pygame as pg
from pygame.locals import *
from Projeteis.projeteis import *

class Jogador(pg.sprite.Sprite):
    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super(Jogador,self).__init__()
        #CARREGANDO O SPRITE DO JOGADOR E DEFININDO SUA HITBOX
        self.surf = pg.image.load("Personagens/ze.png").convert()
        self.surf.set_colorkey((0,255,0),RLEACCEL)
        self.rect = self.surf.get_rect(center = (TELA_LARGURA/2,TELA_ALTURA/2))

        #DIMINUINDO A HITBOX DO JOGADOR
        self.rect.w = self.rect.w * 0.7
        self.rect.h = self.rect.h * 0.7

        #VALORES PARA A VIDA, DOSE, VELOCIDADE E A BARRA DE VIDA/DOSE
        self.barras = pg.image.load("Personagens/barras.png").convert()
        self.velocidade = 8
        self.vidaMAX = 100
        self.vida = self.vidaMAX
        self.doseMAX = 75
        self.dose = self.doseMAX
        self.pontos = 0
        self.poder = 1.


    # ATUALIZACAO DO JOGADOR A CADA FRAME
    def update(self,teclas,TELA_LARGURA,TELA_ALTURA):
        if teclas[K_UP]:
            if self.rect.top > 0:
                self.rect.move_ip(0,-self.velocidade)
        if teclas[K_DOWN]:
            if self.rect.bottom < TELA_ALTURA-30:
                self.rect.move_ip(0,self.velocidade)
        if teclas[K_LEFT]:
            if self.rect.left > 0:
                self.rect.move_ip(-self.velocidade,0)
        if teclas[K_RIGHT]:
            if self.rect.right < TELA_LARGURA-30:
                self.rect.move_ip(self.velocidade,0)

        # ATUALIZA A BARRA DE VIDA
        self.barra_vida=pg.Surface((int((self.vida/self.vidaMAX)*100),30))
        self.barra_vida.fill((24,121,242))

        # ATUALIZA A BARRA DE DOSES
        self.barra_dose=pg.Surface((int((self.dose/self.doseMAX)*100),30))
        self.barra_dose.fill((230,195,77))
        
        
        
