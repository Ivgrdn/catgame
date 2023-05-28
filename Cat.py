import pygame
HEIGHT = 600
WIDTH = 1000
JUMP_NUMBER = 11
MIN_POSITION = 500
from sprites import *
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        global JUMP_NUMBER
        pygame.sprite.Sprite.__init__(self)
        self.x = 200
        self.up_collision = False
        self.image = pygame.transform.scale(pygame.image.load('cat_right1.png'), (100, 80))
        self.y = MIN_POSITION
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.player_speed = 30
        self.jump = False
        self.jump_number = JUMP_NUMBER
        self.gravity = 7
        self.left = False
        self.right = True
        self.jump_count = JUMP_NUMBER
        self.player_animation = 0
        self.height = 60
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()
        self.gravity_num = 1
    def update(self):
        self.gravity_num+=0.5
        walk_left = [pygame.transform.scale(pygame.image.load('cat_left1.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_left2.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_left3.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_left4.png'), (100, 80))] 
        walk_right = [pygame.transform.scale(pygame.image.load('cat_right1.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_right2.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_right3.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_right4.png'), (100, 80))]
        keys = pygame.key.get_pressed()
        self.gravity = 7
        if keys[pygame.K_SPACE]:
            if not self.jump:
                self.jump = True
        if self.jump:
            self.gravity = 0
            self.gravity_num = 0
            if self.jump_count>=0:
                self.pos.y-=(self.jump_count**2)/2
                if self.right:
                    self.image = pygame.transform.scale(pygame.image.load('cat_right_up.png'), (100, 80))
                elif self.left:
                    self.image = pygame.transform.scale(pygame.image.load('cat_left_up.png'), (100, 80))
            elif (self.jump_count<0) and self.pos.y<MIN_POSITION and not self.up_collision:
                self.pos.y+=(self.jump_count**2)/2
                if self.right:
                    self.image = pygame.transform.scale(pygame.image.load('cat_right_down.png'), (100, 80))
                elif self.left:
                    self.image = pygame.transform.scale(pygame.image.load('cat_left_down.png'), (100, 80))
            else:
                self.jump_count = JUMP_NUMBER
                self.jump = False
                self.jump_number = JUMP_NUMBER
            self.jump_count-=1
                

        if keys[pygame.K_LEFT]:
            self.pos.x -= self.player_speed
            self.left = True
            self.right = False
            if not self.jump:
                self.image = walk_left[self.player_animation]
        elif keys[pygame.K_RIGHT]:
            self.pos.x +=self.player_speed
            self.left = False
            self.right = True
            if not self.jump:
                self.image = walk_right[self.player_animation]
        elif not sum([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_SPACE]]) and not self.jump:
            if self.left:
                self.image = walk_left[0]
            elif self.right:
                self.image = walk_right[0]
        
        self.player_animation = (self.player_animation+1)%4
        self.pos.y+=self.gravity*self.gravity_num

    def collisions(self, direction, collision_list):
        self.up_collision = False
        collision_sprites = pygame.sprite.spritecollide(self,collision_list,False)
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    print(self.rect.topleft)
                    print(self.old_rect.topleft)
					# collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        print('left')

					# collision on the left
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        print('right')
		
            if direction == 'vertical':
                for sprite in collision_sprites:
                    
					# collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.gravity = 0
                        self.gravity_num = 0
                        self.up_collision = True
                        print('top')
                    else:
                        self.up_collision = False
					# collision on the top
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
                            self.jump_count = 0
                            print('bottom')
                
    def window_collision(self, window_w, window_h):
        x_num = 0
        y_num = 0
        if self.pos.y>MIN_POSITION:
            self.gravity = 0
            self.gravity_num = 0
            self.pos.y = MIN_POSITION
        elif window_h > HEIGHT and self.pos.y<0:
            y_num = self.pos.y
        elif window_w > WIDTH and self.pos.x>WIDTH:
            return self.pos.x - WIDTH
        elif window_w == WIDTH and self.pos.x>WIDTH-30:
            self.pos.x = WIDTH-30
        elif window_w == WIDTH and self.pos.x<30:
            self.pos.x = 30
        elif window_h == HEIGHT and self.pos.y<0:
            self.pos.y = 0
        return x_num, y_num
        