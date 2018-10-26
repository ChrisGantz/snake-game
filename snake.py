import math, random, pygame, sys
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 32
    w = 800
    def __init__(self, start, dircx=1, dircy=0, color=(255,0,0)):
        self.pos = start
        self.dircx = dircx
        self.dircy = dircy
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
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dircx = 0
        self.dircy = 1

    def addTail(self):
        tail = self.body[-1]
        dx, dy = tail.dircx, tail.dircy
        # add a cube to the tail in any directions its moving
        if dx == 1 and dy == 0:
          self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
          self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
          self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
          self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
        # keep them moving in same direction as head
        self.body[-1].dircx = dx
        self.body[-1].dircy = dy

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
    global rows, width, height, s, snack
    surfaceArea.fill((0,0,0))
    s.draw(surfaceArea)
    snack.draw(surfaceArea)
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

# def obstacles(surfaceArea):
#     pygame.draw.rect(surfaceArea, (255, 0, 0), (100, 50, 50, 50))
#     pygame.display.update()

def show_message(subject, content):
  root = tk.Tk()
  root.attributes("-topmost", True)
  root.withdraw()
  messagebox.showinfo(subject,content)
  try:
    root.destroy()
  except:
    pass

def main():
    global width, height, rows, s, snack
    width = 800
    height = 800
    rows = 32
    win = pygame.display.set_mode((width, height))

    # obstacles(win)

    s = snake((255,255,0), (10,10))
    snack = cube(randSnack(rows, s), color=(255,0,255))
    flag = True
    # makes the game frame rate run lower
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(15)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addTail()
            snack = cube(randSnack(rows, s), color=(255, 0, 255)) ### I AM HERE

        for i in range(len(s.body)):
          if s.body[i].pos in list(map(lambda z:z.pos, s.body[i+1:])):
            print('Your max length', len(s.body))
            show_message('You lose', 'TRY AGAIN!')
            # if you crash reset
            s.reset((10, 10))
            break

        redrawWindow(win)

        pass

main()