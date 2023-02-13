import json5
import pgzrun
import time, datetime
class Sokoban_Settings:
    def __init__(self):
        self.maps = [[['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', ' ', 'p', ' ', ' ', ' ', ' ', ' ', 'w'],
                      ['w', ' ', ' ', ' ', ' ', 'b', 'b', ' ', 'w'],
                      ['w', ' ', ' ', 'w', ' ', 'b', ' ', ' ', 'w'],
                      ['w', 'a', 'a', 'w', ' ', 'b', ' ', ' ', 'w'],
                      ['w', 'a', 'a', 'w', ' ', ' ', ' ', ' ', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']],
                     [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', 'a', 'a', 'a', 'a', ' ', ' ', ' ', 'w'],
                      ['w', 'w', 'w', 'w', ' ', 'b', 'w', ' ', 'w'],
                      ['w', ' ', ' ', ' ', 'b', ' ', ' ', ' ', 'w'],
                      ['w', ' ', ' ', 'w', 'b', 'b', ' ', ' ', 'w'],
                      ['w', ' ', 'p', ' ', ' ', ' ', 'w', ' ', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']],
                     [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', ' ', ' ', 'a', 'a', 'a', 'a', 'a', 'w'],
                      ['w', ' ', 'w', ' ', ' ', 'b', 'w', ' ', 'w'],
                      ['w', ' ', 'w', ' ', 'b', ' ', 'w', ' ', 'w'],
                      ['w', ' ', ' ', 'b', 'b', ' ', 'b', ' ', 'w'],
                      ['w', 'p', ' ', ' ', ' ', ' ', ' ', 'w', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']],
                     [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', ' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'],
                      ['w', ' ', ' ', 'a', 'b', 'a', ' ', 'w', 'w'],
                      ['w', 'p', 'w', 'b', 'b', 'b', 'a', 'w', 'w'],
                      ['w', ' ', 'w', 'a', 'b', 'a', ' ', 'w', 'w'],
                      ['w', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]
                     ]
        self.map_height = len(self.maps[0])*70
        self.map_width = len(self.maps[0][0])*70
        self.colour = (0, 255, 0)
        self.number_to_win = [4, 4, 5, 5]

sets = Sokoban_Settings()
my_map = sets.maps[0]

WIDTH = sets.map_width
HEIGHT = sets.map_height
GREEN = sets.colour

boy = Actor('smallboy.png')
level = 1
direction_y = 0
direction_x = 0
steps = 0
finished = 0
fake_finished = 0
session = {}
seconds = 0

walls = []
boxes = []
aims = []

def clear_field(new_map):
    global steps, finished, my_map
    steps = 0
    finished = 0
    boxes.clear()
    walls.clear()
    aims.clear()
    my_map = new_map
    drawings()

def drawText():
    screen.draw.text("Step {}".format(steps), (35, 35))
    screen.draw.text("Crosses closed: {}".format(finished), (WIDTH-210, 35))
    screen.draw.text("Level: {}".format(level), (WIDTH/2, 35))

def drawings():
    f = 0
    for work in my_map:
        i = 0
        for cursor in work:
            if cursor == 'w':
                walls.append(Actor('texturework.png'))
                walls[-1].x = 35 + (70*i)
                walls[-1].y = 35 + (70*f)
            elif cursor == 'b':
                boxes.append(Actor('box.png'))
                boxes[-1].x = 35 + (70*i)
                boxes[-1].y = 35 + (70*f)
            elif cursor == 'p':
                boy.x = 35 + (70*i)
                boy.y = 35 + (70*f)
            elif cursor == 'a':
                aims.append(Actor('crest.jpg'))
                aims[-1].x = 35 + (70 * i)
                aims[-1].y = 35 + (70 * f)
            i += 1
        f += 1
drawings()

def checking_collisions(x, y, lx, ly):
    global steps, finished, fake_finished
    checking_box = False
    for box in boxes:
        if boy.colliderect(box):
            for bax in boxes:
                if bax.x == box.x + x and bax.y == box.y + y:
                    checking_box = True
            if not checking_box:
                boy.x = box.x
                boy.y = box.y
                box.y += y
                box.x += x
            else:
                boy.x = lx
                boy.y = ly
            checking_box = False

        for aim in aims:
            if box.colliderect(aim):
                fake_finished += 1
    finished = fake_finished
    fake_finished = 0

    for wall in walls:
        if boy.colliderect(wall):
            boy.x = lx
            boy.y = ly
        for box in boxes:
            if box.colliderect(wall):
                boy.x = lx
                boy.y = ly
                box.x -= x
                box.y -= y
    steps += 1

def on_key_down(key):
    global steps, finished, my_map, level
    if key == keys.SPACE:
        clear_field(my_map)
    if key == keys.E:
        clear_field(sets.maps[2])
        level = 3
    if key == keys.W:
        clear_field(sets.maps[1])
        level = 2
    if key == keys.Q:
        clear_field(sets.maps[0])
        level = 1
    if key == keys.R:
        clear_field(sets.maps[3])
        level = 4

def update():
    global direction_y, direction_x
    last_x = boy.x
    last_y = boy.y
    if keyboard.up:
        time.sleep(0.25)
        direction_y = -70
        boy.y -= 70
        checking_collisions(direction_x, direction_y, last_x, last_y)
    elif keyboard.down:
        time.sleep(0.25)
        direction_y = 70
        boy.y += 70
        checking_collisions(direction_x, direction_y, last_x, last_y)
    elif keyboard.left:
        time.sleep(0.25)
        direction_x = -70
        boy.x -= 70
        checking_collisions(direction_x, direction_y, last_x, last_y)
    elif keyboard.right:
        time.sleep(0.25)
        direction_x = 70
        boy.x += 70
        checking_collisions(direction_x, direction_y, last_x, last_y)

    direction_x = 0
    direction_y = 0


def draw():
    global level, seconds
    screen.clear()
    screen.fill(GREEN)
    for aim in aims:
        aim.draw()
    boy.draw()
    for wall in walls:
        wall.draw()
    for box in boxes:
        box.draw()
    if finished == sets.number_to_win[level-1]:
        if level < 4:
            time.sleep(1)
            session[f'Level {str(level)}:'] = steps
            level += 1
            clear_field(sets.maps[level-1])
        else:
            session[f'Level {str(level)}:'] = steps
            now_time = datetime.datetime.now()
            with open("history.json", "w") as history:
                json5.dump({str(now_time):session}, history)
                history.close()
    drawText()

pgzrun.go()