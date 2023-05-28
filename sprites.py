import pygame
from Cat import Cat
HEIGHT = 600
WIDTH = 1000
# pygame.draw.rect(self.screen, (210, 134, 34, 255),self.rect)
MIN_POSITION = 500
import time
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.width = w
        self.height = h
        
        self.image = pygame.transform.scale(image,(self.width, self.height))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.door_image = 'door_closed.png'
        self.rect.y = y
        self.old_rect = self.rect.copy()
    
class Door(pygame.sprite.Sprite):
    def __init__(self, door_image, platform, dimension):
        pygame.sprite.Sprite.__init__(self)
        self.platform = platform
        self.dimension = dimension
        self.door_image = door_image
        self.image = pygame.transform.scale(self.door_image,(120, 170))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform
    def update(self, door_image):
        self.door_image = door_image
        self.image = pygame.transform.scale(pygame.image.load(self.door_image),(120, 170))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform

def platform_door(dimension, door_image):
        platform_list = dimension.platforms_list
        platform_param = dimension.platform_param
        door_list = dimension.door_list
        door_dimension = dimension.door_dimension
        doors = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        counter = 0
        for i, d, p in zip(platform_list, door_list, platform_param):
            platforms.add(Platform(dimension.image_platform, i[0], i[1], p[0], p[1]))
            if d==1:
                doors.add(Door(door_image, Platform(dimension.image_platform, i[0], i[1],p[0], p[1]).rect.midtop, door_dimension[counter]))
                counter+=1  
        return doors, platforms
        
class void():
    def __init__(self, screen):
        self.dimension = 0
        self.screen = screen
        self.door_image = pygame.image.load('door_closed.png')
        self.platforms_list = [[400, 400], [750, 250], [300, 200]]
        self.platform_param = [[200, 60],[200, 60],[200, 60]]
        self.bg = pygame.image.load("void_bg.png")
        self.image_platform = pygame.image.load('platform.png')
        self.door_list = [0, 1, 1]
        self.cat = Cat()
        self.door_dimension = [1, 2]
    def update(self):
        self.cat.old_rect = self.cat.rect.copy()
        doors, platforms = platform_door(void(self.screen), self.door_image)
        platforms.draw(self.screen)
        
        hits_door = pygame.sprite.spritecollide(self.cat, doors, False)
        if hits_door:
            hits_door[0].update('door_open.png')
            point = pygame.mouse.get_pos()
            collide = hits_door[0].rect.collidepoint(point)
            if collide and pygame.mouse.get_pressed()[0]:
                dimension_num = hits_door[0].dimension
                print(dimension_num)
                return dimension_num
        doors.draw(self.screen)
        self.collision_list = pygame.sprite.Group()
        for i in platforms:
            self.collision_list.add(i)
            # pygame.draw.rect(self.screen, (210, 134, 34, 255),i.rect)
        self.cat.update()
        self.cat.rect.x = round(self.cat.pos.x)
        self.cat.collisions('horizontal', self.collision_list)
        self.cat.rect.y = round(self.cat.pos.y)
        self.cat.collisions('vertical', self.collision_list)
        self.cat.window_collision(1000, 600)
        self.screen.blit(self.cat.image, (self.cat.pos))
        # pygame.draw.rect(self.screen, (210, 134, 34, 255),self.cat.rect)
        

        return self.dimension

        
class forest():
    def __init__(self, screen):
        self.dimension = 1
        self.quest = False
        self.screen = screen
        self.cat = Cat()
        self.door_image = pygame.image.load('door_closed.png')
        self.platforms_list = [[603, 527], [70, 226],[281, 339], [630, 214], [847, 163], [0, 425]]
        self.platform_param = [[400, 73],[130, 30],[130, 30], [130, 30], [130, 30], [198, 175]]
        self.image_platform = pygame.image.load('platform.png')
        self.image_platform.set_alpha(0)
        self.door_list = [1, 0, 0, 0, 0, 0]
        self.object_logo = pygame.transform.scale(pygame.image.load('yarn_ball_logo.png'), (30, 25))
        self.object_image = pygame.transform.scale(pygame.image.load('yarn_ball.png'), (60, 55))
        self.door_dimension = [0]
        self.collision_list = []
        self.object = Object(self.object_image, 500, 490, self.screen, self.collision_list)
        self.bg = pygame.image.load('forest.jpeg')
        self.npc = Npc([pygame.transform.scale(pygame.image.load('npc1_1.png'), (80, 60)),pygame.transform.scale(pygame.image.load('npc1_2.png'), (80, 60)),pygame.transform.scale(pygame.image.load('npc1_3.png'), (80, 60)),pygame.transform.scale(pygame.image.load('npc1_4.png'), (80, 60))], 847, 103, self.screen, self.quest, self.object_logo)
    def update(self):
        self.cat.old_rect = self.cat.rect.copy()
        self.object.old_rect = self.object.rect.copy()
        doors, platforms = platform_door(forest(self.screen), self.door_image)
        self.collision_list = pygame.sprite.Group()
        for i in platforms:
            self.collision_list.add(i)
        self.collision_list.add(self.npc)
        hits_door = pygame.sprite.spritecollide(self.cat, doors, False)
        if hits_door and self.quest:
            hits_door[0].update('door_open.png')
            point = pygame.mouse.get_pos()
            collide = hits_door[0].rect.collidepoint(point)
            if collide and pygame.mouse.get_pressed()[0]:
                dimension_num = hits_door[0].dimension
                return dimension_num
        platforms.draw(self.screen)
        doors.draw(self.screen)
        self.npc.update()
        self.cat.update()
        self.object.update()


        self.collision_list.add(self.cat)
        self.object.rect.x = round(self.object.pos.x)
        self.object.collisions('horizontal', self.collision_list)
        self.object.rect.y = round(self.object.pos.y)
        self.object.collisions('vertical', self.collision_list)
        self.object.old_rect = self.object.rect.copy()


        self.collision_list.remove(self.cat)
        self.object.rect.x = round(self.object.pos.x)
        self.object.collisions('horizontal', self.collision_list)
        self.object.rect.y = round(self.object.pos.y)
        self.object.collisions('vertical', self.collision_list)


        # self.collision_list.remove(self.cat)
        # self.collision_list.add(self.object)
        self.cat.rect.x = round(self.cat.pos.x)
        self.cat.collisions('horizontal', self.collision_list)
        self.cat.rect.y = round(self.cat.pos.y)
        self.cat.collisions('vertical', self.collision_list)
        self.cat.window_collision(1000, 600)


        pygame.draw.rect(self.screen,(123, 45, 79), self.object.rect)
        self.object.window_collision(1000, 600)
        self.screen.blit(self.cat.image, (self.cat.pos.x, self.cat.pos.y))
        self.screen.blit(self.object.image, (self.object.pos.x, self.object.pos.y))
        return self.dimension


