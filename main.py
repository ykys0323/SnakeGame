import pygame
import numpy as np
from pygame.locals import (    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,)

pygame.init()
import random



SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

my_radius = 10
available_space = []
for i in range(int(SCREEN_HEIGHT*SCREEN_WIDTH/((my_radius*2)*(my_radius*2)))):
    available_space.append(i)
# print(available_space)

M_LEFT = 1
M_RIGHT = 2
M_UP = 3
M_DOWN = 4


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Fill the background with white
screen.fill((255, 255, 255))
running = True



# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'

class Snake_Body(pygame.sprite.Sprite):
    def __init__(self,new_point):
        super(Snake_Body,self).__init__()
        self.radius = 10
        self.surf = pygame.Surface((self.radius*2-1,self.radius*2-1))
        self.surf.fill((128,128,128))
        self.rect = self.surf.get_rect()
        self.rect.center = new_point



class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food,self).__init__()
        self.radius = 10
        self.surf = pygame.Surface((self.radius*2,self.radius*2))
        self.surf.fill((0,0,255))
        self.rect = self.surf.get_rect()
        global running
        # self.rect.center = ((random.randint(0,SCREEN_WIDTH/(self.radius*2)-1)*(self.radius*2)+self.radius),(random.randint(0,SCREEN_HEIGHT/(self.radius*2)-1)*(self.radius*2)+self.radius))
        if len(available_space) > 0:
            random_index = random.randint(0,len(available_space)-1)
            self.rect.center = ((int(available_space[random_index]%int(SCREEN_WIDTH/20))*20+10),(int(available_space[random_index]/int(SCREEN_HEIGHT/20))*20+10))
            # print(random_index)
            # print(self.rect.center)
        else:
            running = False
            print("Game Over Because of you")
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super(Snake, self).__init__()
        self.radius = 10
        self.surf = pygame.Surface((self.radius*2,self.radius*2))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.rect.center = (self.rect.center[0]+20,self.rect.center[1])
        self.speed = self.radius*2
        self.direction = M_RIGHT
        self.new_body = False
        self.body_len = 1
        self.body_part = pygame.sprite.Group()
        self.body_part.add(Snake_Body((self.rect.center[0]-20,self.rect.center[1])))
        self.add_new_body_count = []
        self.require_step_count = []
        first_sprite = self.body_part.sprites()[0]
        available_space.remove(int((first_sprite.rect.center[0]-first_sprite.radius)/(first_sprite.radius*2))+int((first_sprite.rect.center[1]-first_sprite.radius)/(first_sprite.radius*2)*(SCREEN_WIDTH/(first_sprite.radius*2))))
        available_space.remove(int((self.rect.center[0]-self.radius)/(self.radius*2))+int((self.rect.center[1]-self.radius)/(self.radius*2)*(SCREEN_WIDTH/(self.radius*2))))
    def update_key(self,pressed_keys):
        # print(pressed_keys)
        if pressed_keys[K_UP]:
            if self.direction != M_DOWN:
                self.direction = M_UP
                return
        if pressed_keys[K_DOWN]:
            if self.direction != M_UP:
                self.direction = M_DOWN
                return
        if pressed_keys[K_LEFT]:
            if self.direction != M_RIGHT:
                self.direction = M_LEFT
                return
        if pressed_keys[K_RIGHT]:
            if self.direction != M_LEFT:
                self.direction = M_RIGHT
                return

    def update_movement(self):
        # print("Update Movement")
        if self.new_body == True:
            self.new_body = False
            self.add_new_body_count.append(0)
            self.body_len+=1
            # print(self.body_len)
            self.require_step_count.append(self.body_len-1)
            # print(self.add_new_body_count)
        if len(self.body_part) > 0:
            # print(len(self.body_part))
            self.body_part.add(Snake_Body(self.rect.center))
            first_sprite = self.body_part.sprites()[0]
            skip_remove = False
            if len(self.require_step_count) > 0:
                if self.add_new_body_count[0] == self.require_step_count[0]:
                    skip_remove = True
                    self.add_new_body_count.pop(0)
                    self.require_step_count.pop(0)
            if not skip_remove:
                available_space.append(int((first_sprite.rect.center[0]-first_sprite.radius)/(first_sprite.radius*2))+int((first_sprite.rect.center[1]-first_sprite.radius)/(first_sprite.radius*2)*(SCREEN_WIDTH/(first_sprite.radius*2))))
                # print(first_sprite.rect.center)
                self.body_part.remove(first_sprite)
        # for first_sprite in self.body_part:
        #     try:
        #         available_space.remove(int((first_sprite.rect.center[0]-first_sprite.radius)/(first_sprite.radius*2))+((first_sprite.rect.center[1]-first_sprite.radius)/(first_sprite.radius*2)*(SCREEN_WIDTH/(first_sprite.radius*2))))
        #     except:
        #         pass

                

        if self.direction == M_UP:
            self.rect.move_ip(0,-1*self.speed)
        if self.direction == M_DOWN:
            self.rect.move_ip(0,self.speed)
        if self.direction == M_RIGHT:
            self.rect.move_ip(self.speed,0)
        if self.direction == M_LEFT:
            self.rect.move_ip(-1*self.speed,0)

        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0

        # available_space.remove((self.rect.center[0]-10)/20+(self.rect.center[0]-10)/20)
        # print(f"remove x = {int((self.rect.center[0]-self.radius)/(self.radius*2))+int((self.rect.center[1]-self.radius)/(self.radius*2)*(SCREEN_WIDTH/(self.radius*2)))}")
        try:
            available_space.remove(int((self.rect.center[0]-self.radius)/(self.radius*2))+int((self.rect.center[1]-self.radius)/(self.radius*2)*(SCREEN_WIDTH/(self.radius*2))))
        except:
            pass
        # print(len(available_space))
        # print(len(self.body_part)+1)
        # print(available_space)
        # print(self.rect.center)
        for i in range(len(self.add_new_body_count)):
            self.add_new_body_count[i]+=1



clock = pygame.time.Clock()
snake = Snake()
food = Food()

snake_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()
snake_group.add(snake)
food_group.add(food)
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exit Loop")
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Escape")
                running = False

    pressed_keys = pygame.key.get_pressed()
    snake.update_key(pressed_keys)
    snake.update_movement()
    screen.fill((255,255,255))
    if pygame.sprite.collide_rect(snake,food):
        # food_group.kill()
        food = Food()
        snake.new_body = True
        # food_group.add(food)
    if len(snake_group) > 0:
        if pygame.sprite.spritecollideany(snake,snake.body_part):
            running = False
            print("GameOver")
    screen.blit(snake.surf,snake.rect)
    for body in snake.body_part:
        screen.blit(body.surf,body.rect)
    screen.blit(food.surf,food.rect)
    

    


    pygame.display.flip()
    clock.tick(10)

# Done! Time to quit.
pygame.quit()