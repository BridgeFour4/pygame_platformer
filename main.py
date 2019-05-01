#jumpy platform game part 10
#Art from Kenny.nl
# Happy Tune by http://opengameart.org/users/syncapiko
#Yippee by http://opengameart.org/users/snabisk
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #initializize game elements
        pg.init()
        pg.mixer.init()  # for sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir= path.dirname(__file__)
        img_dir = path.join(self.dir,'img')
        with open(path.join(self.dir,HS_FILE),"r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # load clouds
        self.cloud_images =[]
        for i in range(1,4):
            self.cloud_images.append((pg.image.load(path.join(img_dir,'cloud{}.png'.format(i))).convert()))

        #load_sound
        self.snd_dir = path.join(self.dir,'snd')
        self.jumpsound = pg.mixer.Sound(path.join(self.snd_dir,'Jump3.wav'))
        self.boostsound = pg.mixer.Sound(path.join(self.snd_dir, 'Powerup.wav'))


    def new(self):
        #starts game again resets values
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms =pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
            pg.mixer.music.load(path.join(self.snd_dir,'happytune.ogg'))
        for i in range(10):
            c = Cloud(self)
            c.rect.y+=500
        self.mob_timer =0
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)


    def update(self):
        #game loop update
        self.all_sprites.update()

        #spawn mob
        now = pg.time.get_ticks()
        if now - self.mob_timer >5000 + random.choice([-1000,-500,0,500,1000]):
            self.mob_timer = now
            Mob(self)

        # hit mobs
        mob_hits = pg.sprite.spritecollide(self.player,self.mobs,False, pg.sprite.collide_mask )
        if mob_hits:
            self.playing = False

        #check if player hits platform only if falling
        if self.player.vel.y>0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit .rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right and self.player.pos.x>lowest.rect.left:
                    if self.player.pos.y<lowest. rect.bottom:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top of screen scroll over the screen
        if self.player.rect.top < HEIGHT/4:
            if random.randint(1,100)<15:
                Cloud(self)
            self.player.pos.y +=max(abs(self.player.vel.y),2)
            for cloud in self.clouds:
                cloud.rect.y +=max(abs(self.player.vel.y/random.randint(2,4)),2)
            for mob in self.mobs:
                mob.rect.y +=max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y +=max(abs(self.player.vel.y),2)
                if plat.rect.top>=HEIGHT:
                    plat.kill()
                    self.score+=10

        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player,self.powerups,True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
                self.boostsound.play()

        # if we fall off the bottom
        if self.player.rect.bottom >HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y-=max(self.player.vel.y,10)
                if sprite.rect.bottom<0:
                    sprite.kill()
        if len(self.platforms)==0:
            self.playing=False

        #spawn new platforms to keep some aveerage number
        while len(self.platforms)<6:
            width = random.randrange(30,85)
            Platform(self,random.randrange(0,WIDTH - width),
                         random.randrange(-75,-30))

    def events(self):
        # game loop events
        # process input
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing=False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        #game loop draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22,WHITE,WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Arrows to move space to jump ",22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('press a key to start',22,WHITE,WIDTH/2, HEIGHT*3/4 )
        self.draw_text('High Score: '+str(self.highscore), 22, WHITE, WIDTH / 2,15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: "+ str(self.score), 22, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text('press a key to play again', 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore= self.score
            self.draw_text("NEW HIGH SCORE! ", 22, GREEN, WIDTH / 2, HEIGHT / 2+40)
            with open(path.join(self.dir,HS_FILE),'w')as f:
                f.write(str(self.highscore))
        else:
            self.draw_text('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2+40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)


g = Game();
g.show_start_screen()
while g.running :
    g.new()
    g.show_go_screen()
pg.quit()