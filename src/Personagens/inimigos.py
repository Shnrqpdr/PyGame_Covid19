import pygame as pg
from pygame.locals import *
import random
from Projeteis.projeteis import *

#CLASSE PRINCIPAL DOS INIMIGOS
class Inimigos(pg.sprite.Sprite):
    def __init__(self,vida,velocidade,pontos,imagem,TELA_ALTURA,TELA_LARGURA):
        super(Inimigos,self).__init__()
        self.vida = vida
        self.velocidade = velocidade
        self.pontos = pontos
        #CARREGA O SPRITE DO INIMIGO
        self.surf = pg.image.load(imagem).convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        #POSICIONA O INIMIGO EM UMA ALTUTA ALEATORIA FORA DA TELA NA DIREITA
        self.rect = self.surf.get_rect(center=(
            TELA_LARGURA+50, random.randint(0,TELA_ALTURA)
            )
        )
        #DIMINUI O HITBOX DO INIMIGO
        self.rect.w = self.rect.w * 0.7
        self.rect.h = self.rect.h * 0.7
                
    #ATUALIZA POSICAO DO INIMIGO  
    def update(self):
        self.rect.move_ip(-self.velocidade,0)
        if self.rect.right < 0:
            self.kill()


class Covid1(Inimigos):
    vida = 20
    velocidade = 7
    dano = 10
    pontos = 1
    def __init__(self,TELA_ALTURA,TELA_LARGURA):
        super().__init__(self.vida,self.velocidade,self.pontos,"Personagens/covid1.png",TELA_ALTURA,TELA_LARGURA)


        

class Covid2(Inimigos):
    vida = 10
    velocidade = 15
    dano = 15
    pontos = 3
    def __init__(self,TELA_ALTURA,TELA_LARGURA):
        super().__init__(self.vida,self.velocidade,self.pontos,"Personagens/covid2.png",TELA_ALTURA,TELA_LARGURA)


class Covid3(Inimigos):
    vida = 30
    velocidade = 5
    dano = 20
    pontos = 4
    def __init__(self,TELA_ALTURA,TELA_LARGURA):
        super().__init__(self.vida,self.velocidade,self.pontos,"Personagens/covid3.png",TELA_ALTURA,TELA_LARGURA)
        #DEFINE UM VETOR VELOCIDADE COM VX=-5 E VY ENTRE -5 E 5
        self.vvelocidade = pg.math.Vector2(-self.velocidade,random.randint(-self.velocidade,self.velocidade))

    #ATUALIZA POSICAO DO INIMIGO
    def update(self):
        if self.rect.top < 0 or self.rect.bottom > 600:
             #REFLETE O VETOR VELOCIDADE EM RELAÇÃO AO EIXO Y CASO ATINJA O LIMITE SUPERIOR/INFERIOR DA TELA
            self.vvelocidade.reflect_ip((0,1))
        self.rect.move_ip(self.vvelocidade)
        if self.rect.right < 0:
            self.kill()


class Covid4(Inimigos):
    vida = 40
    velocidade = 10
    dano = 25
    pontos = 5
    def __init__(self,TELA_ALTURA,TELA_LARGURA):
        super().__init__(self.vida,self.velocidade,self.pontos,"Personagens/covid4.png",TELA_ALTURA,TELA_LARGURA)

    #ATUALIZA POSICAO DO INIMIGO
    def update(self):
        # O QUANTO O INIMIGO SE MOVE A CADA FRAME E ESCOLHIDO DE FORMA ALEATORIA
        self.rect.move_ip(-random.randint(5,20),random.randint(-20,20))
        if self.rect.right < 0:
            self.kill()


class Chefe(Inimigos):
    vidaMAX = 500
    velocidade = 4
    dano = 1000
    timer = 50
    pontos = 100
    def __init__(self,TELA_ALTURA,TELA_LARGURA):
        super().__init__(self.vidaMAX,self.velocidade,self.pontos,"Personagens/bolso1.png",TELA_ALTURA,TELA_LARGURA)
        self.altura = TELA_ALTURA
        self.largura = TELA_LARGURA

        #CARREGA OS SPRITES UTILIZADOS NA ANIMACAO
        self.animacao=[]
        for i in range(2):
            self.animacao.append(pg.image.load("Personagens/bolso"+str(i+1)+".png").convert())
            self.animacao[i].set_colorkey((255,0,0),RLEACCEL)
        self.surf = self.animacao[0]
        self.rect = self.surf.get_rect(right = self.largura-10, bottom =self.altura/2)

        #CRIA UM CONTADOR DO TEMPO RESTANTE PARA ATIRAR
        self.temp_tiro = self.timer

        #COLOCA O CHEFE NO PRIMEIRO ESTAGIO
        self.fase1 = True

        #E ESCOLHIDO DE FORMA ALEATORIA SE O CHEFE COMECA SUBINDO OU DESCENDO
        if random.randint(0,100) < 50:
            self.desce = True
            self.sobe = False
        else:
            self.desce = False
            self.sobe = True

    #ATUALIZA POSICAO DO INIMIGO
    def update(self):
           
           # CHEFE SE MOVE PARA CIMA OU PARA BAIXO DE ACORDO COM O QUE FOR POSSIVEL
            if self.sobe:
                self.rect.move_ip(0,-self.velocidade)
                if self.rect.top < 0:
                    self.rect.top = 0
                    self.sobe = False
                    self.desce = True

            else:
                self.rect.move_ip(0,self.velocidade)
                if self.rect.bottom > self.altura:
                    self.rect.bottom = self.altura
                    self.sobe = True
                    self.desce = False

            #DECREMENTA O CONTADOR DO TIRO E TROCA O SPRITE DO CHEFE QUANDO CHEGA NA METADE
            self.temp_tiro -= 1
            if self.temp_tiro < self.timer/2:
                self.surf = self.animacao[0]
            else:
                self.surf = self.animacao[1]

            # CHEFE SAI DO ESTAGIO 1 QUANDO A VIDA CAI ABAIXO DA METADE
            if self.vida <= Chefe.vidaMAX/2 and self.fase1:
                self.velocidade*= 2
                self.timer-=5
                self.fase1 = False

            # ATUALIZA A BARRA DE VIDA
            self.barra_vida=pg.Surface((int((self.vida/self.vidaMAX)*800),30))
            if self.vida >= self.vidaMAX/2:
                R = int ((-510*self.vida/self.vidaMAX)+510)
                G = 255
            else:
                G = int (510*self.vida/self.vidaMAX)
                R = 255
            self.barra_vida.fill((R,G,0))
            


    def tiro(self):
        # ATIRA QUANDO O CONTADOR CHEGA A 0
        if  self.temp_tiro == 0:
            self.temp_tiro = self.timer # RESETA O CONTADOR

            #MUDA O TIPO DE PROJETIL DE ACORDO COM O ESTÁGIO DO CHEFE
            if self.fase1:
                if random.randint(0,100) < 10:
                    projetil = Ivermectina(self.rect.center)
                else:
                    projetil = Cloroquina(self.rect.center)

            else:
                if random.randint(0,100) < 30:
                    projetil = Ivermectina(self.rect.center)
                else:
                    projetil = Hidroxicloroquina(self.rect.center)  
            return projetil
        return None


