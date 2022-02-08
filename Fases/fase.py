import pygame as pg
import sys, random, time, math
from Personagens.jogador import Jogador
from Personagens.inimigos import *
from Projeteis.projeteis import *
from Poderes.poderes import *
from pygame.locals import *

# DEFININDO TUPLAS DAS CORES
PRETO = (0,0,0)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)

# CARREGANDO OS EFEITOS SONOROS UTILIZADOS NAS FASES
pg.mixer.init()
hit = pg.mixer.Sound("Audio/hit.wav")
hit.set_volume(0.2)
shot = pg.mixer.Sound("Audio/shot.wav")
shot.set_volume(0.2)
kill = pg.mixer.Sound("Audio/kill.wav")
kill.set_volume(0.2)
power = pg.mixer.Sound("Audio/power.wav")
power.set_volume(0.2)
health = pg.mixer.Sound("Audio/health.wav")
health.set_volume(0.2)
shothit = pg.mixer.Sound("Audio/shothit.wav")
shothit.set_volume(0.2)
bullethit = pg.mixer.Sound("Audio/bullethit.wav")
bullethit.set_volume(0.2)


# CLASSE PRINCIPAL DAS FASES
class Fases(object):
    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        self.largura = TELA_LARGURA
        self.altura = TELA_ALTURA
        self.fonte="Serif"
        self.fonte_pequena = pg.font.SysFont(self.fonte,20)
        self.fonte_media = pg.font.SysFont(self.fonte,30)
        self.fonte_grande = pg.font.SysFont(self.fonte,60)
        

    def colisao_jogador(self,jogador,inimigos):
            # VERIFICA COLISAO DOS INIMIGOS COM O JOGADOR

            inimigo_colidiu = pg.sprite.spritecollideany(jogador,inimigos)
            if inimigo_colidiu:
                hit.play()
                jogador.vida -= inimigo_colidiu.dano
                inimigo_colidiu.kill()
                if jogador.vida <= 0:
                    jogador.vida = 0
                    return True
                

            return False

    def colisao_projetil(self,projeteis,inimigos,jogador):
        # VERIFICA SE OS INIMIGOS FORAM ACERTADOS PELAS VACINAS
            for tiro in projeteis:
                inimigo_acertado = pg.sprite.spritecollideany(tiro,inimigos)
                if inimigo_acertado:
                    shothit.play()
                    inimigo_acertado.vida -= tiro.dano*jogador.poder
                    if inimigo_acertado.vida <= 0:
                        kill.play()
                        jogador.pontos += inimigo_acertado.pontos
                        inimigo_acertado.kill()
                        
                    tiro.kill()

    def colisao_poderes (self,jogador,poderes):
        # VERIFICA SE O JOGADOR PEGOU ALGUM DOS PODERES
            poder_acertado = pg.sprite.spritecollideany(jogador,poderes)
            if poder_acertado:
                if poder_acertado.tipo == "VIDA":
                    health.play()
                    jogador.vida += poder_acertado.vida
                    if jogador.vida > jogador.vidaMAX:
                        jogador.vida = jogador.vidaMAX

                if poder_acertado.tipo == "DOSE":
                    power.play()
                    jogador.dose += poder_acertado.dose
                    if jogador.dose > jogador.doseMAX:
                        jogador.dose = jogador.doseMAX
                poder_acertado.kill()

    def atualiza_sprites(self,tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes):
        # ATUALIZA A POSICAO DOS SPRITES
        jogador.update(teclas,self.largura,self.altura)
        inimigos.update()
        projeteis.update(self.largura)
        poderes.update()
        
        #COLOCA OS SPRITES NA TELA
        tela.blit(self.surf,self.rect)
        for sprite in todos_sprites:
            tela.blit(sprite.surf,sprite.rect)
        pontos= self.fonte_grande.render('Pontos: '+str(jogador.pontos), True, BRANCO)
        pontos_rect = pontos.get_rect(center =(self.largura/2,30))
        
        tela.blit(jogador.barras,(0,0))
        tela.blit(jogador.barra_vida,(30,10))
        tela.blit(jogador.barra_dose,(30,50))
        tela.blit(pontos,pontos_rect)
        



    def cria_grupos(self,jogador):
        #CRIA OS GRUPOS DE SPRITES
        todos_sprites = pg.sprite.Group()
        inimigos = pg.sprite.Group()
        projeteis = pg.sprite.Group()
        poderes = pg.sprite.Group()
        todos_sprites.add(jogador)
        return todos_sprites,inimigos,projeteis,poderes


