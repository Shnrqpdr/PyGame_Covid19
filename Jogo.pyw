import pygame as pg
import sys, random, time, math
from Fases.fase import *
from Personagens.jogador import *
from pygame.locals import *


# DEFININDO CONSTANTES DO JOGO
TELA_LARGURA = 1000
TELA_ALTURA = 600
FPS = 60

# DEFININDO A LISTA COM AS MUSICAS DAS FASES
musicas = ["Audio/title.mp3","Audio/fase1.mp3",
            "Audio/fase2.mp3","Audio/fase3.mp3",
            "Audio/fase4.mp3","Audio/fase5.mp3"]

# DEFININDO TUPLAS DAS CORES
PRETO = (0,0,0)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)

# INICIALIZANDO O PYGAME
pg.init()

# FUNCAO PARA PARAR TODOS OS SOMS DO JOGO
def som_stop():
    pg.mixer.stop()
    pg.mixer.music.stop()

# FUNCA PARA EXECUTAR  A MUSICA DAS FASES
def som_play(fase): 
    pg.mixer.music.load(fase)
    pg.mixer.music.set_volume(1)
    pg.mixer.music.play(loops=-1)

# DEFININDO FONTES PARA OS TEXTOS DO JOGO
fonte="Arial"
fonte_pequena = pg.font.SysFont(fonte,20)
fonte_media = pg.font.SysFont(fonte,30)
fonte_grande = pg.font.SysFont(fonte,40)

# CRIANDO A TELA DO JOGO
tela = pg.display.set_mode((TELA_LARGURA,TELA_ALTURA))
tela_inicio=pg.image.load("Telas/inicio.png").convert()
tela.blit(tela_inicio,(0,0))
pg.display.flip()

#CARREGANDO OS AUDIOS PRINCIPAIS
som_play(musicas[0])
proxima=pg.mixer.Sound("Audio/next.wav")
proxima.set_volume(0.3)

# VARIAVEL DE CONTROLE DA TELA DE INICIO
inicio = True

# TELA INICIAL
while inicio:

    for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    pg.quit()
                    sys.exit()
        
        # VERIFICACAO DAS TELAS ACIONADAS
                if evento.type == KEYDOWN:

                    # SAI DO JOGO AO APERTAR ESC    
                    if evento.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()

            # INICIA O JOGO AO APERTAR ENTER   
                    if evento.key == K_RETURN:
                        tela_inicio=pg.image.load("Telas/inicio2.png").convert()
                        tela.blit(tela_inicio,(0,0))
                        pg.display.flip()
                        pg.mixer.music.fadeout(2000)
                        time.sleep(2)
                        inicio = False
    

# INSTANCIANDO O JOGADOR
jogador=Jogador(TELA_LARGURA,TELA_ALTURA)

#CARREGANDO A TELA DE VITORIA
vitoria=pg.image.load("Telas/vitoria.png").convert()

#CRIANO A LISTA COM AS FASES
fases=[Fase5(TELA_LARGURA,TELA_ALTURA),Fase1(TELA_LARGURA,TELA_ALTURA),
       Fase2(TELA_LARGURA,TELA_ALTURA),Fase3(TELA_LARGURA,TELA_ALTURA),
       Fase4(TELA_LARGURA,TELA_ALTURA)]


# LOOP ONDE ACONTECEM AS 4 PRIMEIRAS FASES, COMECANDO PELA FASE 1
fase=1
while jogador and fase < 5: # LOOP OCORRE ATE A 4a FASE E SE O OBJETO JOGADOR AINDA EXISTIR
    som_play(musicas[fase])
    jogador = fases[fase].play(jogador,tela,FPS) #INICIA FASE
    som_stop()
    if jogador: # SE O OBJETO JOGADOR VOLTOU DA FASE DIFERENTE DE 'NONE', I.E., NAO MORREU, ELE PROSSEGUE PARA A PROXIMA FASE
        
        if fase < 4:
            proxima.play()
            tela.blit(vitoria,(0,0))
            pg.display.flip()
            time.sleep(3)
        fase+=1
    else: 
        break  # SE O OBJETO JOGADOR VOLTAR DA FASE COMO 'NONE' O LOOP E QUEBRADO

fase=0
# APOS SAIR DO LOOP A PROXIMA FASE A SER JOGADA E A DA POSICAO 0 DA LISTA, 
# A FASE DO CHEFE, MAS APENAS SE O OBJETO  JOGADOR NAO FOR 'NONE'

if jogador:
    som_stop()
    proxima.play()
    vitoria=pg.image.load("Telas/vitoria2.png").convert()
    tela.blit(vitoria,(0,0))
    pg.display.flip()
    pg.time.wait(3000)
    pg.mixer.music.load("Audio/chefe.mp3")
    pg.mixer.music.play(loops=-1)
    vitoria=pg.image.load("Telas/chefe.png").convert()
    tela.blit(vitoria,(0,0))
    pg.display.flip()
    pg.time.wait(5000)
    jogador = fases[fase].play(jogador,tela,FPS)
    if jogador:  #VERIFICA SE O JOGADOR VOLTOU "VIVO" DA FASE, I.E, ELE NAO E 'NONE', E A TELA DE VITORIA E EXIBIDA
        som_stop()
        pg.mixer.music.load("Audio/win.mp3")
        pg.mixer.music.play(loops=-1)
        vitoria=pg.image.load("Telas/fim.png").convert()
        tela.blit(vitoria,(0,0))
        pg.display.flip()
        while True:
    
            for evento in pg.event.get():

        # SAIR DO JOGO CASO A TELA SEJA FECHADA
                if evento.type == QUIT:
                    vitoria=pg.image.load("Telas/lula.png").convert()
                    tela.blit(vitoria,(0,0))
                    pg.display.flip()
                    pg.time.wait(400)
                    pg.quit()
                    sys.exit()
        

# SE O OBJETO JOGADOR SE TORNOU 'NONE' EM ALGUM MOMENTO O BLOCO DE GAMEOVER E EXECUTADO
if not jogador:
    som_stop()
    died = pg.mixer.Sound("Audio/died.wav")
    died.play()
    time.sleep(3)
    gameover=pg.image.load("Telas/gameover.png").convert()
    tela.blit(gameover,(0,0))
    pg.display.flip()
    som_play("Audio/gameover.mp3")

    time.sleep(8)

# TODOS OS AUDIOS SAO ENCERRADOS E O JOGO E FECHADO
som_stop()
pg.quit()
sys.exit()











