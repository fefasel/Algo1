import time
import sys
import os

import pygame

# Import game object classes
from level import Level
from player import Player
from apple import Apple

# Import constant definitions
from macros import *

# Import agents
from agent import Agent


class Game:
    def __init__(self, game_window_name="Pyna Blaster v0.001"):
        # Initialize pygame stuff
        pygame.display.init()
        pygame.mixer.init()
        pygame.display.set_caption(game_window_name)
        self.screen = pygame.display.set_mode(game_window_size)
        self.clock = pygame.time.Clock()

        self.agent_moving = False
        self.player_current_frame_index = 0
        # wall_width = self.wall.get_width()
        wall_width = 16

        ASSET_PATH = os.path.dirname(os.path.abspath(__file__)) + '/images/Bomberman/'
        # Load images
        self.wall = pygame.transform.scale(
            pygame.image.load(ASSET_PATH + 'Blocks/indestructable.png').convert(),
            (wall_width, wall_width))
        self.breakable_wall = pygame.transform.scale(
            pygame.image.load(ASSET_PATH + 'Blocks/destructable1.png').convert(),
            (wall_width, wall_width))
        self.door = pygame.transform.scale(
            pygame.image.load(ASSET_PATH + 'Blocks/door.png').convert(),
            (wall_width, wall_width))
        self.bomb = [
            pygame.transform.scale(
                pygame.image.load(ASSET_PATH + 'Bomb/idle2.png').convert_alpha(),
                (wall_width, wall_width)),
            pygame.transform.scale(
                pygame.image.load(ASSET_PATH + 'Bomb/idle3.png').convert_alpha(),
                (wall_width, wall_width)),
            pygame.transform.scale(
                pygame.image.load(ASSET_PATH + 'Bomb/explosion_center3.png').convert_alpha(),
                (wall_width, wall_width))
        ]
        self.floor = pygame.transform.scale(
            pygame.image.load(ASSET_PATH + 'Blocks/floor.png').convert(),
            (wall_width, wall_width))

        PLAYER_IMAGE_PATH = ASSET_PATH + 'Agent/move'
        self.player_left = [
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '1.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '2.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '3.png').convert_alpha(), (wall_width, wall_width)),
        ]
        self.player_down = [
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '4.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '5.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '6.png').convert_alpha(), (wall_width, wall_width)),
        ]
        self.player_right = [
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '7.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '8.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '9.png').convert_alpha(), (wall_width, wall_width)),
        ]
        self.player_up = [
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '10.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '11.png').convert_alpha(), (wall_width, wall_width)),
            pygame.transform.scale(pygame.image.load(PLAYER_IMAGE_PATH + '12.png').convert_alpha(), (wall_width, wall_width)),
        ]

        self.player_image = self.player_left[self.player_current_frame_index]
        self.player_images = [self.player_right, self.player_up, self.player_left, self.player_down]

        #  load sounds
        self.win_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/tada.wav')
        self.lose_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/fail_trombone_4s.wav')

        # Dictionary to map images to characters in level matrix
        self.images = {
            'W': self.wall,
            'B': self.breakable_wall,
            'F': self.floor,
            'P': self.player_image,
            'D': self.door
        }

        self.current_level = None
        self.current_level_number = 0

        # Player object
        self.player = None
        self.game_finished = False
        self.player_alive = True

        """
        Current level statistics
        """
        #  number of all apples in the initial level configuration
        self.total_apple_count = 0

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

    def print_images_for_matrix(self, level_matrix, box_size):
        for r in range(0, len(level_matrix)):
            for c in range(0, len(level_matrix[r])):
                if level_matrix[r][c] == 'P':
                    self.screen.blit(self.images['F'], (c * box_size, r * box_size))
                self.screen.blit(self.images[level_matrix[r][c]], (c * box_size, r * box_size))


    def draw_level(self, level_matrix):
        # Get image size to print on screen
        box_size = self.wall.get_width()
        self.images["P"] = self.player_images[self.player.current_facing_index][self.player_current_frame_index]
        #self.player_current_frame_index = (self.player_current_frame_index + 1) % 3

        # Print images for matrix
        self.print_images_for_matrix(level_matrix, box_size)
        pygame.display.update()

    def draw_level_search(self, level_matrix, direction):
        # Get image size to print on screen
        box_size = self.wall.get_width()

        if direction != "X":
            drs = ["R", "U", "L", "D"]
            self.images["P"] = self.player_images[drs.index(direction)][self.player_current_frame_index]

        # Print images for matrix
        self.print_images_for_matrix(level_matrix, box_size)
        pygame.display.update()

    def init_level(self, level):
        self.current_level = Level(level)

        # mark game as not finished
        self.game_finished = False
        self.player_alive = True

        # number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  create player object
        player_pos = self.current_level.get_player_pos()
        player_current_row = player_pos[0]
        player_current_col = player_pos[1]
        self.player = Player(player_current_row, player_current_col)
        self.goal = self.current_level.get_goal_pos()

    """
    def plant(self, render=True):
        pm0 = self.player.movement_history[-1]
        pm1 = self.player.movement_history[-2]
        moves = []
        def move_inverter(pm):
            if pm == 'L':
                return 'R'
            elif pm == 'R':
                return 'L'
            elif pm == 'U':
                return 'D'
            elif pm == 'D':
                return 'U'

        moves.append(move_inverter(pm0))
        moves.append(move_inverter(pm1))
        moves.append("PASS")
        moves.append(pm1)
        moves.append(pm0)

        bomb_location = self.player.current_pos
        r = bomb_location[0]
        c = bomb_location[1]
        i = 0
        for move in moves:
            self.step(move, render)
            box_size = self.wall.get_width()
            if i < 3:
                self.screen.blit(self.bomb[i], (c * box_size, r * box_size))
                i += 1
                pygame.display.update()
            time.sleep(0.2)
    """

    def step(self, player_direction, render=True):
        matrix = self.current_level.get_matrix()
        self.current_level.save_history(matrix)

        player_current_pos = self.player.get_pos()
        player_current_row = player_current_pos[0]
        player_current_col = player_current_pos[1]

        #  calculate new position of the player
        player_next_pos = self.player.move(player_direction)
        player_next_row = player_next_pos[0]
        player_next_col = player_next_pos[1]

        # Resolve static collisions for player
        next_cell = matrix[player_next_row][player_next_col]
        if next_cell == "F":
            # Next cell is floor
            pass
        elif next_cell == "W" or next_cell == "B":
            # Next cell is wall or breakable wall
            # Player cant pass here
            self.player.current_pos = self.player.prev_pos
        else:
            pass

        # Update game matrix
        level_matrix = self.current_level.get_matrix()
      
        player_prev_row = self.player.get_prev_row()
        player_prev_col = self.player.get_prev_col()
        player_next_row = self.player.get_row()
        player_next_col = self.player.get_col()

        level_matrix[player_prev_row][player_prev_col] = "F"
        level_matrix[player_next_row][player_next_col] = "P"
        # Draw
        if render:
            self.draw_level(matrix)

        self.elapsed_time_step += 1

        if [player_next_row, player_next_col] == self.goal:
        #  check if game is finished
            return RESULT_PLAYER_WON
        else:
            return RESULT_GAME_CONTINUE

    # Function when a human player plays the game
    def start_level_human(self, level_index):
        self.init_level(level_index)
        self.draw_level(self.current_level.get_matrix())

        #  game loop
        while True:
            result = 0

            # Manual input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        result = self.step("R", render=True)
                    elif event.key == pygame.K_UP:
                        result = self.step("U", render=True)
                    elif event.key == pygame.K_LEFT:
                        result = self.step("L", render=True)
                    elif event.key == pygame.K_DOWN:
                        result = self.step("D", render=True)
                    #elif event.key == pygame.K_SPACE:
                    #    result = self.plant(render=True)
                    #elif event.key == pygame.K_u:
                    #    self.draw_level(self.current_level.undo())
                    elif event.key == pygame.K_r:
                        self.init_level(self.current_level_number)
                        result = RESULT_GAME_CONTINUE
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD:
                sound_channel = None
                if result == RESULT_PLAYER_WON:
                    #print("WON")
                    sound_channel = self.win_sound.play()
                else:
                    #print("LOSE")
                    sound_channel = self.lose_sound.play()

                #  wait for sound to end
                while sound_channel.get_busy() == True:
                    continue
                break
            else:
                pass

        return self.elapsed_time_step



    def start_level_computer(self, level_index, agent, 
                             render=False, play_sound=False,
                             max_episode_length=150,
                             test=False):
        self.init_level(level_index)

        if render:
            self.draw_level(self.current_level.get_matrix())

        #  let the agent think
        t1 = time.time()
        sequence = agent.solve(self.current_level.get_matrix(), self.current_level.get_goal_pos(),
                               self.player.get_row(), self.player.get_col())
        t2 = time.time()
        elapsed_solve_time = t2-t1
        print("Decided sequence:")
        print(sequence)
        print("{} decided sequence length:{}".format(agent.__class__.__name__, len(sequence)))
        
        result = None

        #  start playing the decided sequence
        for chosen_action in sequence:
            result = 0

            #  input source will use matrix to decide
            matrix = self.current_level.get_matrix()

            chosen_action = chosen_action  #sequence[self.elapsed_time_step]

            # Apply decided action
            result = self.step(chosen_action, render=render)

            # If we want to render our agent, wait some time
            if render:
                self.clock.tick(FPS)
                pygame.event.get()

            #  check if game finished
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                if (play_sound):
                    sound_channel = None
                    if (result == RESULT_PLAYER_WON):
                        sound_channel = self.win_sound.play()
                    else:
                        sound_channel = self.lose_sound.play()

                    #  wait for sound to end
                    while sound_channel.get_busy() == True:
                        continue
                break
            else:
                pass


            #  check if we reached episode length
            if (self.elapsed_time_step >= max_episode_length):
                break

        if result != RESULT_PLAYER_WON:
            #  must be lose case for this homework
            if (play_sound):
                sound_channel = None
                sound_channel = self.lose_sound.play()

                #  wait for sound to end
                while sound_channel.get_busy() == True:
                    continue

        return self.elapsed_time_step, elapsed_solve_time, result


    def convert_direction_to_vector(self, player_direction):
        if player_direction == 'L':
            return -1, 0
        elif player_direction == 'R':
            return 1, 0
        elif player_direction == 'U':
            return 0, -1
        elif player_direction == 'D':
            return 0, 1
