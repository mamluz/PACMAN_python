# okno główne
import pygame, os
SIZESCREEN = WIDTH, HEIGHT = 800, 800
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# kolory
DARK = pygame.color.THECOLORS['black']


screen = pygame.display.set_mode(SIZESCREEN)

# grafika  - wczytywanie grafik
print(os.curdir)

path = os.path.join('assets')
file_names = sorted(os.listdir(path))
file_names.remove('background.png')
file_names.remove('.DS_Store') #MACOS MUSIAL STWORZYC TAKI PLIK I NIE DA SIE TEGO WYLACZYC DLATEGO NIE DZIALALO :))))))))
BACKGROUND = pygame.image.load(os.path.join(path, 'background.png')).convert()
for file_name in file_names:
    image_name = file_name[:-4].upper()
    globals()[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

PACMAN_WALK_LIST_R = [PACMAN_1, PACMAN_2_RIGHT, PACMAN_3_RIGHT]
PACMAN_WALK_LIST_L = [PACMAN_1, PACMAN_2_LEFT, PACMAN_3_LEFT]
PACMAN_WALK_LIST_U = [PACMAN_1, PACMAN_2_UP, PACMAN_3_UP]
PACMAN_WALK_LIST_D = [PACMAN_1, PACMAN_2_DOWN, PACMAN_3_DOWN]

BLOCK_LIST = [RIGHT_CLOSED_BLOCK, DOWN_CLOSED_BLOCK, LEFT_CLOSED_BLOCK, UP_CLOSED_BLOCK,
              OPEN_HORIZONTAL_BLOCK, OPEN_VERTICAL_BLOCK, POINT_BLOCK, ENEMY_TRANSFORM_BLOCK,
              THREE_WAY_OPEN_RIGHT_BLOCK, THREE_WAY_OPEN_DOWN_BLOCK, THREE_WAY_OPEN_LEFT_BLOCK, THREE_WAY_OPEN_UP_BLOCK,
              BORDER, POINT_BLOCK]

ENEMY_WALK_LIST = [ENEMY_RIGHT, ENEMY_DOWN, ENEMY_LEFT, ENEMY_UP]

ENEMY_BLIND_ONE_IMG_LIST = [ENEMY_BLIND]




