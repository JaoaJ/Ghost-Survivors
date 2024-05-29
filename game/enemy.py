import pygame
import math
import random


class Inimigo:
    def __init__(self, x, y, velocidade, cor):
        self.velocidade = velocidade
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.dist = 0
        
        sprites = {"verde" : "assets/inimigo_sprite_green.png",
                   "azul" : "assets/inimigo_sprite_blue.png",
                  "vermelho" : "assets/inimigo_sprite_red.png"}

        self.cor = cor
        self.sprite = pygame.image.load(sprites[cor])
        self.sprite = pygame.transform.scale(self.sprite, (50, 48))
        self.largura = self.sprite.get_width()
        self.altura = self.sprite.get_height()

        self.personagem_sprite_esquerda = self.sprite
        self.personagem_sprite_direita =  pygame.transform.flip(self.sprite, True, False)

        
    def virar(self, direcao):
        if direcao == "direita":
            return self.personagem_sprite_direita
        elif direcao == "esquerda":
            return self.personagem_sprite_esquerda
        
    
    def perseguir_jogador(self, jogador):
        dx = jogador.personagem_x - self.x
        dy = jogador.personagem_y - self.y
        self.dist = math.hypot(dx, dy)
        if self.dist > 0:
            direcao_x = dx / self.dist
            direcao_y = dy / self.dist
            self.x += direcao_x * self.velocidade
            self.y += direcao_y * self.velocidade
