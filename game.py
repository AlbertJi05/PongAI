import pygame
import time
from collections import namedtuple
from enum import Enum
import random
import numpy as np

# reset
# reward
# play(action) -> direction
# game_iteration
# is_collision

pygame.init()
font = pygame.font.Font('super_waffles/Super Waffles.ttf', size=40)

BLOCK_HEIGHT = 80
BLOCK_WIDTH = 15
PONG_VELOCITY = 5

FPS = 60

DISPLAY_HEIGHT = 640
DISPLAY_WIDTH = 640
DISPLAY_BUFFER = 5

BALL_SIZE = 15
BALL_X_VELOCITY = 3
BALL_Y_VELOCITY = 1

class Direction(Enum):
    UP = 1
    DOWN = 0
    STOP = -1

INIT_LX = 15
INIT_RX = (DISPLAY_WIDTH - INIT_LX*2)
INIT_Y = (DISPLAY_HEIGHT/2) - (BLOCK_HEIGHT/2)




class PongAI:
    def __init__(self, w=DISPLAY_WIDTH, h=DISPLAY_HEIGHT):
        # init display
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.game_speed = 1
        self.reset()
        
    def reset(self):
        # init game state
        self.score_left = 0
        self.score_right = 0
        self.frame_iteration = 0
        
        # init pong
        self.l_direction = Direction.STOP
        self.r_direction = Direction.STOP
        self.left_pong = pygame.Rect(INIT_LX, INIT_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.right_pong = pygame.Rect(INIT_RX, INIT_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.pong_velocity = PONG_VELOCITY * self.game_speed    
    
        
        # init ball
        self.ball = pygame.Rect(DISPLAY_WIDTH/2-BALL_SIZE, DISPLAY_HEIGHT/2-BALL_SIZE, BALL_SIZE, BALL_SIZE)
        self.ball_x_velocity = random.choice([BALL_X_VELOCITY, -BALL_X_VELOCITY]) * self.game_speed
        self.ball_y_velocity = None
        self._intialize_ball()


        
    def play_step(self, action):
        self.frame_iteration += 1
        
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.l_direction = Direction.UP
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.l_direction = Direction.DOWN
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.l_direction = Direction.STOP
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.l_direction = Direction.STOP
                if event.key == pygame.K_t:
                    self.game_speed = 2
                if event.key == pygame.K_r:
                    self.game_speed = 1

        # move objects
        self._move_left_pong()
        self._move_right_pong(action)
        self._move_ball()
        
        # check collision
        collide = self.get_wall_collision()
        pong_collide = self.get_pong_collision()
        
        reward = 0
        game_over = False    
        # check if game over
        if collide or self.frame_iteration > max(1000, 1000*self.score_right):
            reward = -10
            # time.sleep(0.1)            
            game_over = True
            return reward, game_over, self.score_right

        # check reward for pong
        if pong_collide:
            reward = 20
            
        # update game
        self._update_ui()
        self.clock.tick(FPS) # clock tick needs to be after the screen.flip()
        
        return reward, game_over, self.score_right
                
    def _update_ui(self):
        self.display.fill((0, 0, 0))
        
        score = font.render(f"{self.score_left}             {self.score_right}", True, (255, 255, 255))
        
        pygame.draw.rect(self.display, (255, 255, 255), self.left_pong)
        pygame.draw.rect(self.display, (255, 255, 255), self.right_pong)
        pygame.draw.rect(self.display, (255, 255, 255), self.ball)
        
        self.display.blit(score, (DISPLAY_WIDTH/2 - score.get_width() + 70, 70))
        
        pygame.display.flip()
        
    def _update_time(self):
        # TODO fix delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now
    
        return dt
    
    def _move_left_pong(self):
        # move left pong
        if self.l_direction == Direction.UP:
            self.left_pong.y -= self.pong_velocity
        elif self.l_direction == Direction.DOWN:
            self.left_pong.y += self.pong_velocity
        elif self.l_direction == Direction.STOP:
            self.left_pong.y += 0
            
    def _move_right_pong(self, action):
        # [up, stop, down]
        
        if np.array_equal(action, [0, 1, 0]):
            self.r_direction = Direction.STOP
        elif np.array_equal(action, (1, 0, 0)):
            self.r_direction = Direction.UP
        else:
            self.r_direction = Direction.DOWN
        
        if self.r_direction == Direction.UP:
            self.right_pong.y -= self.pong_velocity
        elif self.r_direction == Direction.DOWN:
            self.right_pong.y += self.pong_velocity
        elif self.r_direction == Direction.STOP:
            self.right_pong.y += 0
            
            
            
    def get_wall_collision(self):
        # left pong direction
        if self.left_pong.y < DISPLAY_BUFFER:
            self.l_direction = Direction.STOP
        if (self.left_pong.y + BLOCK_HEIGHT + DISPLAY_BUFFER) > DISPLAY_HEIGHT:
            self.l_direction = Direction.STOP
        
        # right pong direction
        if self.right_pong.y < DISPLAY_BUFFER:
            self.r_direction = Direction.STOP
        if (self.right_pong.y + BLOCK_HEIGHT + DISPLAY_BUFFER) > DISPLAY_HEIGHT:
            self.r_direction = Direction.STOP
        
        
        
        
        if self.ball.x > (DISPLAY_WIDTH - BALL_SIZE):
            self.ball.x = DISPLAY_WIDTH/2-BALL_SIZE
            self.ball_x_velocity *= -1
            self._intialize_ball()
            return True
        
        if self.ball.x < 0:
            # self.ball.x = DISPLAY_WIDTH/2-BALL_SIZE
            self.ball_x_velocity *= -1
            # self._intialize_ball()
        
            
        if self.ball.y < 0:
            self.ball_y_velocity *= -1
        if self.ball.y > (DISPLAY_HEIGHT - BALL_SIZE):
            self.ball_y_velocity *= -1
        
        
    def get_pong_collision(self):
        # detect left pong
        l_collision = self.ball.colliderect(self.left_pong)
        if l_collision:
            self.ball_x_velocity *= -1
            self.ball.x + 10
            self.score_left += 1
        r_collision = self.ball.colliderect(self.right_pong)
        if r_collision:
            self.ball_x_velocity *= -1
            self.ball.x = self.right_pong.x - BLOCK_WIDTH - 10
            self.score_right += 1
            return True       

            
    def _move_ball(self):
        self.ball.x -= self.ball_x_velocity
        self.ball.y += self.ball_y_velocity
    
    def _intialize_ball(self):
        y = random.choice([BALL_Y_VELOCITY, -BALL_Y_VELOCITY])
        self.ball_y_velocity = y
        
            
    
    
# if __name__ == '__main__':
#     game = Pong()
#     game_over = False
    
#     while not game_over:
#         scores, game_over = game.play_step()
        
#     print("Final score:", scores[0])
        
#     pygame.quit()
        
    
    