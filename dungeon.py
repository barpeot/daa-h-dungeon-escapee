import pygame
import copy
import math

from board import boards

pygame.init()

WIDTH = 900
HEIGHT = 950
FPS = 60

level = copy.deepcopy(boards)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('DUNGEON ESCAPEE')
timer = pygame.time.Clock()
main_menu = True
font = pygame.font.Font('freesansbold.ttf', 20)
font_title = pygame.font.Font('freesansbold.ttf', 50)

player_current_sprite = 0
player_images = pygame.transform.scale(pygame.image.load(f'assets/player_images/player_down_1.png'), (45, 45))

player_spritelist_up = []
player_spritelist_down = []
player_spritelist_side = []

player_spritelist_down.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_down_{1}.png'), (45, 45)))
player_spritelist_down.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_down_{2}.png'), (45, 45)))
player_spritelist_down.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_down_{3}.png'), (45, 45)))
player_spritelist_down.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_down_{4}.png'), (45, 45)))

player_spritelist_up.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_up_{1}.png'), (45, 45)))
player_spritelist_up.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_up_{2}.png'), (45, 45)))
player_spritelist_up.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_up_{3}.png'), (45, 45)))
player_spritelist_up.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_up_{4}.png'), (45, 45)))

player_spritelist_side.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_side_{1}.png'), (45, 45)))
player_spritelist_side.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_side_{2}.png'), (45, 45)))
player_spritelist_side.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_side_{3}.png'), (45, 45)))
player_spritelist_side.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/player_side_{4}.png'), (45, 45)))

key_images = pygame.transform.scale(pygame.image.load(f'assets/misc/key.png'), (45, 45))
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))

# for i in range (1, 5):
#     player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

level_game = ' '

player_x = 450
player_y = 663
center_x = 0
center_y = 0
direction = 0

blinky_x = 56
blinky_y = 58
blinky_direction = 0

inky_x = 440
inky_y = 388
inky_direction = 2

pinky_x = 412
pinky_y = 323
pinky_direction = 2

clyde_x = 800
clyde_y = 770
clyde_direction = 2

counter = 0
flicker = False

targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False

blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False

powerup = False
eaten_ghost = [False, False, False, False]

ghost_speeds = [3, 2, 3, 2]


#                Right  Left   Up     Down
turns_allowed = [False, False, False, False]

direction_command = 0
player_speed = 3

time = 0
# obtain_key = False
obtain_key = 0

game_over = False
game_won = False

run = True

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))

        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.direction = 0
        elif self.x_pos > 900:
            self.direction = 1
        return self.x_pos, self.y_pos, self.direction
    
    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.direction = 0
        elif self.x_pos > 900:
            self.direction = 1
        return self.x_pos, self.y_pos, self.direction
    
    def move_blinky(self):
            # r, l, u, d
            # blinky is going to turn whenever colliding with walls, otherwise continue straight
            if self.direction == 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    self.x_pos += self.speed
            elif self.direction == 1:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    self.x_pos -= self.speed
            elif self.direction == 2:
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[2]:
                    self.y_pos -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[3]:
                    self.y_pos += self.speed
            if self.x_pos < -30:
                self.direction = 0
            elif self.x_pos > 900:
                self.direction = 1
            return self.x_pos, self.y_pos, self.direction
    
def draw_misc():
    # score_text = font.render(f'Time: {time}', True, 'white')
    # screen.blit(score_text, (10, 920))

    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))
        gameover_text = font.render('Press \'m\' to change level!', True, 'black')
        screen.blit(gameover_text, (100, 350))

    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
        gameover_text = font.render('Press \'m\' to change level!', True, 'black')
        screen.blit(gameover_text, (100, 350))

def draw_board(obtain_key):
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    
    for i in range (len(level)):
        for j in range (len(level[i])):
            if level[i][j] == 3:
                pygame.draw.line(screen, 'blue', (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, 'blue', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, math.pi / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, 'blue',
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], math.pi / 2, math.pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], math.pi,
                                3 * math.pi / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, 'blue',
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * math.pi / 2,
                                2 * math.pi, 3)
            if level[i][j] == 9 and not obtain_key == 3:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 9 and obtain_key == 3:
                level[i][j] = 0
            if level[i][j] == 1:
                # pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                screen.blit(key_images, (j * num2 + (0.5 * num2) - 20, i * num1 + (0.5 * num1) - 20))

def check_collisions(obtain_key, game_won):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            obtain_key += 1

        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            game_won = True

    return obtain_key, game_won

