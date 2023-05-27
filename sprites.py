import pygame
# pygame.draw.rect(self.screen, (210, 134, 34, 255),self.rect)
JUMP_NUMBER = 10
MIN_POSITION = 500
import time
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.width = w
        self.height = h
        
        self.image = pygame.transform.scale(image,(self.width, self.height))
        self.rect = self.image.get_rect()
        self.old_rect = self.rect.copy()
        self.rect.x = x
        self.door_image = 'door_closed.png'
        self.rect.y = y
    
class up_platforms(Platform):
    def __init__(self, image, x, y, w, h):
        super().__init__(image, x, y, w, h)
        self.image = self.image.convert_alpha()
        self.parent_rect = self.rect.midtop
        self.rect =  pygame.rect.Rect((0, 0), (self.width, 10))
        self.rect.midbottom = self.parent_rect
class down_platforms(Platform):
    def __init__(self, image, x, y, w, h):
        super().__init__(image, x, y, w, h)
        self.parent_rect = self.rect.midbottom
        self.image = self.image.convert_alpha()
        self.rect =  pygame.rect.Rect((0, 0), (self.width/10*6, 5))
        self.rect.midbottom = self.parent_rect
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

def platform_door(cat, dimension, door_image):
        platform_list = dimension.platforms_list
        platform_param = dimension.platform_param
        door_list = dimension.door_list
        door_dimension = dimension.door_dimension
        doors = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        platforms_up = pygame.sprite.Group()
        platforms_down = pygame.sprite.Group()
        counter = 0
        for i, d, p in zip(platform_list, door_list, platform_param):
            platforms.add(Platform(dimension.image_platform, i[0], i[1], p[0], p[1]))
            platforms_up.add(up_platforms(dimension.image_platform, i[0], i[1],p[0], p[1]))
            platforms_down.add(down_platforms(dimension.image_platform, i[0], i[1],p[0], p[1]))
            if d==1:
                doors.add(Door(door_image, Platform(dimension.image_platform, i[0], i[1],p[0], p[1]).rect.midtop, door_dimension[counter]))
                counter+=1  
        hits_up = pygame.sprite.spritecollide(cat, platforms_up, False)
        if hits_up:
            cat.y = hits_up[0].rect.top +1 - 60
            cat.collision_up = True
        else:
            cat.collision_up = False
        hits_down = pygame.sprite.spritecollide(cat, platforms_down, False)
        if hits_down:
            cat.y = hits_down[0].rect.bottom +1
            cat.collision_down = True
        else:
            cat.collision_down = False
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
        doors, platforms = platform_door(self.cat, void(self.screen), self.door_image)
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
        self.collision_list = pygame.sprite.Group()
        for i in platforms:
            self.collision_list.add(i)
        self.cat.update('horizontal', self.collision_list)
        self.cat.update('vertical', self.collision_list)
        print(self.cat.x)
        print(self.cat.y)
        print(self.cat.image)
        self.screen.blit(self.cat.image, (self.cat.x, self.cat.y))
        doors.draw(self.screen)
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
        doors, platforms = platform_door(self.cat, forest(self.screen), self.door_image)
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
        self.npc.update()
        self.cat.update(self.screen,'horizontal', self.collision_list)
        # self.cat.update(self.screen,'vertical', self.collision_list)
        self.screen.blit(self.cat.image, (self.cat.x, self.cat.y))
        self.collision_list.add(self.cat)
        # self.object.update('horizontal')
        self.object.update('vertical')
        self.screen.blit(self.object.image, (self.object.x, self.object.y))
        doors.draw(self.screen)
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
        doors, platforms = platform_door(self.cat, sun(self.screen), self.door_image)
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
    


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        global JUMP_NUMBER
        pygame.sprite.Sprite.__init__(self)
        self.x = 200
        self.image = pygame.transform.scale(pygame.image.load('cat_right1.png'), (100, 80))
        self.image = pygame.image.load('cat_right1.png')
        self.y = MIN_POSITION
        # self.rect = pygame.Rect((0,0),(100,80))
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.player_speed = 30
        self.jump = False
        self.jump_number = JUMP_NUMBER
        self.gravity = 10
        self.collision_up = False
        self.collision_down = False
        self.left = False
        self.right = True
        self.jump_count = JUMP_NUMBER
        self.player_animation = 0
        self.height = 60
        self.old_rect = self.rect
        self.gravity_num = 1
    def update(self, direction, collision_list):
        self.old_rect = self.rect.copy()
        self.gravity_num+=0.5
        walk_left = [pygame.transform.scale(pygame.image.load('cat_left1.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_left2.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_left3.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_left4.png'), (100, 80))] 
        walk_right = [pygame.transform.scale(pygame.image.load('cat_right1.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_right2.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_right3.png'), (100, 80)), pygame.transform.scale(pygame.image.load('cat_right4.png'), (100, 80))]
        keys = pygame.key.get_pressed()
        self.gravity = 10
        if keys[pygame.K_SPACE]:
            if not self.jump:
                self.jump = True
        if self.collision_up:
            self.gravity = 0
            self.gravity_num = 0
        if self.jump:
            if self.collision_down:
                self.jump_number = self.y - 490
                self.jump_count = 0
                self.gravity = 10 
            else:
                self.gravity = 0
                self.gravity_num = 0
            if self.jump_count>=self.jump_number*-1 and ((self.y<490) or (self.jump_count>=0)):
                if self.jump_count>=0 and not self.collision_down:
                    self.y-=(self.jump_count**2)/2
                    if self.right:
                        self.image = pygame.transform.scale(pygame.image.load('cat_right_up.png'), (100, 80))
                    elif self.left:
                        self.image = pygame.transform.scale(pygame.image.load('cat_left_up.png'), (100, 80))
                elif (not self.collision_up) and (self.jump_count<0):
                    self.y+=(self.jump_count**2)/2
                    if self.right:
                        self.image = pygame.transform.scale(pygame.image.load('cat_right_down.png'), (100, 80))
                    elif self.left:
                        self.image = pygame.transform.scale(pygame.image.load('cat_left_down.png'), (100, 80))
                else:
                    self.jump_count = JUMP_NUMBER
                    self.jump = False
                    self.jump_number = JUMP_NUMBER
                self.jump_count-=1

                
            else:
                if self.y<490:
                    self.jump_number = (self.jump_count-(490-self.y))*-1
                else:
                    self.jump_count = JUMP_NUMBER
                    self.jump = False
                    self.jump_number = JUMP_NUMBER

        if keys[pygame.K_LEFT]:
            if self.x>30:
                self.x -= self.player_speed
            self.left = True
            self.right = False
            if not self.jump:
                self.image = walk_left[self.player_animation]
        elif keys[pygame.K_RIGHT]:
            if self.x<870:
                self.x +=self.player_speed
            self.left = False
            self.right = True
            if not self.jump:
                self.image = walk_right[self.player_animation]
        elif not sum([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_SPACE]]) and not self.jump:
            if self.left:
                self.image = walk_left[0]
            elif self.right:
                self.image = walk_right[0]
        self.y+=self.gravity*self.gravity_num
        if self.y>=MIN_POSITION:
            self.gravity = 0
            self.gravity_num = 0
            self.y = MIN_POSITION
        
        self.player_animation = (self.player_animation+1)%4
        self.rect = self.image.get_rect().move(self.x, self.y)
        

        
