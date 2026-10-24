import pygame
import time
from collections import namedtuple
from enum import Enum
import random

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

X = 15
Y = (DISPLAY_HEIGHT/2) - (BLOCK_HEIGHT/2)

class Pong:
    def __init__(self, w=DISPLAY_WIDTH, h=DISPLAY_HEIGHT):
        # init display
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        
        # init game state
        self.score_left = 0
        self.score_right = 0
        
        # init pong
        self.direction = Direction.STOP
        self.left_pong = pygame.Rect(X, Y, BLOCK_WIDTH, BLOCK_HEIGHT)
        
        # init ball
        self.ball = pygame.Rect(DISPLAY_WIDTH/2-BALL_SIZE, DISPLAY_HEIGHT/2-BALL_SIZE, BALL_SIZE, BALL_SIZE)
        self.ball_x_velocity = random.choice([BALL_X_VELOCITY, -BALL_X_VELOCITY])
        self.ball_y_velocity = None
        self._intialize_ball()

        
    def play_step(self):
        
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.direction = Direction.UP
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.direction = Direction.STOP
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.direction = Direction.STOP
                

        # move objects
        self._move_pong()
        self._move_ball()
        
        # check collision
        self._get_wall_collision()
        self._get_pong_collision()
        
        game_over = False    
        # check if game over
        if self.score_left >= 5:
            game_over = True
            
        # update game
        self._update_ui()
        self.clock.tick(FPS) # clock tick needs to be after the screen.flip()
        
        return (self.score_left, self.score_right), game_over
                
    def _update_ui(self):
        self.display.fill((0, 0, 0))
        
        score = font.render(f"{self.score_left}             {self.score_right}", True, (255, 255, 255))
        
        pygame.draw.rect(self.display, (255, 255, 255), self.left_pong)
        pygame.draw.rect(self.display, (255, 255, 255), self.ball)
        
        self.display.blit(score, (DISPLAY_WIDTH/2 - score.get_width() + 70, 70))
        
        pygame.display.flip()
        
    def _update_time(self):
        # TODO fix delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now
    
        return dt
    
    def _move_pong(self):
        if self.direction == Direction.UP:
            self.left_pong.y -= PONG_VELOCITY
        if self.direction == Direction.DOWN:
            self.left_pong.y += PONG_VELOCITY
        if self.direction == Direction.STOP:
            self.left_pong.y += 0
            
    def _get_wall_collision(self):
        # pong direction
        if self.left_pong.y < DISPLAY_BUFFER:
            self.direction = Direction.STOP
        if (self.left_pong.y + BLOCK_HEIGHT + DISPLAY_BUFFER) > DISPLAY_HEIGHT:
            self.direction = Direction.STOP
        
        
        # ball direction
        if self.ball.x > (DISPLAY_WIDTH - BALL_SIZE):
            self.ball_x_velocity *= -1
        if self.ball.x < 0:
            self.ball.x = DISPLAY_WIDTH/2-BALL_SIZE
            self.ball_x_velocity *= -1
            self._intialize_ball()
            
        if self.ball.y < 0:
            self.ball_y_velocity *= -1
        if self.ball.y > (DISPLAY_HEIGHT - BALL_SIZE):
            self.ball_y_velocity *= -1
        
        
    def _get_pong_collision(self):
        collision = self.ball.colliderect(self.left_pong)
        if collision:
            self.ball_x_velocity *= -1
            self.score_left += 1
            
    def _move_ball(self):
        self.ball.x -= self.ball_x_velocity
        self.ball.y += self.ball_y_velocity
    
    def _intialize_ball(self):
        y = random.choice([BALL_Y_VELOCITY, -BALL_Y_VELOCITY])
        self.ball_y_velocity = y
        
            
    
    
if __name__ == '__main__':
    game = Pong()
    game_over = False
    
    while not game_over:
        scores, game_over = game.play_step()
        
    print("Final score:", scores[0])
        
    pygame.quit()
        
    
    