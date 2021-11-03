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

    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, h_value):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        self.h = h_value

    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h

        """
            There are different strategies you can choose for
        tie breaking, that is, which node to choose when two
        nodes have equal f (g+h) values. Some of these are:

        1- Choose the node with lower h value, implying that you
        trust your heuristic more than g.

        2- Choose the node with lower g value, implying that you
        do not trust your heuristic function that much.

        3- Choose the node which is put into the
        queue earlier/later

        4- Use a secondary heuristic function to compare two 
        nodes when they have equal f value

        5- Select one of the nodes randomly. Not good for this
        assignment, but if you are making a game this also has
        an effect that makes your agent follow different routes
        each time it runs (if there are more than 1 shortest path
        to goal)

        ...
        ...
        ... 
        """


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class AStarAgent(Agent):

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