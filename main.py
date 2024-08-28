import pygame
from game import player
from game import enemy
from game import weapon
import time
import random


# Inicialização do Pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 55


# Configurações da janela
x = 1000
y = 600
tela = pygame.display.set_mode((x, y))
pygame.display.set_caption("Minha Janela Pygame")
efeito_cinza = pygame.Surface((x, y), pygame.SRCALPHA)
efeito_cinza.fill((60,60,60, 100))


# Criando personagem
jogador = player.Personagem(x,y)
personagem = jogador.personagem_sprite_direita

# criando vidas personagem
vidas = [0, 0, 0]
coracao_sprite = "assets/vida.png"
coracao = pygame.image.load(coracao_sprite)
coracao = pygame.transform.scale(coracao, (70, 60))

dano = pygame.Surface((x, y), pygame.SRCALPHA)
dano.fill((255, 0, 0, 100))
tempo_dano = 0

# Criando lista de inimigos
inimigos = [enemy.Inimigo(200, 200, velocidade=2, cor="verde")]


# Criando arma
arma = weapon.Arma()


# Fundo da tela
fundo_imagem = pygame.image.load("assets/fundo.png")
fundo_imagem = pygame.transform.scale(fundo_imagem, (x, y))


# Inicializando posição do fundo
fundo_x = 0
fundo_y = 0


# inicia contador de kill
kills = 0.0


# Distancia minima para novos inimigos

distancia_minima = 515
distancia_maxima = 600


def gerar_posicao_inimigo():
    while True:
        local_x = x
        local_y = y
        local_x_n = -x
        local_y_n = -y

        x_i, y_i = random.randint(local_x_n, local_x), random.randint(local_y_n, local_y)
        distancia = ((x_i - jogador.personagem_x) ** 2 + (y_i - jogador.personagem_y) ** 2) ** 0.5
        if distancia >= distancia_minima and distancia <= distancia_maxima:
            return x_i, y_i

def adicionar_inimigo():
    global kills
    if kills < 50:
        kills += 1
        for _ in range(int(kills) + 1 - len(inimigos)):
            x_i, y_i = gerar_posicao_inimigo()
            novo_inimigo = enemy.Inimigo(x_i, y_i, velocidade=2, cor="verde")
            inimigos.append(novo_inimigo)

    elif kills < 100:
        kills += 0.25
        x_i, y_i = gerar_posicao_inimigo()
        novo_inimigo = enemy.Inimigo(x_i, y_i, velocidade=2.5, cor="azul")
        inimigos.append(novo_inimigo)

    else:
        kills += 0.25
        x_i, y_i = gerar_posicao_inimigo()
        novo_inimigo = enemy.Inimigo(x_i, y_i, velocidade=3, cor="vermelho")
        inimigos.append(novo_inimigo)

    if kills >= 50 and not arma.segundo_orb_ativo:
        # nova arma
        arma.ativar_segundo_orb()

def adicionar_inimigo_sem_kill():
    if kills < 50:
        for _ in range(int(kills) + 1 - len(inimigos)):
            x_i, y_i = gerar_posicao_inimigo()
            novo_inimigo = enemy.Inimigo(x_i, y_i, velocidade=2, cor="verde")
            inimigos.append(novo_inimigo)

    elif kills < 100:
        x_i, y_i = gerar_posicao_inimigo()
        novo_inimigo = enemy.Inimigo(x_i, y_i, velocidade=2.5, cor="azul")
        inimigos.append(novo_inimigo)

    else:
        x_i, y_i = gerar_posicao_inimigo()
        novo_inimigo = enemy.Inimigo(x_i, y_i, velocidade=3, cor="vermelho")
        inimigos.append(novo_inimigo)


