import pygame, game_module as gm

class Block(pygame.sprite.Sprite):
    
    def __init__(self, image, position_x, position_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y
        