def draw_player():
    # R L U D
    if direction == 0:
        screen.blit(pygame.transform.flip(player_spritelist_side[counter // 5], True, False), (player_x, player_y))
    elif direction == 1:
        screen.blit(player_spritelist_side[counter // 5], (player_x, player_y))
    elif direction == 2:
        screen.blit(player_spritelist_up[counter // 5], (player_x, player_y))
    elif direction == 3:
        screen.blit(player_spritelist_down[counter // 5], (player_x, player_y))

def check_position(center_x, center_y):
    turns = [False, False, False, False]
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    num3 = 15

    # Check Collision
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][(center_x - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y // num1][(center_x + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + num3) // num1][(center_x) // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y - num3) // num1][(center_x - num3) // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num2) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num2) // num2] < 3:
                    turns[0] = True
        
        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num3) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):

    if 340 < blink_x < 560 and 340 < blink_y < 500:
        blink_target = (400, 100)
    else:
        blink_target = (player_x, player_y)
    
    if 340 < ink_x < 560 and 340 < ink_y < 500:
        ink_target = (400, 100)
    else:
        ink_target = (player_x, player_y)

    if 340 < pink_x < 560 and 340 < pink_y < 500:
        pink_target = (400, 100)
    else:
        pink_target = (player_x, player_y)
    
    if 340 < clyd_x < 560 and 340 < clyd_y < 500:
        clyd_target = (400, 100)
    else:
        clyd_target = (player_x, player_y)

    return [blink_target, ink_target, pink_target, clyd_target]

def draw_menu():
    global level_game
    text = font_title.render('DUNGEON ESCAPEE', True, 'black')
    screen.blit(text, (230, 250))
    
    easy_btn = pygame.draw.rect(screen, 'light gray', [370, 350, 200, 40], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [370, 350, 200, 40], 5, 5)
    text = font.render('Easy', True, 'black')
    screen.blit(text, (450, 360))

    medium_btn = pygame.draw.rect(screen, 'light gray', [370, 450, 200, 40], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [370, 450, 200, 40], 5, 5)
    text = font.render('Medium', True, 'black')
    screen.blit(text, (437, 460))

    hard_btn = pygame.draw.rect(screen, 'light gray', [370, 550, 200, 40], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [370, 550, 200, 40], 5, 5)
    text = font.render('Hard', True, 'black')
    screen.blit(text, (450, 560))

    if easy_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = False
        level_game = 'easy'
    elif medium_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = False
        level_game = 'medium'
    elif hard_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = False
        level_game = 'hard'
    else:
        menu = True
    return menu
# Main Program
while run:
    screen.fill('light blue')
    timer.tick(FPS)
    if main_menu:
        main_menu = draw_menu()
    else:
        if counter < 19:
            counter += 1
            if counter > 3:
                flicker = False
        else:
            counter = 0
            flicker = True

        screen.fill('black')

        draw_board(obtain_key)
        center_x = player_x + 23
        center_y = player_y + 24

        player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
        
        draw_player()
        if level_game == 'easy':
            pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                    pinky_box, 2)
            blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                    blinky_box, 0)
        elif level_game == 'medium':
            pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                    pinky_box, 2)
            inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                    inky_box, 1)
            blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                    blinky_box, 0)
        elif level_game == 'hard':
            pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                    pinky_box, 2)
            inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                    inky_box, 1)
            blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                    blinky_box, 0)
            clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                        clyde_box, 3)
        
        draw_misc()
        
        targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

        player_x, player_y = move_player(player_x, player_y)
        if level_game == 'easy':
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()

            if player_circle.colliderect(pinky.rect):
                game_over = True
            if player_circle.colliderect(blinky.rect):
                game_over = True
        elif level_game == 'medium':
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
            inky_x, inky_y, inky_direction = inky.move_inky()
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()

            if player_circle.colliderect(blinky.rect):
                game_over = True
            if player_circle.colliderect(inky.rect):
                game_over = True
            if player_circle.colliderect(pinky.rect):
                game_over = True 
        elif level_game == 'hard':
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
            inky_x, inky_y, inky_direction = inky.move_inky()
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

            if player_circle.colliderect(blinky.rect):
                game_over = True
            if player_circle.colliderect(inky.rect):
                game_over = True
            if player_circle.colliderect(pinky.rect):
                game_over = True      
            if player_circle.colliderect(clyde.rect):
                game_over = True

        turns_allowed = check_position(center_x, center_y)

        obtain_key, game_won = check_collisions(obtain_key, game_won)

        time += 1 / 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and (game_over or game_won):
                main_menu = True
                powerup = False
                power_counter = 0
                startup_counter = 0
                
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 350
                pinky_direction = 2

                clyde_x = 800
                clyde_y = 770
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0

                obtain_key = 0

                level = copy.deepcopy(boards)

                game_over = False
                game_won = False
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                startup_counter = 0
                
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 350
                pinky_direction = 2

                clyde_x = 800
                clyde_y = 770
                clyde_direction = 2

                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0

                obtain_key = 0

                level = copy.deepcopy(boards)

                #level[]

                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
        
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()

pygame.quit()

