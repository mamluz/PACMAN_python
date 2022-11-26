from random import random, randrange
import pygame, os, game_module as gm
from board import Board
from block import Block
from level_structures import level1_board
import time

pygame.mixer.init()
transform_sound = pygame.mixer.Sound("other/point.mp3")

 

menu_on = True
play = True
running = False
caption_timeout = 0
caption_list = []
enemy_blind_timeout = 0
image_tick = True
os.environ["SDL_VIDEO_CENTERED"] = '1'

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(gm.SIZESCREEN)

class Character(pygame.sprite.Sprite):
    def __init__(self,file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self._count = 0
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def stop(self):
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        
    def animate(self, image_list):
        self.image = image_list[self._count//3]
        self._count = (self._count + 1) % 9

class Pacman(Character):
    def __init__(self, file_image):
        super().__init__(file_image)
        self.points = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
                self.move_right = False
                self.move_down = False 
                self.move_up = False
            if event.key == pygame.K_RIGHT:
                self.move_left = False
                self.move_right = True
                self.move_down = False 
                self.move_up = False
            if event.key == pygame.K_UP:
                self.move_left = False
                self.move_right = False
                self.move_down = False 
                self.move_up = True
            if event.key == pygame.K_DOWN:
                self.move_left = False
                self.move_right = False
                self.move_down = True
                self.move_up = False
                
    
        
    def update(self):
        #ruch we wszystkich kierunkach i wywolanie animacji
        if self.move_left:
            self.rect.x -= 4
            self.animate(gm.PACMAN_WALK_LIST_L)
        if self.move_right:
            self.rect.x += 4
            self.animate(gm.PACMAN_WALK_LIST_R)
        if self.move_up:
            self.rect.y -= 4
            self.animate(gm.PACMAN_WALK_LIST_U)
        if self.move_down:
            self.rect.y += 4
            self.animate(gm.PACMAN_WALK_LIST_D)
        
        #kolizja ze scianami    
        colliding_blocks = pygame.sprite.spritecollide(self, main_board.list_of_blocks, False)
        
        for block in colliding_blocks:
            if self.move_down:
                self.rect.bottom = block.rect.top
            if self.move_up:
                self.rect.top = block.rect.bottom
            if self.move_left:
                self.rect.left = block.rect.right
            if self.move_right:
                self.rect.right = block.rect.left
            self.stop()
            
        #kolizja z punktami do zdobycia
        colliding_points = pygame.sprite.spritecollide(self, main_board.list_of_points, True)
        for point in colliding_points:
            self.points += 5
            
        #kolizja z przeciwnikami
        colliding_enemies = pygame.sprite.spritecollide(self, list_of_enemies, False)
        global running
        global caption_timeout
        for enemy in colliding_enemies:
            if enemy.active:
                time.sleep(3)
                running = False
                print("GAME OVER!")
            else:
                font = pygame.font.Font('freesansbold.ttf', 10)
                kill_text = font.render("200", True, (255,255,0), (0,0,0))
                kill_text_rect = kill_text.get_rect()
                kill_text_rect.center = enemy.rect.center
                caption_list.append([kill_text,kill_text_rect])
                caption_timeout = 0
                enemy.kill()
                player.points += 200
                
        #kolizja z transform blokami:
        colliding_tr_blocks = pygame.sprite.spritecollide(self, main_board.list_of_transform_blocks, True)
        global enemy_blind_timeout        
        for tr in colliding_tr_blocks:
            for el in list_of_enemies:
                el.active = False
            tr.kill()
            transform_sound.play()
            enemy_blind_timeout = 1

        
class Enemy(Character):
    def __init__(self,file_image):
        super().__init__(file_image)
        self.active = True
        #poczatkowo ustawione move_right zeby zaczal sie gdziekowiek ruszac, potem juz losowy ruch
        self.move_right = True
        
        
    def update(self):
        #ruch we wszystkich kierunkach i wywolanie animacji ORAZ ANIMACJA DLA NIEAKTYWNYCH
        if self.move_left:
            self.rect.x -= 3
            if self.active == False:
                self.image = gm.ENEMY_BLIND_ONE_IMG_LIST[0]
            else:
                self.image = gm.ENEMY_WALK_LIST[2]
        if self.move_right:
            self.rect.x += 3
            if self.active == False:
                self.image = gm.ENEMY_BLIND_ONE_IMG_LIST[0]
            else:
                self.image = gm.ENEMY_WALK_LIST[0]
        if self.move_up:
            self.rect.y -= 3
            if self.active == False:
                self.image = gm.ENEMY_BLIND_ONE_IMG_LIST[0]
            else:
                self.image = gm.ENEMY_WALK_LIST[3]
        if self.move_down:
            self.rect.y += 3
            if self.active == False:
                self.image = gm.ENEMY_BLIND_ONE_IMG_LIST[0]
            else:
                self.image = gm.ENEMY_WALK_LIST[1]
        
        #kolizja ze scianami    
        colliding_blocks = pygame.sprite.spritecollide(self, main_board.list_of_blocks, False)
        
        for block in colliding_blocks:
            if self.move_down:
                self.rect.bottom = block.rect.top
            if self.move_up:
                self.rect.top = block.rect.bottom
            if self.move_left:
                self.rect.left = block.rect.right
            if self.move_right:
                self.rect.right = block.rect.left
        
            self.stop()
            self.change_move_direction()
            
    def change_move_direction(self):
        number = randrange(0,4,1)
        
        if number == 0:
            self.move_right = True
            self.move_left = False
            self.move_down = False
            self.move_up = False
        elif number == 1:
            self.move_right = False
            self.move_left = True
            self.move_down = False
            self.move_up = False
        elif number == 2:
            self.move_right = False
            self.move_left = False
            self.move_down = True
            self.move_up = False
        elif number == 3:
            self.move_right = False
            self.move_left = False
            self.move_down = False
            self.move_up = True
        

main_board = Board(level1_board)
main_board.create()
        
player = Pacman(gm.PACMAN_WALK_LIST_R[0])
player.rect.center = screen.get_rect().center

#rozmieszczanie przeciwnikow:

amount_of_points = len(main_board.list_of_points)
list_of_enemies = pygame.sprite.Group()
for i in range(0,10):
    enemy = Enemy(gm.ENEMY_WALK_LIST[0])
    #losowe rozmieszczanie przeciwnikow tam gdzie bloki z punktami
    enemy.rect.center = main_board.list_of_points.sprites()[randrange(0,amount_of_points)].rect.center
    list_of_enemies.add(enemy)
    

pygame.display.set_caption("Michal Nawara's PACMAN")

font = pygame.font.Font('freesansbold.ttf', 16)



r1 = pygame.Rect(200, 300, 400, 150)
r2 = pygame.Rect(200, 500, 400, 150)
r3 = pygame.Rect(200, 500, 450, 200)
r3.center = r1.center



#petla z menu
while menu_on == True:
    screen.fill(gm.DARK)
    pygame.draw.rect(screen, (255,255,0), r3)
    pygame.draw.rect(screen, (0,0,255), r1)
    pygame.draw.rect(screen, (0,0,255), r2)
    
    menu_font_big = pygame.font.Font('freesansbold.ttf', 70)
    menu_font_main = pygame.font.Font('freesansbold.ttf', 100)
    play_text = menu_font_big.render("PLAY!", True, (255,255,0), (0,0,255))
    exit_text = menu_font_big.render("EXIT", True, (255,255,0), (0,0,255))
    main_text = menu_font_main.render("PACMAN", True, (255,255,0), (0,0,0))
    
    play_text_rect = play_text.get_rect()
    play_text_rect.center = r1.center
    screen.blit(play_text, play_text_rect)
    
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.center = r2.center
    screen.blit(exit_text, exit_text_rect)
    
    main_text_rect = main_text.get_rect()
    main_text_rect.center = (400,150)
    screen.blit(main_text, main_text_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # klikniecie przycisku zamkniecia okna (X)
            menu_on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_on = False
            elif event.key == pygame.K_DOWN:
                play = False
                r3.center = r2.center
            elif event.key == pygame.K_UP:
                play = True
                r3.center = r1.center
            elif event.key == pygame.K_RETURN:
                if play:
                    menu_on = False
                    running = True
                else:
                    menu_on = False
    pygame.display.flip()

    clock.tick(30)

while running:
    #koniec gry
    if len(list_of_enemies) == 0 or len(main_board.list_of_points) == 0:
        time.sleep(1)
        running = False
        print("GAME OVER!")
    # obsluga zdarzen (event handling)
    screen.fill(gm.DARK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # klikniecie przycisku zamkniecia okna (X)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        player.handle_event(event)
            
    player.update()
    main_board.draw()
        
    #migotanie przeciwnikow
    if enemy_blind_timeout == 0:
        for enemy in list_of_enemies:
            enemy.draw(screen)
            enemy.update()
    elif enemy_blind_timeout > 0 and enemy_blind_timeout < 210:
        for enemy in list_of_enemies:
            enemy.draw(screen)
            enemy.update()
        enemy_blind_timeout += 1
    elif enemy_blind_timeout >= 210 and enemy_blind_timeout < 330:
        if image_tick:
            for enemy in list_of_enemies:
                enemy.draw(screen)
                enemy.update()
                image_tick = False
        else:
            image_tick = True
        
        enemy_blind_timeout += 1
    else:
        #zmiana na aktywne
        for enemy in list_of_enemies:
            enemy.draw(screen)
            enemy.active = True
        enemy_blind_timeout = 0    
    #napis po przeciwniku:
    if caption_timeout < 90:
        caption_timeout += 1
        for el in caption_list:
            screen.blit(el[0], el[1])
    else:
        caption_timeout = 0
        caption_list.clear()
        
    player.draw(screen)

    #rysowanie ramki na okolo gry
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(0, 0, 800, 40))
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(0, 0, 40, 800))
    
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(0, 760, 800, 40))
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(760, 0, 40, 800))
    
    
    #napis z punktami:
    
    points_text = font.render('Points: ' + str(player.points), True, (255,255,0), (0,0,255))
    points_text_rect = points_text.get_rect()
    points_text_rect.bottomleft = (40, 780)

    screen.blit(points_text, points_text_rect)
                

    pygame.display.flip()

    clock.tick(30)

pygame.quit()