class Teclas(object):
    #CLASSE QUE SERA USADA COMO DICIONARIO PARA VERIFICAR OS TECLAS PRESSIONADAS

    def tecla32(tela,jogador,inimigos,projeteis,poderes,todos_sprites): # BARRA DE ESPACO (K_SPACE = 32)
        if jogador.dose >= Vacina.custo:
            shot.play()
            tiro = Vacina(jogador.rect.center)
            projeteis.add(tiro)
            todos_sprites.add(tiro)
            jogador.dose -= Vacina.custo

    def tecla27(tela,jogador,inimigos,projeteis,poderes,todos_sprites): # ESC (K_ESCAPE = 27)
        pg.mixer.pause()
        pg.mixer.music.pause()
        pausa = pg.image.load("Fases/pausa.png").convert()
        pausa.set_colorkey((0,0,0),RLEACCEL)
        pausa_rect = pausa.get_rect(center=tela.get_rect().center)
        tela.blit(pausa,pausa_rect)
        pg.display.flip()

        while True:
            for evento in pg.event.get():
                if evento.type == KEYDOWN:
                    if evento.key == K_ESCAPE:
                        pg.mixer.unpause()
                        pg.mixer.music.unpause()
                        return
                if evento.type == QUIT:
                    pg.quit()
                    sys.exit()

    def tecla120(tela,jogador,inimigos,projeteis,poderes,todos_sprites): # X (K_x = 120)
        jogador.vida += 30
        if jogador.vida > jogador.vidaMAX:
            jogador.vida = jogador.vidaMAX

    def tecla122(tela,jogador,inimigos,projeteis,poderes,todos_sprites): # Z (K_z = 122)
        jogador.dose += 50
        if jogador.dose > jogador.doseMAX:
            jogador.dose = jogador.doseMAX

    def tecla99(tela,jogador,inimigos,projeteis,poderes,todos_sprites): # C (K_c = 99)
        jogador.pontos+=10


    




class Fase1(Fases):  
    #PRIMEIRA FASE

    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__(TELA_LARGURA,TELA_ALTURA)
        
        self.surf = pg.image.load("Fases/fase1bg.png").convert()
        self.rect = self.surf.get_rect()
        self.pontos = 10
        
        
    #EXECUTA A FASE
    def play(self,jogador,tela,FPS):
     

# CRIANDO OS GRUPOS DE SPRITES
        todos_sprites,inimigos,projeteis,poderes = self.cria_grupos(jogador)
        

# EVENTO PARA CRIACAO DE NOVOS INIMIGOS

        NOVO_INIMIGO = pg.USEREVENT + 1
        pg.time.set_timer(NOVO_INIMIGO,900)

# EVENTO PARA A CRIACAO DE POWERUPS
        NOVO_PODER = pg.USEREVENT + 2
        pg.time.set_timer(NOVO_PODER,1000)

# VARIAVEL QUE MANTEM O JOGO RODANDO
        executando = True

# DEFININDO O RELOGIO PARA CONTROLE DE FRAMERATE
        relogio=pg.time.Clock()
#   CRIANDO O DICIONÁRIO DA CLASSE TECLAS
        teclas_pressionadas = Teclas.__dict__

        

