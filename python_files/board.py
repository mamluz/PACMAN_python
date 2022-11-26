import game_module as gm
from block import Block
import pygame
from random import randrange

screen = gm.screen


class Board:
    def __init__(self, table):
        self.table = table
        self.list_of_blocks = []
        self.list_of_points = pygame.sprite.Group()
        self.list_of_transform_blocks = pygame.sprite.Group()

    def create(self):
        # plansza do tego ma 720x720 blocki 20x20 !
        # generowanie labiryntu:

        for i in range(0, 36):
            for j in range(0, 36):
                if self.table[i][j] == 1:
                    #"3way blocki"
                    if self.table[i+1][j] == 1 and self.table[i][j-1] == 1 and self.table[i][j+1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[9], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                    elif self.table[i-1][j] == 1 and self.table[i][j-1] == 1 and self.table[i][j+1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[11], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                    elif self.table[i+1][j] == 1 and self.table[i-1][j] == 1 and self.table[i][j+1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[8], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                    elif self.table[i+1][j] == 1 and self.table[i-1][j] == 1 and self.table[i][j-1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[10], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                        # "rury"
                    elif self.table[i-1][j] == 1 and self.table[i+1][j] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[5], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                    elif self.table[i][j-1] == 1 and self.table[i][j+1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[4], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                        # zamkniecia wertykalne:
                    elif self.table[i-1][j] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[1], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                    elif self.table[i+1][j] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[3], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                        # zamkniecia horyzontalne:
                    elif self.table[i][j-1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[0], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                    elif self.table[i][j+1] == 1:
                        current_block = Block(
                            gm.BLOCK_LIST[2], 40 + j * 20, 40 + i * 20)
                        self.list_of_blocks.append(current_block)
                # rysowanie blokow ramki
                elif self.table[i][j] == 2:
                    current_block = Block(
                        gm.BLOCK_LIST[12], 40 + j * 20, 40 + i * 20)
                    self.list_of_blocks.append(current_block)
                # rysowanie blokow w punktami
                elif self.table[i][j] == 0:
                    current_block = Block(
                        gm.BLOCK_LIST[13], 40 + j * 20, 40 + i * 20)
                    self.list_of_points.add(current_block)



        # rozmieszczanie blokow dezaktywacji przeciwnikow:
        for i in range(0, 10):
            # losowe rozmieszczanie blokow dezaktywacji (transform blockow) tam gdzie bloki z punktami
            current_random_point_block = self.list_of_points.sprites()[randrange(0, len(self.list_of_points))]
            tr_block = Block(
                gm.BLOCK_LIST[7], current_random_point_block.rect.x, current_random_point_block.rect.y)
            tr_block.rect.center = current_random_point_block.rect.center
            self.list_of_transform_blocks.add(tr_block)
            current_random_point_block.kill()

    def draw(self):
        for el in self.list_of_blocks:
            screen.blit(el.image, el.rect)

        for point in self.list_of_points:
            screen.blit(point.image, point.rect)
            
        for tr in self.list_of_transform_blocks:
            screen.blit(tr.image, tr.rect)
