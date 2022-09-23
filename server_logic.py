#basic philosophy of snake: about this snake that his priority is to survive, when it sees other enemies keep a low profile and don't aproach them and when it sees food his survival instic is to go for it and the will keep growin to survive. 

import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_walls(data, possible_moves):
  if data['you']['head']['x'] == 0:
    possible_moves.remove('left')
  if data['you']['head']['x'] == data['board']['width']-1:
    possible_moves.remove('right')
  if data['you']['head']['y'] == 0:
    possible_moves.remove('down')
  if data['you']['head']['y'] == data['board']['height']-1:
    possible_moves.remove('up')
  return possible_moves

def SnakeSafe(data,x,y):
    for element1 in data['board']['hazards']:
        if element1 ['x'] == x and element1['y'] == y: 
            return False
    for element2 in data['board']['snakes']:
        for element3 in element2['body']:
            if element3['x'] == x and element3 ['y'] == y: 
                return False
    return True
   
def avoid_hazards(data,possible_moves):
  xh = data['you']['head']['x'] 
  yh = data['you']['head']['y'] 
  if SnakeSafe(data,xh+1,yh) == False:
    if 'right' in possible_moves:
      possible_moves.remove('right')

  if SnakeSafe(data,xh-1,yh) == False:
    if 'left' in possible_moves:
      possible_moves.remove('left')

  if SnakeSafe(data,xh,yh+1) == False:  
    if 'up' in possible_moves:
      possible_moves.remove('up')

  if SnakeSafe(data,xh,yh-1) == False: 
    if 'down' in possible_moves:
      possible_moves.remove('down')

  return possible_moves

def distance(x1,y1,x2,y2):
    return abs(x1 - x2) + abs(y1 - y2)

def shortcut(data):
    hx = data['you']['head']['x']
    hy = data['you']['head']['y']
    
    foods = data['board']['food']
    min_d = None
    x = 0 
    y = 0
    for food in foods:
        fx = food['x']
        fy = food['y']
        d = distance(hx,hy,fx,fy)
        if min_d == None or d < min_d:
            min_d = d
            x,y = fx,fy
       
    return x,y

def avoid_starvation(data, possible_moves):
  xh = data['you']['head']['x'] 
  yh = data['you']['head']['y']
  location = [] 
  sx,sy = shortcut(data)
  #current_healt = data['you']['health']

  if sx < xh:
    if 'left' in possible_moves:
      location.append('left')

  if sy < yh:
    if 'down' in possible_moves:
      location.append('down')

  if sx > xh:
    if 'right' in possible_moves:
      location.append('right')

  if sy > yh:
    if 'up' in possible_moves:
      location.append('up')

  if len(location) == 0:
    return possible_moves

  # print(location)

  return location



  # hungry = avoid_starvation(data,current_health, possible_moves)
  # if hungry == []:
  #   move = random.choice(possible_moves)

  # return move




# def dinner_time(data, my_head, possible_moves):
#   current_health = data['you']['health']
#   priority_moves = []

#   if current_health < 65:
#     try:
#       if my_head['x'] < data['board']['foof'][0]['x'] and 'right' in possible_moves:
#         priority_moves.append('rigth')

#       if my_head['x'] > data['board']['foof'][0]['x'] and 'left' in possible_moves:
#         priority_moves.append('left')

#       if my_head['y'] < data['board']['foof'][0]['y'] and 'down' in possible_moves:
#         priority_moves.append('down')

#       if my_head['y'] < data['board']['foof'][0]['y'] and 'up' in possible_moves:
#         priority_moves.append('up')
      
#     except:
#       return priority_moves
    
#     return priority_moves

#   when_hungry = dinner_time(data, my_head, possible_moves)
#   print('happens fourth')

#   print(possible_moves)
#   print(when_hungry)
#   print(data['you']['health'])

#   if when_hungry == []:
#     move = ramdom.choice(possible_moves)
#     print("f'went for a random, at turn:" {data["turn"]}\n)

def choose_move(data):
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    possible_moves = avoid_walls(data, possible_moves)
    possible_moves = avoid_hazards(data,possible_moves)
    possible_moves = avoid_starvation(data,possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    # board_height = ?
    # board_width = ?

    

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
