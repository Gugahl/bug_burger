from pygame import *

init()

relogio = time.Clock()
fps = 60

# Tela do jogo
painel_botoes = 151
tela_largura = 1280
tela_altura = 569 + painel_botoes

tela = display.set_mode((tela_largura, tela_altura))
display.set_caption('Game')

# Carrega a imagem
# Usa como plano de fundo
fundo = image.load("imagem\imagem2.jpeg").convert_alpha()
painel = image.load("imagem\painel.png").convert_alpha()
fundo = transform.scale(fundo, (1280, 720 - painel_botoes))
painel = transform.scale(painel, (1280, painel_botoes))

# Função para desenhar o fundo
def desenha_fundo():
    tela.blit(fundo, (0, 0))
    
# Função para desenhar o painel
def desenha_painel():
    tela.blit(painel, (0, tela_altura - painel_botoes))

loop = True
while loop:
    
    desenha_fundo()
    desenha_painel()
    
    for events in event.get():
        if events.type == QUIT:
            loop = False
    tela.blit(fundo, (0, 0))
    rel_x = 1280 % fundo.get_rect().width
    tela.blit(fundo, (rel_x - fundo.get_rect().width, 0))
    
    if rel_x < 1200:
        tela.blit(fundo, (rel_x, 0))
    display.update()
