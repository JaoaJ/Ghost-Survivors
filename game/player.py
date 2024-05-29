import pygame


class Personagem:
    def __init__(self,x,y):
        self.sprite = pygame.image.load("assets/player_sprite.png")
        self.sprite = pygame.transform.scale(self.sprite, (55, 45))
        self.tamanho = self.sprite.get_width()
        self.personagem_sprite_direita = self.sprite
        self.personagem_sprite_esquerda = pygame.transform.flip(self.sprite, True, False)
        self.x_centro = x // 2
        self.y_centro = y // 2
        self.personagem_x = self.x_centro - self.tamanho // 2
        self.personagem_y = self.y_centro - self.tamanho // 2    
