import math, random, pygame, sys
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox

class cube(object):
  rows = 32
  w = 800
  def __init__(self, start, dircx=1, dircy=0, color=(255,0,0)):
    self.pos = start
    self.dircx = 1
    self.dircy = 0
    self.color = color

  def move(self, dircx, dircy):
    self.dircx = dircx
    self.dircy = dircy
    self.pos = (self.pos[0] + self.dircx, self.pos[1] + self.dircy)

  def draw(self, surface, eyes=False):
    d = self.w // self.rows
    row = self.pos[0]
    col = self.pos[1]
    # make sure we draw inside of white square
    pygame.draw.rect(surface, self.color, (row * d + 1, col * d + 1, d-2, d-2))
    if eyes:
      centre = d//2
      eyeRad = 2
      eye1 = (row * d + centre - eyeRad, col * d + 8)
      eye2 = (row * d + d - eyeRad * 2, col * d + 8)
      # draw 2 circles
      pygame.draw.circle(surface, (0,0,0), eye1, eyeRad)
      pygame.draw.circle(surface, (0,0,0), eye2, eyeRad)

# snake body
class snake(object):
  body = []
  turns = {}
  def __init__(self, color, pos):
    self.color = color
    self.head = cube(pos)
    self.body.append(self.head)
    self.dircx = 0
    self.dircy = 1

  def move(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
       pygame.quit()
      # gets keys when event pressed
      keys = pygame.key.get_pressed()

      for key in keys:
        if keys[pygame.K_LEFT]:
          # direction for going up
          self.dircx = -1
          self.dircy = 0
          # adds key curr pos of head and sets equal to dirc head turns
          self.turns[self.head.pos[:]] = [self.dircx, self.dircy]
        elif keys[pygame.K_RIGHT]:
          # direction for going up
          self.dircx = 1
          self.dircy = 0
          # adds key curr pos of head and sets equal to dirc head turns
          self.turns[self.head.pos[:]] = [self.dircx, self.dircy]
        elif keys[pygame.K_UP]:
          # direction for going up
          self.dircx = 0
          self.dircy = -1
          # adds key curr pos of head and sets equal to dirc head turns
          self.turns[self.head.pos[:]] = [self.dircx, self.dircy]
        elif keys[pygame.K_DOWN]:
          # direction for going up
          self.dircx = 0
          self.dircy = 1
          # adds key curr pos of head and sets equal to dirc head turns
          self.turns[self.head.pos[:]] = [self.dircx, self.dircy]
    # get index and cube from self.body
    for i, c in enumerate(self.body):
      # [:] just copies grab position of cube check if they are in turn list
      position = c.pos[:]
      if position in self.turns:
        turn = self.turns[position]
        c.move(turn[0], turn[1])
        # when the last cube you remove it from turn
        if i == len(self.body) - 1:
          self.turns.pop(position)
      else:
      # check if we have reached edge of grid
        # if we move right at head pos is less than zero change pos to right  
        if c.dircx == -1 and c.pos[0] <= 0:
          c.pos = (c.rows - 1, c.pos[1])
        elif c.dircx == 1 and c.pos[0] >= c.rows - 1:
          c.pos = (0, c.pos[1])
        elif c.dircy == 1 and c.pos[1] >= c.rows - 1:
          c.pos = (c.pos[0], 0)
        elif c.dircy == -1 and c.pos[1] >= c.rows - 1:
          c.pos = (c.pos[0], c.rows-1)
        else: c.move(c.dircx, c.dircy)

  def reset(self, pos):
    pass

  def addCube(self):
    pass

  def draw(self, surface):
    for i, c in enumerate(self.body):
      if i == 0:
        c.draw(surface,True)
      else:
        c.draw(surface)

def drawGrid(w, rows, surfaceArea):
  # make sure there is no large decimal numbers
  sizeBetween = w // rows

  x = 0
  y = 0
  for l in range(rows):
    x += sizeBetween
    y += sizeBetween
    #draws 2 lines in for loop to create grid
    pygame.draw.line(surfaceArea, (255, 255, 255), (x,0), (x,w))
    pygame.draw.line(surfaceArea, (255, 255, 255), (0,y), (w,y))

def redrawWindow(surfaceArea):
  # make variables accessible globally
  global rows, width, height, s
  surfaceArea.fill((0,0,0))
  s.draw(surfaceArea)
  drawGrid(width, rows, surfaceArea)
  pygame.display.update()

def randSnack(rows, snake):
  positions = snake.body
  while True:
    # this makes sure that the snack doesnt go on the snake
    x = random.randrange(rows)
    y = random.randrange(rows)
    if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
      continue
    else:
      break
  return (x, y)

def main(): 
  global width, height, rows, s
  width = 500
  height = 500
  rows = 20
  win = pygame.display.set_mode((width, height))

  s = snake((255, 0, 0), (10,10))
  snack = cube(randSnack(rows, s))
  flag = True
  # makes the game frame rate run lower
  clock = pygame.time.Clock()

  while flag:
    pygame.time.delay(50)
    clock.tick(10)
    s.move()
    redrawWindow(win)


    pass

main()