# LOOP PRINCIPAL DO JOGO
        while executando:


    # TRATANDO OS EVENTOS DO JOGO
            for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    executando = False
                    break

        # VERIFICAÇÃO DAS TELAS ACIONADAS
                if evento.type == KEYDOWN:
                    try:
                        tecla_acionada = teclas_pressionadas["tecla"+str(evento.key)]
                    except KeyError:
                        tecla_acionada = None
                    if tecla_acionada:
                        tecla_acionada(tela,jogador,inimigos,projeteis,poderes,todos_sprites)
                        
        # ADICIONA NOVO INIMIGO
                if evento.type == NOVO_INIMIGO:
                    inimigo = Covid1(self.altura,self.largura)
                    inimigos.add(inimigo)
                    todos_sprites.add(inimigo)

         # ADICIONA NOVO PODER
                if evento.type == NOVO_PODER:
                    poder_prob = random.randint(0,100)
                    if poder_prob < 5:
                        poder = Vida(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)
                    elif poder_prob < 65:
                        poder = Dose(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)

                    

    # VERIFICA AS TECLAS APERTADAS PELO JOGADOR
            teclas=pg.key.get_pressed()

    # ATUALIZA A POSIÇÃO DOS SPRITES
            
            self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)

    # VERIFICA COLISAO ENTRE PROJETEIS E INIMIGOS
            self.colisao_projetil(projeteis,inimigos,jogador)

    # VERIFICA COLISAO ENTRE JOGADOR E PODERES
            self.colisao_poderes(jogador,poderes)

    # VERIFICA COLISÃO COM INIMIGOS
            if self.colisao_jogador(jogador,inimigos):
                self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
                pg.display.flip()
                return None  


    # ATUALIZA A TELA

            pg.display.flip()
    
    # CONTROLANDO O FPS

            relogio.tick(FPS)

    # VERIFICANDO SE O JOGADOR ATINGIU O NUMERO DE PONTOS
            if jogador.pontos >= self.pontos:
                for projetil in projeteis:
                    projetil.kill()
                for inimigo in inimigos:
                    inimigo.kill()
                for poder in poderes:
                    poder.kill()
                 
                return jogador


# SAINDO DO JOGO
        pg.quit()
        sys.exit()



class Fase2(Fases):  

    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__(TELA_LARGURA,TELA_ALTURA)
        self.surf = pg.image.load("Fases/fase2bg.png").convert()
        self.rect = self.surf.get_rect()
        
        self.pontos = 25
        
        
       
    def play(self,jogador,tela,FPS):
     

# CRIANDO OS GRUPOS DE SPRITES
        todos_sprites,inimigos,projeteis,poderes = self.cria_grupos(jogador)

# EVENTO PARA CRIAÇÃO DE NOVOS INIMIGOS

        NOVO_INIMIGO = pg.USEREVENT + 1
        pg.time.set_timer(NOVO_INIMIGO,800)

# EVENTO PARA A CRIAÇÃO DE POWERUPS
        NOVO_PODER = pg.USEREVENT + 2
        pg.time.set_timer(NOVO_PODER,1500)

# VARIÁVEL QUE MANTÉM O JOGO RODANDO
        executando = True

# DEFININDO O RELÓGIO PARA CONTROLE DE FRAMERATE
        relogio=pg.time.Clock()
        teclas_pressionadas = Teclas.__dict__
        

# LOOP PRINCIPAL DO JOGO
        while executando:


    # TRATANDO OS EVENTOS DO JOGO
            for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    executando = False

        # VERIFICAÇÃO DAS TELAS ACIONADAS
                if evento.type == KEYDOWN:
                    try:
                        tecla_acionada = teclas_pressionadas["tecla"+str(evento.key)]
                    except KeyError:
                        tecla_acionada = None
                    if tecla_acionada:
                        tecla_acionada(tela,jogador,inimigos,projeteis,poderes,todos_sprites)

        # ADICIONA NOVO INIMIGO
                if evento.type == NOVO_INIMIGO:
                    inimigo_prob = random.randint(0,100)
                    if inimigo_prob < 30:
                        inimigo = Covid2(self.altura,self.largura)
                    else:
                        inimigo = Covid1(self.altura,self.largura)
                    inimigos.add(inimigo)
                    todos_sprites.add(inimigo)

        # ADICIONA NOVO PODER
                if evento.type == NOVO_PODER:
                    poder_prob = random.randint(0,100)
                    if poder_prob < 5:
                        poder = Vida(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)
                    elif poder_prob < 65:
                        poder = Dose(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)

    # VERIFICA AS TECLAS APERTADAS PELO JOGADOR
            teclas=pg.key.get_pressed()


    # VERIFICA COLISAO ENTRE PROJETEIS E INIMIGOS
            self.colisao_projetil(projeteis,inimigos,jogador)

    # VERIFICA COLISAO ENTRE JOGADOR E PODERES
            self.colisao_poderes(jogador,poderes)

    # VERIFICA COLISÃO COM INIMIGOS
            if self.colisao_jogador(jogador,inimigos):
                self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
                pg.display.flip()
                return None     

    # ATUALIZA A POSIÇÃO DOS SPRITES
            self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)



    # ATUALIZA A TELA

            pg.display.flip()
    
    # CONTROLANDO O FPS

            relogio.tick(FPS)

    # VERIFICANDO SE O JOGADOR ATINGIU O NUMERO DE PONTOS
            if jogador.pontos >= self.pontos:
                for projetil in projeteis:
                    projetil.kill()
                for inimigo in inimigos:
                    inimigo.kill()
                return jogador