class Object():
    def __init__(self, image, x_start, y_start, screen, collision_list):
        self.x = x_start
        self.y = y_start
        self.screen = screen
        self.collision_list = collision_list
        self.gravity_num = 1
        self.gravity = 10
        self.image = image
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.old_rect = self.rect
    def update(self, direction):
        self.old_rect = self.rect.copy()
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.gravity_num+=0.5
        if self.y<=490:
            self.y = self.y +self.gravity
        if self.y>=MIN_POSITION:
            self.gravity = 0
            self.gravity_num = 0
            self.y = MIN_POSITION
        self.y+=self.gravity*self.gravity_num
        collide = self.rect.colliderect(self.cat.rect)
        keys = pygame.key.get_pressed()
        if collide:
            print('Object!')
            if keys[pygame.K_RIGHT]:
                self.x = self.cat.rect.right +50
            elif keys[pygame.K_LEFT]:
                self.x = self.cat.rect.left - 50

        if self.collision_up:
            self.gravity = 0
            self.gravity_num = 0
        if self.collision_down:
            self.jump_number = self.y - 490
            self.jump_count = 0
            self.gravity = 10 
       


class Npc(pygame.sprite.Sprite):
    def __init__(self, npc_animation, x, y, screen, quest, object):
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
        self.buble = pygame.transform.scale(pygame.image.load('npc_dialog.png'), (50, 40))
        self.buble_animation = False
        self.buble_timer = 0
        self.cadr = 0
    def update(self):
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
            pygame.Surface.blit(self.object, self.screen, (self.buble.get_rect().left + 5, self.buble.get_rect().top + 5))
            self.screen.blit(self.object, self.buble.get_rect().move(self.rect.left + 6, self.rect.top -38))
        else:
            self.buble_animation = False
        point = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(point)
        pygame.draw.rect(self.screen, (30, 144, 23, 255), self.npc.rect)
        if collide and self.quest and pygame.mouse.get_pressed()[0]:
            # animation
            print('animation')
        elif collide and pygame.mouse.get_pressed()[0]:
            self.buble_animation  =True
            self.buble_timer = time.process_time()



    