class sun():
    def __init__(self, screen):
        self.dimension = 2
        self.quest = False
        self.screen = screen
        self.cat = Cat()
        self.door_image = pygame.image.load('door_closed.png')
        self.platforms_list = [[0, 0], [100, 80], [400, 350]]
        self.platform_param = [[200, 60],[200, 60],[200, 60]]
        self.image_platform = pygame.image.load('platform.png')
        self.door_list = [1, 0, 0]
        self.door_dimension = [0]
        self.bg = pygame.image.load("cave.jpeg")
    def update(self):
        doors, platforms = platform_door(sun(self.screen), self.door_image)
        platforms.draw(self.screen)
        hits_door = pygame.sprite.spritecollide(self.cat, doors, False)
        if hits_door and self.quest:
            hits_door[0].update('door_open.png')
            point = pygame.mouse.get_pos()
            collide = hits_door[0].rect.collidepoint(point)
            if collide and pygame.mouse.get_pressed()[0]:
                dimension_num = hits_door[0].dimension
                self.cat = Cat()
                return dimension_num
        doors.draw(self.screen)
        self.screen.blit(self.cat.image, (self.cat.x, self.cat.y))
        return self.dimension
    




        
class Object(pygame.sprite.Sprite):
    def __init__(self, image, x_start, y_start, screen, collision_list):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.pos.x  = x_start
        self.pos.y = y_start
        self.screen = screen
        self.collision_list = collision_list
        self.gravity_num = 1
        self.gravity = 10
        self.old_rect = self.rect.copy()
    def update(self):
        self.gravity_num+=0.5
        self.pos.y = self.pos.y +self.gravity
        # if self.y>=MIN_POSITION:
        #     self.gravity = 0
        #     self.gravity_num = 0
        #     self.y = MIN_POSITION
        self.pos.y+=self.gravity*self.gravity_num
    def collisions(self, direction, collision_list):
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
                            print('bottom')

                
    def window_collision(self, window_w, window_h):
        if self.rect.bottom>=MIN_POSITION:
            self.gravity = 0
            self.gravity_num = 0
            self.pos.y = MIN_POSITION
        elif window_w == WIDTH and self.pos.x>WIDTH-30:
            self.pos.x = WIDTH-30
        elif window_w == WIDTH and self.pos.x<30:
            self.pos.x = 30

        
       


class Npc(pygame.sprite.Sprite):
    def __init__(self, npc_animation, x, y, screen, quest, object):
        pygame.sprite.Sprite.__init__(self)
        self.animation = npc_animation
        self.image = self.animation[0]
        self.quest = quest
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.image1 = self.animation[0]
        self.image2 = self.animation[1]
        self.timer = time.process_time()
        self.timer2 = time.process_time()
        self.screen = screen
        self.object = object
        self.old_rect = self.rect.copy()
        self.buble = pygame.transform.scale(pygame.image.load('npc_dialog.png'), (50, 40))
        self.buble_animation = False
        self.buble_timer = 0
        self.cadr = 0
    def update(self):
        self.old_rect = self.rect.copy()
        if time.process_time() - self.timer>=1:
            if self.image1 == self.animation[0]:
                self.image1 = self.animation[2]
                self.image2 = self.animation[3]
            else:
                self.image1 = self.animation[0]
                self.image2 = self.animation[1]
            self.timer = time.process_time()
        if time.process_time() - self.timer2>=0.05:
            if self.image != self.image2:
                self.image = self.image2
            else:
                self.image = self.image1
            self.timer2 = time.process_time()
        self.screen.blit(self.image, (self.x, self.y))
        if self.buble_animation and time.process_time() - self.buble_timer<=0.5:
            self.screen.blit(self.buble, (self.rect.left - 3, self.rect.top-45))
            self.screen.blit(self.object, self.buble.get_rect().move(self.rect.left + 6, self.rect.top -38))
        else:
            self.buble_animation = False
        point = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(point)
        if collide and self.quest and pygame.mouse.get_pressed()[0]:
            # animation
            print('animation')
        elif collide and pygame.mouse.get_pressed()[0]:
            self.buble_animation  =True
            self.buble_timer = time.process_time()



    