# SAINDO DO JOGO
        pg.quit()
        sys.exit()


class Fase3(Fases):  

    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__(TELA_LARGURA,TELA_ALTURA)
        self.surf = pg.image.load("Fases/fase3bg.png").convert()
        self.rect = self.surf.get_rect()
        self.pontos = 45
        
        
       
    def play(self,jogador,tela,FPS):
     

# CRIANDO OS GRUPOS DE SPRITES
        todos_sprites,inimigos,projeteis,poderes = self.cria_grupos(jogador)

# EVENTO PARA CRIAÇÃO DE NOVOS INIMIGOS

        NOVO_INIMIGO = pg.USEREVENT + 1
        pg.time.set_timer(NOVO_INIMIGO,600)

# EVENTO PARA A CRIAÇÃO DE POWERUPS
        NOVO_PODER = pg.USEREVENT + 2
        pg.time.set_timer(NOVO_PODER,1500)

# VARIÁVEL QUE MANTÉM O JOGO RODANDO
        executando = True

# DEFININDO O RELÓGIO PARA CONTROLE DE FRAMERATE
        relogio=pg.time.Clock()
        teclas_pressionadas = Teclas.__dict__
        

# LOOP PRINCIPAL DO JOGO
        while executando:


    # TRATANDO OS EVENTOS DO JOGO
            for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    executando = False

        # VERIFICAÇÃO DAS TELAS ACIONADAS
                if evento.type == KEYDOWN:
                    try:
                        tecla_acionada = teclas_pressionadas["tecla"+str(evento.key)]
                    except KeyError:
                        tecla_acionada = None
                    if tecla_acionada:
                        tecla_acionada(tela,jogador,inimigos,projeteis,poderes,todos_sprites)

        # ADICIONA NOVO INIMIGO
                if evento.type == NOVO_INIMIGO:
                    inimigo_prob = random.randint(0,100)
                    if inimigo_prob < 20:
                        inimigo = Covid3(self.altura,self.largura)
                    elif inimigo_prob < 70:
                        inimigo = Covid2(self.altura,self.largura)
                    else:
                        inimigo = Covid1(self.altura,self.largura)
                    inimigos.add(inimigo)
                    todos_sprites.add(inimigo)

        # ADICIONA NOVO PODER
                if evento.type == NOVO_PODER:
                    poder_prob = random.randint(0,100)
                    if poder_prob < 5:
                        poder = Vida(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)
                    elif poder_prob < 65:
                        poder = Dose(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)

    # VERIFICA AS TECLAS APERTADAS PELO JOGADOR
            teclas=pg.key.get_pressed()

    # VERIFICA COLISAO ENTRE PROJETEIS E INIMIGOS
            self.colisao_projetil(projeteis,inimigos,jogador)

    # VERIFICA COLISAO ENTRE JOGADOR E PODERES
            self.colisao_poderes(jogador,poderes)

    # VERIFICA COLISÃO COM INIMIGOS
            if self.colisao_jogador(jogador,inimigos):
                self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
                pg.display.flip()
                return None  
        

     # ATUALIZA A POSIÇÃO DOS SPRITES
            self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
            



    # ATUALIZA A TELA

            pg.display.flip()
    
    # CONTROLANDO O FPS

            relogio.tick(FPS)

    # VERIFICANDO SE O JOGADOR ATINGIU O NUMERO DE PONTOS
            if jogador.pontos >= self.pontos:
                for projetil in projeteis:
                    projetil.kill()
                for inimigo in inimigos:
                    inimigo.kill()
                return jogador


