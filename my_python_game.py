# Packages
import pygame

import sys

import os

import random

import math

from button import Button

# Initializing Pygame
pygame.init()

WIDTH = 1125
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH,HEIGHT))

def get_font(size):
    return pygame.font.Font('game_font.ttf', size)
def play():
    while True:
        screen.fill("BLUE")
        clock = pygame.time.Clock()

        #Background image

        background_image = pygame.image.load('background.jpg')

        #Player image

        player_image = pygame.image.load('bunny_avatar.png')

        #Enemy Image

        otter_enemy = pygame.image.load('otter_enemy.png')

        fox_enemy = pygame.image.load('fox_enemy.png')

        duck_enemy = pygame.image.load('duck_enemy.png')

        enemy_array = [otter_enemy, fox_enemy, duck_enemy]

        bullet_image = pygame.image.load('bullet.png')

        # Objects

        class Player(pygame.sprite.Sprite):

            def __init__ (self):
                pygame.sprite.Sprite.__init__(self)
                self.movex = 0
                self.movey = 0
                self.frame = 0
                self.images = []
                for i in range(1,5):
                    img = player_image
                    img.convert_alpha()
                    self.images.append(img)
                    self.image = self.images[0]
                    self.rect = self.image.get_rect()
            def control(self, x, y):
                self.movex += x
                self.movey += y
            def update(self):
                self.rect.x += self.movex
                self.rect.y += self.movey
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > 1125:
                    self.rect.right = 1125
                if self.rect.top <= 0:
                    self.rect.top = 0
                if self.rect.bottom >= 750:
                    self.rect.bottom = 750
            def shoot(self):
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    player_list.add(bullet)
                    bullets.add(bullet)
        # Opponent Class
        class Mob(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = random.choice(enemy_array)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(1125 - self.rect.width)
                self.rect.y = random.randrange(0,1)
                self.speedy = random.randrange(1,8)
                self.speedx = random.randrange(-3,3)
            def update(self):
                self.rect.y += self.speedy
                self.rect.x += self.speedx

                if self.rect.top > HEIGHT + 10 or self.rect.left < -30 or self.rect.right > WIDTH:
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-100, 0)
                    self.speedy = random.randrange(1,8)
                    self.speedx = random.randrange(-3,3)
                    
        class Bullet(pygame.sprite.Sprite):
                def __init__(self,x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = bullet_image
                    self.rect = self.image.get_rect()
                    self.rect.bottom = y
                    self.rect.centerx = x
                    self.speedy = -10
                    
                def update(self):
                    self.rect.y += self.speedy
                    if self.rect.bottom < 0:
                        self.kill()
        # Adding the Player
        player = Player()
        player.rect.x = 470
        player.rect.y = 750
        player_list = pygame.sprite.Group()
        player_list.add(player)
        # Adding the Enemies
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        steps = 1
        m = Mob()
        for i in range(5):
            m = Mob()
            player_list.add(m)
            mobs.add(m)         
        if len(mobs) == 0:
            main_menu()
        def main():
            online = True
            move_left = False
            move_right = False
            move_up = False
            move_down = False   
            while online:
                # Collisions
                collisions = pygame.sprite.spritecollide(player, mobs, False)
                if collisions:
                    main_menu() # Change to a "YOU LOSE" SCREEN
                collisions = pygame.sprite.groupcollide(mobs, bullets, True, True)
                print(len(mobs))
                if len(mobs) == 0:
                    main_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        online = False
                        pygame.QUIT()
                        sys.quit()
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.KEYDOWN:
                        if keys[pygame.K_a]:
                            move_left = True
                        if keys[pygame.K_s]:
                            move_down = True
                        if keys[pygame.K_w]:
                            move_up = True
                        if keys[pygame.K_d]:
                            move_right = True
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        player.shoot()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            move_left = False
                        if event.key == pygame.K_s:
                            move_down = False
                        if event.key == pygame.K_w:
                            move_up = False
                        if event.key == pygame.K_d:
                            move_right = False
                if(move_right):
                    player.control(steps/5,0)
                if(move_left):
                    player.control(-steps/5,0)
                if(move_up):
                    player.control(0,-steps/5)
                if(move_down):
                    player.control(0,steps/5)
                drawWindow()
        # Drawing Window
        def drawWindow():
            screen.blit(background_image, (0,0))
            player_list.draw(screen)
            player.update()
            player_list.update()
            pygame.display.flip()
            clock.tick(60)
            pygame.display.update()
            bullets.update()
        # Run main()
        main()
        
        pygame.display.update()
def settings():
    while True:
        background3 = pygame.image.load('background.jpg')
        screen.blit(background3,(0,0))
        
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()
        MAIN_MENU = Button(image = pygame.image.load("settings_image.jpg"), pos=(562.5,650), text_input ="MAIN MENU", font=get_font(75),base_color = "RED", hovering_color = "#967bb6")
        RESOLUTION = Button(image = pygame.image.load("settings_image.jpg"), pos=(562.5,300), text_input ="RESOLUTION", font=get_font(75),base_color = "RED", hovering_color = "#967bb6")
        for button in [MAIN_MENU,RESOLUTION]:
            button.changeColor(SETTINGS_MOUSE_POS)
            button.update(screen)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if MAIN_MENU.checkforInput(SETTINGS_MOUSE_POS):
                    main_menu()
               
        pygame.display.update()
def exit():
    while True:
        sys.quit()
        pygame.QUIT()  
def main_menu():
    while True:
        background2 = pygame.image.load('background2.jpg')
        screen.blit(background2, (0,0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "BLACK")
        
        MENU_RECT = MENU_TEXT.get_rect(center=(562.5,50))
        
        PLAY_BUTTON = Button(image = pygame.image.load("playbutton_image.jpg"), pos=(562.5,250), text_input ="PLAY", font=get_font(75),base_color = "RED", hovering_color = "#967bb6")
        
        SETTINGS_BUTTON = Button(image = pygame.image.load("settings_image.jpg"), pos=(562.5,450), text_input ="SETTINGS", font=get_font(75),base_color = "RED", hovering_color = "#967bb6")

        EXIT_BUTTON = Button(image = pygame.image.load("playbutton_image.jpg"), pos=(562.5,650), text_input ="EXIT", font=get_font(75),base_color = "RED", hovering_color = "#967bb6")

        
        screen.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, SETTINGS_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkforInput(MENU_MOUSE_POS):
                    play()
                if EXIT_BUTTON.checkforInput(MENU_MOUSE_POS):
                    quit()
                if SETTINGS_BUTTON.checkforInput(MENU_MOUSE_POS):
                    settings()
        pygame.display.update()
main_menu()