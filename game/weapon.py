import math
import pygame

class Arma:
    def __init__(self):
        self.orbital_raio = 100
        self.orbital_angulo = 0
        self.orbital_speed = 0.025
        self.orbital_size = 10
        self.kills = 0
        self.segundo_orb_ativo = False
        self.segundo_orb_angulo = self.orbital_angulo  + math.pi# Inicia o segundo orb na posição oposta

        # Inicializa a posição da segunda orb
        self.segundo_orb_x = 0
        self.segundo_orb_y = 0

    def update_position(self, x, y):
        self.x_centro = x // 2
        self.y_centro = y // 2
        self.orbital_angulo += self.orbital_speed

        # atualiza posição primeiro orb
        self.orb_x = self.x_centro + self.orbital_raio * math.cos(self.orbital_angulo)
        self.orb_y = self.y_centro + self.orbital_raio * math.sin(self.orbital_angulo)

        # atualiza posição segundo orb se ativo
        if self.segundo_orb_ativo:
            self.segundo_orb_angulo = self.orbital_angulo + math.pi
            self.segundo_orb_x = self.x_centro + self.orbital_raio * math.cos(self.segundo_orb_angulo)
            self.segundo_orb_y = self.y_centro + self.orbital_raio * math.sin(self.segundo_orb_angulo)

        return self.orb_x, self.orb_y

    def ativar_segundo_orb(self):
        self.segundo_orb_ativo = True

    def checar_colisao(self, inimigo):
        # verifica colisao primeiro orb
        self.orb_rect = pygame.Rect(self.orb_x - 5, self.orb_y - 5, 10, 10)
        self.inimigo_rect = pygame.Rect(inimigo.x, inimigo.y, inimigo.largura, inimigo.altura)
        if self.orb_rect.colliderect(self.inimigo_rect):
            return True

        # verifica colisao segundo orb se ativado
        if self.segundo_orb_ativo:
            self.segundo_orb_rect = pygame.Rect(self.segundo_orb_x, self.segundo_orb_y, 10, 10)
            if self.segundo_orb_rect.colliderect(self.inimigo_rect):
                return True

        return False