# SAINDO DO JOGO
        pg.quit()
        sys.exit()


class Fase4(Fases):  

    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__(TELA_LARGURA,TELA_ALTURA)

        self.surf = pg.image.load("Fases/fase4bg.png").convert()
        self.rect = self.surf.get_rect()
        self.pontos = 70 
       
    def play(self,jogador,tela,FPS):
     

# CRIANDO OS GRUPOS DE SPRITES
        todos_sprites,inimigos,projeteis,poderes = self.cria_grupos(jogador)

# EVENTO PARA CRIAÇÃO DE NOVOS INIMIGOS

        NOVO_INIMIGO = pg.USEREVENT + 1
        pg.time.set_timer(NOVO_INIMIGO,400)

# EVENTO PARA A CRIAÇÃO DE POWERUPS
        NOVO_PODER = pg.USEREVENT + 2
        pg.time.set_timer(NOVO_PODER,2000)

# VARIÁVEL QUE MANTÉM O JOGO RODANDO
        executando = True

# DEFININDO O RELÓGIO PARA CONTROLE DE FRAMERATE
        relogio=pg.time.Clock()
        teclas_pressionadas = Teclas.__dict__
      

# LOOP PRINCIPAL DO JOGO
        while executando:


    # TRATANDO OS EVENTOS DO JOGO
            for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    executando = False

        # VERIFICAÇÃO DAS TELAS ACIONADAS
                if evento.type == KEYDOWN:
                    try:
                        tecla_acionada = teclas_pressionadas["tecla"+str(evento.key)]
                    except KeyError:
                        tecla_acionada = None
                    if tecla_acionada:
                        tecla_acionada(tela,jogador,inimigos,projeteis,poderes,todos_sprites)

        # ADICIONA NOVO INIMIGO
                if evento.type == NOVO_INIMIGO:
                    inimigo_prob = random.randint(0,100)
                    if inimigo_prob < 10:
                        inimigo = Covid4(self.altura,self.largura)
                    elif inimigo_prob < 40:
                        inimigo = Covid3(self.altura,self.largura)
                    elif inimigo_prob < 75:
                        inimigo = Covid2(self.altura,self.largura)
                    else:
                        inimigo = Covid1(self.altura,self.largura)
                    inimigos.add(inimigo)
                    todos_sprites.add(inimigo)


        # ADICIONA NOVO PODER
                if evento.type == NOVO_PODER:
                    poder_prob = random.randint(0,100)
                    if poder_prob < 5:
                        poder = Vida(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)
                    elif poder_prob < 65:
                        poder = Dose(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)

    # VERIFICA AS TECLAS APERTADAS PELO JOGADOR
            teclas=pg.key.get_pressed()


    # VERIFICA COLISAO ENTRE PROJETEIS E INIMIGOS
            self.colisao_projetil(projeteis,inimigos,jogador)

    # VERIFICA COLISAO ENTRE JOGADOR E PODERES
            self.colisao_poderes(jogador,poderes)

    # VERIFICA COLISÃO COM INIMIGOS
            if self.colisao_jogador(jogador,inimigos):
                self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
                pg.display.flip()
                return None  

     # ATUALIZA A POSIÇÃO DOS SPRITES
            self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
            
    # ATUALIZA A TELA
            pg.display.flip()
    
    # CONTROLANDO O FPS
            relogio.tick(FPS)

    # VERIFICANDO SE O JOGADOR ATINGIU O NUMERO DE PONTOS
            if jogador.pontos >= self.pontos:
                for projetil in projeteis:
                    projetil.kill()
                for inimigo in inimigos:
                    inimigo.kill()
                return jogador
            
            

# SAINDO DO JOGO
        pg.quit()
        sys.exit()


