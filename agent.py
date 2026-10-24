import torch
import random
import numpy as np
from collections import deque
from game import PongAI, Direction
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness 
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if full
        self.model = Linear_QNet(7, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
        
    def get_state(self, game):
        # state [ball x, ball up, ball down, move_up, move_stop, move_down, pong_y]
        ball_x = game.ball.x
        ball_y = game.ball.y
        
        pong_y = game.right_pong.y
        
        dir_u = game.r_direction == Direction.UP
        dir_s = game.r_direction == Direction.STOP
        dir_d = game.r_direction == Direction.DOWN

        state = [
            # ball position
            ball_x,
            ball_y > game.right_pong.y,
            ball_y < game.right_pong.y,
            
            # Move direction
            dir_u,
            dir_s,
            dir_d,
            
            # pong y
            pong_y
            ]
        
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEM is reached
                                                                      # return one tuple

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
        
        
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0] # up stop down
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_scores = 0
    record = 0
    agent = Agent()
    game = PongAI()
    while True:
        # get old state 
        state_old = agent.get_state(game)
        
        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state
        rewards, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        # train short memory
        agent.train_short_memory(state_old, final_move, rewards, state_new, done)
        
        # remember
        agent.remember(state_old, final_move, rewards, state_new, done)
        
        if done:
            # train long memory, plot results
            # (replay memory or experience replay)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                agent.model.save()
            
            print("Game", agent.n_games, "Score", score, "Record:", record)
            
            plot_scores.append(score)
            total_scores += score
            mean_score = total_scores / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            
if __name__ == '__main__':
    train()