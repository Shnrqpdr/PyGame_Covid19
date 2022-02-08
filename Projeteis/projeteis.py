import pygame as pg
from pygame.locals import *
import random



class Vacina(pg.sprite.Sprite):
    #PROJETIL DO JOGADOR   
    custo = 5
    def __init__(self, origem):
        super(Vacina,self).__init__()
        #DEFINE O DANO, VELOCIDADE, SPRITE E HITBOX
        self.dano = 10
        self.surf = pg.image.load("Projeteis/vacina.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = origem)
        self.velocidade = 10

    #ATUALIZA A POSICAO DO PROJETIL
    def update(self,TELA_LARGURA):
        self.rect.move_ip(self.velocidade,0)
        if self.rect.left > TELA_LARGURA:
            self.kill()


class Cloroquina(pg.sprite.Sprite):
    #PROJETIL 1 DO CHEFE
    
    def __init__(self, origem):
        super(Cloroquina,self).__init__()
        #DEFINE O DANO, VELOCIDADE, SPRITE E HITBOX
        self.dano = 10
        self.surf = pg.image.load("Projeteis/cloroquina.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = origem)

        #CADA TIRO TEM VELOCIDADE EM Y ALEATORIA ENTRE 10 E 25
        self.velocidade = random.randint(10,25)

    #ATUALIZA A POSICAO DO PROJETIL
    def update(self,jogador):
        self.rect.move_ip(-self.velocidade,0)
        if self.rect.right < 0:
            self.kill()


class Ivermectina(pg.sprite.Sprite):
    #PROJETIL 2 DO CHEFE
    
    def __init__(self, origem):
        super(Ivermectina,self).__init__()
        #DEFINE O DANO, VELOCIDADE, SPRITE E HITBOX
        self.dano = 10
        self.surf = pg.image.load("Projeteis/ivermectina.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = origem)
        self.velocidade = 5

    #ATUALIZA A POSICAO DO PROJETIL
    def update(self,jogador):
        # VETOR DA DIFERENÇA ENTRE A POSICAO DO TIRO E DO JOGADOR
        vetor = pg.math.Vector2(jogador.rect.x - self.rect.x,
                                 jogador.rect.y - self.rect.y)
        # VETOR DA DIFERENÇA É NORMALIZADO E ESCALADO DE ACORDO COM A VELOCIDADE
        vetor.normalize()
        vetor.scale_to_length(self.velocidade)
        #PROJETIL DE MOVE NA DIRECAO DESTE VETOR
        self.rect.move_ip(vetor)
        if self.rect.right < 0:
            self.kill()


class Hidroxicloroquina(pg.sprite.Sprite):
    #PROJETIL 3 DO CHEFE
    
    def __init__(self, origem):
        super( Hidroxicloroquina,self).__init__()
        #DEFINE O DANO, VELOCIDADE, SPRITE E HITBOX
        self.dano = 10
        self.surf = pg.image.load("Projeteis/hidroxicloroquina.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center = origem)
         #CADA TIRO TEM VELOCIDADE EM Y ALEATORIA ENTRE -10 E 10 E EM X ENTRE -10 E -5
        self.velocidade = pg.math.Vector2(random.randint(-10,-5),random.randint(-10,10))

    #ATUALIZA A POSICAO DO PROJETIL
    def update(self,jogador):
        if self.rect.top < 0 or self.rect.bottom > 600:
            # VETOR VELOCIDADE E REFLETIDO EM Y SE ATINGE O LIMITE SUPERIOR/INFERIOR DA TELA
            self.velocidade.reflect_ip((0,1))
        self.rect.move_ip(self.velocidade)
        if self.rect.right < 0:
            self.kill()