class Fase5(Fases):  

    def __init__(self,TELA_LARGURA,TELA_ALTURA):
        super().__init__(TELA_LARGURA,TELA_ALTURA)
        self.surf = pg.image.load("Fases/fase5bg.png").convert()
        self.rect = self.surf.get_rect()
        self.pontos = 100
        
        
       
    def play(self,jogador,tela,FPS):
     

# CRIANDO OS GRUPOS DE SPRITES
        todos_sprites,inimigos,projeteis,poderes = self.cria_grupos(jogador)

# CRIANDO O CHEFE
        chefe=Chefe(self.altura,self.largura)
        inimigos.add(chefe)
        projeteis_inimigo=pg.sprite.Group()
        todos_sprites.add(chefe)

# EVENTO PARA A CRIAÇÃO DE POWERUPS
        NOVO_PODER = pg.USEREVENT + 2
        pg.time.set_timer(NOVO_PODER,1850)

# VARIÁVEL QUE MANTÉM O JOGO RODANDO
        executando = True

# DEFININDO O RELÓGIO PARA CONTROLE DE FRAMERATE
        relogio=pg.time.Clock()
        teclas_pressionadas = Teclas.__dict__
      

# LOOP PRINCIPAL DO JOGO
        while executando:


    # TRATANDO OS EVENTOS DO JOGO
            for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    executando = False

        # VERIFICAÇÃO DAS TELAS ACIONADAS
                if evento.type == KEYDOWN:
                    try:
                        tecla_acionada = teclas_pressionadas["tecla"+str(evento.key)]
                    except KeyError:
                        tecla_acionada = None
                    if tecla_acionada:
                        tecla_acionada(tela,jogador,inimigos,projeteis,poderes,todos_sprites)


        # ADICIONA NOVO PODER
                if evento.type == NOVO_PODER:
                    poder_prob = random.randint(0,100)
                    if poder_prob < 5:
                        poder = Vida(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)
                    elif poder_prob < 75:
                        poder = Dose(self.largura,self.altura)
                        todos_sprites.add(poder)
                        poderes.add(poder)

    # VERIFICA AS TECLAS APERTADAS PELO JOGADOR
            teclas=pg.key.get_pressed()

    # VERIFICA SE INIMIGO ATIROU
            tiro_inimigo = chefe.tiro()
            if tiro_inimigo:
                todos_sprites.add(tiro_inimigo)
                projeteis_inimigo.add(tiro_inimigo)


    # VERIFICA COLISAO ENTRE PROJETEIS E INIMIGOS
            self.colisao_projetil(projeteis,inimigos,jogador)

    # VERIFICA COLISAO ENTRE JOGADOR E PODERES
            self.colisao_poderes(jogador,poderes) 

     # ATUALIZA A POSIÇÃO DOS SPRITES
            self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
            projeteis_inimigo.update(jogador)
            tela.blit(chefe.barra_vida,(120,self.altura-50))

    # VERIFICA COLISÃO DOS TIROS DO CHEFE COM O JOGADOR
            tiro_acertado = pg.sprite.spritecollideany(jogador,projeteis_inimigo)
            if tiro_acertado:
                hit.play()
                jogador.vida -= tiro_acertado.dano
                tiro_acertado.kill()
         

    # VERIFICA COLISÃO DOS TIROS DO CHEFE COM OS DO JOGADOR

            for tiro in projeteis:
                tiro_acertado = pg.sprite.spritecollideany(tiro,projeteis_inimigo)
                if tiro_acertado:
                    bullethit.play()
                    tiro_acertado.kill()
                    tiro.kill()

    # VERIFICA COLISÃO DO CHEFE COM O JOGADOR

            if  pg.sprite.collide_rect(jogador,chefe):
                return None 



    # VERIFICA SE O JOGADOR MORREU
            if jogador.vida <= 0:
                jogador.vida = 0
                self.atualiza_sprites(tela,todos_sprites,jogador,teclas,inimigos,projeteis,poderes)
                pg.display.flip()
                return None

    # VERIFICA SE O CHEFE MORREU
            if chefe.vida <= 0:
                return jogador

    # ATUALIZA A TELA

            pg.display.flip()
    
    # CONTROLANDO O FPS

            relogio.tick(FPS)
          


# SAINDO DO JOGO
        pg.quit()
        sys.exit()
