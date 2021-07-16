import pygame
import sys
from pygame.locals import *
import random

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 250
WIDTH = 600
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

platforms = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("static/dino.png")
        self.image = pygame.transform.scale(self.image,(30,30))
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((70,70,70))
        self.rect = self.surf.get_rect()
  
        self.pos = vec((10, 160))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hiding = False

    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.image = pygame.image.load("static/dino.png")
            self.image = pygame.transform.scale(self.image,(30,30))
            self.vel.y = -8
            self.hiding = False

    def hide(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.image = pygame.image.load("static/dino_hide.png")
            self.image = pygame.transform.scale(self.image,(30,30))
            self.hiding = True

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1


class Cactus(pygame.sprite.Sprite):
    def __init__(self, pre_x):
        super().__init__() 
        self.image = pygame.image.load("static/cact.png")
        self.image = pygame.transform.scale(self.image,(30,30))
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,128,128))
        self.rect = self.surf.get_rect()
  
        self.pos = vec((pre_x, 260))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self): 
        self.acc = vec(0,0.5)
        self.acc.x = -ACC
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            return 1
            
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1


class Bird(pygame.sprite.Sprite):
    def __init__(self, pre_x):
        super().__init__() 
        self.image = pygame.image.load("static/bird.png")
        self.image = pygame.transform.scale(self.image,(30,30))
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,128,128))
        self.rect = self.surf.get_rect()
  
        self.pos = vec((pre_x, 220))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self): 
        self.acc = vec(0,0)
        self.acc.x = -ACC
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            self.pos = vec((self.pos.x, random.randint(20,25)*10))
            return 1
            
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 1))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 19))

    def move(self):
        return 0

 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
def dino_game(counter):
    PT1 = platform()
    P1 = Player()
    C1 = Cactus(10)
    B1 = Bird(200)

    platforms.add(PT1)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(PT1)
    all_sprites.add(P1)
    all_sprites.add(C1)
    all_sprites.add(B1)

    while True:
        text = font.render(str(counter), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP and P1.pos.y > 231:
                    P1.jump()
                    counter += 1
                elif event.key == pygame.K_DOWN and P1.hiding == False  and P1.pos.y > 231:
                    P1.hide()
                    counter += 1
    
        displaysurface.fill((255,255,255))
        P1.update()
        C1.update()
        B1.update()
        if P1.pos.y == C1.pos.y and C1.pos.x < 30:        
            break
        if B1.pos.x-15 <= P1.pos.x <= B1.pos.x+15 and B1.pos.y-25 <= P1.pos.y <= B1.pos.y+5 and P1.hiding == False:        
            break
        if B1.pos.x-15 <= P1.pos.x <= B1.pos.x+15 and B1.pos.y-25 <= P1.pos.y <= B1.pos.y:        
            break

        displaysurface.blit(text, textRect)
        for entity in all_sprites:
            try:
                displaysurface.blit(entity.image, entity.rect)
            except:
                displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS+counter)


def main_menu(counter):
    while True:
        displaysurface.fill((0,0,0))
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(WIDTH // 3, HEIGHT // 3, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                dino_game(counter)
        
        pygame.draw.rect(displaysurface, (255, 255, 255), button_1)
        draw_text('начать игру', font, (0, 0, 0), displaysurface, WIDTH // 2.9, HEIGHT // 2.8)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        FramePerSec.tick(FPS+counter)


click = False
counter = 0
font = pygame.font.Font('static/freesansbold.ttf', 32)
main_menu(counter)
