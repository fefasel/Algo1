import time
import random
from copy import deepcopy
from agent import Agent

#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque

"""
  you may use the following Node class
  modify it if needed, or create your own
"""


class Node():

    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir


class DFSAgent(Agent):

    def __init__(self):
        super().__init__()

    def solve(self, level_matrix, goal, player_row, player_column):
        super().solve(level_matrix, goal, player_row, player_column)
        move_sequence = []

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """


        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence