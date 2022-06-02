from pygame import *
from random import randint
import time as t

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("pygame window")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 15, 22)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update (self):
        self.rect.y -= self.speed 
        if self.rect.y < 0:
            self.kill()       

lost=0 #пропуски
score = 0

font.init()
font2 = font.SysFont('Arial', 36)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 690:
            self.rect.y = 0
            self.rect.x = randint(0, 690)
            self.speed = randint(2, 5)
            lost = lost + 1

#class Astro(GameSprite):
#    def update(self):
#        self.rect.y += self.speed
#        global lost
#        if self.rect.y >= 690:
#            self.rect.y = 0
#            self.rect.x = randint(0, 690)
#            self.speed = randint(5, 10)
#            lost = lost + 1


'''enemy1 = Enemy('ufo.png', randint(0, 690), 0, 80, 50, randint(2, 5))
enemy2 = Enemy('ufo.png', randint(0, 690), 0, 80, 50, randint(2, 5))
enemy3 = Enemy('ufo.png', randint(0, 690), 0, 80, 50, randint(2, 5))
enemy4 = Enemy('ufo.png', randint(0, 690), 0, 80, 50, randint(2, 5))
enemy5 = Enemy('ufo.png', randint(0, 690), 0, 80, 50, randint(2, 5))'''

monsters = sprite.Group()
#stones = sprite.Group()

for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
'''for i in range(1, 2):
    stone = Astro('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(5, 10))
    stones.add(stone)'''

ship = Player('rocket.png', 300, win_height  - 100, 80, 100,  12) #80 и 6 это скорость. было медленнее - 80, 4

fire_sound = mixer.Sound('fire.ogg')
max_lost = 35 #было 10
bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
            if e.key == K_w:
                fire_sound.play()
                ship.fire()
            if e.key == K_UP:
                fire_sound.play()
                ship.fire()


    if finish != True:
        # text5 = font2.render("Победа: убить 15 врагов" , 3, (255, 0, 0))
        # window.blit(text5, (300, 230) )
        # text6 = font2.render("Проигрыш: пропустил 35 врагов/дотронулся до врага" , 3, (255, 0, 0))
        # window.blit(text6, (300, 230) )
        window.blit(background, (0, 0))
        monsters.update()
        #stones.update()
        ship.update()
        ship.reset()

        monsters.draw(window)
        #stones.draw(window)
        bullets.update()
        
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True) #or sprite.groupcollide(stones, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            #stone = Astro('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(5, 10))
            #stones.add(stone)
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            text3 = font2.render("DEFEAT" , 3, (255, 0, 0))
            window.blit(text3, (300, 230) )
        '''if sprite.spritecollide(ship, stones, False):
            finish = True
            text3 = font2.render("DEFEAT" , 3, (255, 0, 0))
            window.blit(text3, (300, 230) )'''
        if  lost == 35:
            text3 = font2.render("DEFEAT" , 3, (255, 0, 0))
            window.blit(text3, (300, 230) )
            finish = True
        if score == 15:
            finish = True
            text4 = font2.render("VICTORY", 3, (0, 255, 150))
            window.blit(text4, (300, 230) )
        text = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text2 = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 30))
        window.blit(text2, (10, 60) )
        display.update()
        clock.tick(FPS) 