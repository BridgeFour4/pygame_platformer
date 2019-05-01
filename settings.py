# game options/settings
TITLE ="Jumpy"
WIDTH = 480 # width of game window
HEIGHT = 600 # height of screen
FPS = 60 # frames
FONT_NAME = 'arial'
HS_FILE= "highscore.txt"
SPRITESHEET ="spritesheet_jumper.png"

#player proppeties
PLAYER_ACC = 0.5
PLAYER_FRICTION= -0.12
PLAYER_GRAV=0.8
PLAYER_JUMP = 22

# game properties
BOOST_POWER = 60
POW_SPAWN = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER=0

#Starting platform
PLATFORM_LIST=[(0,HEIGHT-60),
              (WIDTH /2 -50, HEIGHT *3/ 4),
              (125,HEIGHT -350),
              (350,200),
              (175,100),
              (125,350)]

#COLORS (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW =(255,255,0)
LIGHTBLUE = (0,155,155)
BGCOLOR = LIGHTBLUE