def checar_colisao_inimigos(inimigo1, inimigo2):
    # Calcula a distância entre os dois inimigos
    distancia = ((inimigo1.x - inimigo2.x) ** 2 + (inimigo1.y - inimigo2.y) ** 2) ** 0.5

    # Se a distância for menor que a soma das metades das larguras ou alturas dos inimigos, há uma colisão
    if distancia < (inimigo1.largura // 2 + inimigo2.largura // 2):
        return True
    return False

def tratar_colisao_inimigos(inimigo1, inimigo2):
    # Faz os inimigos se afastarem em direções opostas
    dx = inimigo1.x - inimigo2.x
    dy = inimigo1.y - inimigo2.y
    distancia = ((dx ** 2) + (dy ** 2)) ** 0.6

    if distancia == 0:  # Evitar divisão por zero
        distancia = 1

    # Ajusta a posição dos inimigos para que se afastem
    deslocamento = 5  # Quanto mais os inimigos se afastam em cada colisão
    inimigo1.x += (dx / distancia) * deslocamento
    inimigo1.y += (dy / distancia) * deslocamento
    inimigo2.x -= (dx / distancia) * deslocamento
    inimigo2.y -= (dy / distancia) * deslocamento


rodando = True
# Loop principal
while rodando:
    # Outros códigos do loop...

    # Verifica colisão entre inimigos
    for i in range(len(inimigos)):
        for j in range(i + 1, len(inimigos)):
            if checar_colisao_inimigos(inimigos[i], inimigos[j]):
                tratar_colisao_inimigos(inimigos[i], inimigos[j])


    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_d]:
        # Atualiza a posição do fundo para a direita
        personagem = jogador.personagem_sprite_direita
        for inimigo in inimigos:
            inimigo.x -= 4

        fundo_x -= 4

        if abs(fundo_x) > fundo_imagem.get_width():
            fundo_x = 0
       
    if teclas[pygame.K_a]:
        # Atualiza a posição do fundo para a esquerda
        personagem = jogador.personagem_sprite_esquerda

        for inimigo in inimigos:
            inimigo.x += 4

        fundo_x += 4

        if abs(fundo_x) > fundo_imagem.get_width():
            fundo_x = 0
        
    if teclas[pygame.K_w]:
        # Atualiza a posição do fundo para cima
        for inimigo in inimigos:
            inimigo.y += 4

        fundo_y += 4

        if abs(fundo_y) > fundo_imagem.get_height():
            fundo_y = 0
        
    if teclas[pygame.K_s]:
        # Atualiza a posição do fundo para baixo
        for inimigo in inimigos:
            inimigo.y -= 4

        fundo_y -= 4

        if abs(fundo_y) > fundo_imagem.get_height():
            fundo_y = 0


    #adiciona um tile ao centro
    tela.blit(fundo_imagem, (fundo_x, fundo_y))

    #adiciona um tile a esquerda e a direita
    tela.blit(fundo_imagem, (fundo_x + x, fundo_y))
    tela.blit(fundo_imagem, (fundo_x - x, fundo_y))

    #adiciona um tile acima e abaixo
    tela.blit(fundo_imagem, (fundo_x , fundo_y + y))
    tela.blit(fundo_imagem, (fundo_x , fundo_y - y))
    
    # tile diagonais
    tela.blit(fundo_imagem, (fundo_x + x, fundo_y + y))
    tela.blit(fundo_imagem, (fundo_x - x, fundo_y - y))
    tela.blit(fundo_imagem, (fundo_x + x, fundo_y - y))
    tela.blit(fundo_imagem, (fundo_x - x, fundo_y + y))

   
    # desenha o personagem na tela    
    tela.blit(personagem, (jogador.personagem_x, jogador.personagem_y))
    

    # desenha o sprite do inimigo em direção ao personagem
    for inimigo in inimigos:
        # inimigo perseguir
        inimigo.perseguir_jogador(jogador)

        if inimigo.x > jogador.personagem_x:
            tela.blit(inimigo.virar("esquerda"), (inimigo.x, inimigo.y))  # type: ignore

        elif inimigo.x < jogador.personagem_x:
            tela.blit(inimigo.virar("direita"), (inimigo.x, inimigo.y))  # type: ignore


    # cria posições para arma
    orb_x, orb_y = arma.update_position(x, y)


    # desenha o orb/arma numero 1
    pygame.draw.circle(tela, (0,255,0),(orb_x, orb_y),arma.orbital_size)
    pygame.draw.circle(tela, (0,0,0),(orb_x, orb_y),arma.orbital_size, 3)


    # aplica efeito cinza na tela
    tela.blit(efeito_cinza, (0, 0))


    # desenha vidas/coracao
    count = 0
    for vida in vidas:
        tela.blit(coracao, (900 + count, 20))
        count += coracao.get_width() - 110

    
    # desenha o orb/arma numero 2 se ativado
    if arma.segundo_orb_ativo:
            pygame.draw.circle(tela, (0, 0, 255), (arma.segundo_orb_x, arma.segundo_orb_y), arma.orbital_size)
            pygame.draw.circle(tela, (0, 0, 0), (arma.segundo_orb_x, arma.segundo_orb_y), arma.orbital_size, 3)


    # checa colisao da arma
    for inimigo in inimigos:

        if arma.checar_colisao(inimigo):
            inimigos.remove(inimigo)
            adicionar_inimigo()

            # Adiciona novos inimigos baseado na quantidade de kills
            

    # checa se inimigo saiu da tela e remove sem contar kill
    for inimigo in inimigos:
        if inimigo.x + 700 < -inimigo.largura or inimigo.x - 700 > x + inimigo.largura or inimigo.y + 700 < -inimigo.altura or inimigo.y - 700 > y + inimigo.altura:
            inimigos.remove(inimigo)
            adicionar_inimigo_sem_kill()



    # checa fim de jogo/colisao inimigo
    for inimigo in inimigos:
        if inimigo.dist > 0 and inimigo.dist < jogador.tamanho - 15:
            tempo_dano = 20
            del vidas[-1]
            inimigo.x, inimigo.y = gerar_posicao_inimigo()

        if tempo_dano > 0:
            tela.blit(dano, (0, 0))
            tempo_dano -=1

        if len(vidas) == 0:
            fonte_f = pygame.font.Font(None, 250)
            texto_fim_de_jogo = fonte_f.render("Game Over", True, (0, 0, 0))
            tela.blit(texto_fim_de_jogo, (20, (y // 2) - 250 // 2))
            rodando = False  # Termina o jogo


    # contador de kills na tela
    fonte = pygame.font.Font(None,80)
    texto_s = fonte.render("Points: "+str(int(kills)), True, (0,0,0))
    tela.blit(texto_s, (23, 25))


    #sombra contador
    texto = fonte.render("Points: " + str(int(kills)), True, (255,255,255))
    tela.blit(texto, (20, 20))

    #atualiza tela
    pygame.display.update()

# tela game over
fonte_f = pygame.font.Font(None, 250)
texto_fim_de_jogo = fonte_f.render("Game Over", True, (0, 0, 0))
tela.blit(texto_fim_de_jogo, (20, (y // 2) - 250 // 2))
time.sleep(4)

# Finaliza o Pygame
pygame.quit()
