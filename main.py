import pygame as pg
import random

def draw_button(button):
    pos = buttons[button]['text pos']
    pg.draw.rect(screen, bd_color, buttons[button]['edge'])
    buttons[button]['surface'].fill(button_color)
    buttons[button]['surface'].blit(buttons[button]['text'], pos)

def draw_main_menu():
    screen.fill(bg_color)
    draw_button('play')
    draw_button('settings')

def draw_settings():
    screen.fill(bg_color)
    pg.draw.rect(screen, bd_color, s_menu_edge)
    s_menu.fill(menu_color)
    line_num = 0
    for line in s_lines:
        text_pos_y = s_line_height*line_num + text_size*2//3
        s_menu.blit(s_lines[line]['text'], (text_pos_x_1,  text_pos_y))
        if line == 'mines':
            s_menu.blit(settings_numbers[mines_num],
                        (text_pos_x_2, text_pos_y))
        line_num += 1

def generate_mines():
    global field_cells
    field_cells = []
    for i in range(cells_in_line):
        field_cells.append([])
        for j in range(cells_in_line):
            field_cells[i].append(0)
    mines_list = random.sample(range(cells_in_line**2), mines_num)
    for mine in range(mines_num):
        mines_list[mine] = (mines_list[mine]//cells_in_line,
                            mines_list[mine]%cells_in_line)
    for mine in range(mines_num):
        i = mines_list[mine][0]
        j = mines_list[mine][1]
        neigh = find_neighbors(i, j)
        count = 0
        for case in neigh:
            field_cells[case[0]][case[1]] += 1
    return mines_list

def draw_field_bd():
    pg.draw.rect(screen, bd_color, (bd, bd, field + bd*2, field + bd*2))

def draw_field():
    field_surf.fill(bg_color)
    k = 0
    for i in range(cells_in_line):
        for j in range(cells_in_line):
            this_rect = (j*cell, i*cell, cell, cell)
            if k % 2 == 0:
                pg.draw.rect(field_surf, bd_color, this_rect)
            k += 1
        k += 1

def draw_field_cell(i, j):
    global opens_list, opens_num
    opens_list.append((i, j))
    opens_num += 1
    this_rect = (j*cell, i*cell, cell, cell)
    pg.draw.rect(field_surf, field_color, this_rect)
    if field_cells[i][j] != 0:
        number = numbers[field_cells[i][j]]
        field_surf.blit(number, (j*cell, i*cell))
    else:
        neigh = find_neighbors(i, j)
        for case in neigh:
            if case not in opens_list:
                draw_field_cell(case[0], case[1])

def open_field(win):
    field_surf.fill(field_color)
    for i in range(cells_in_line):
        for j in range(cells_in_line):
            this_rect = (j*cell, i*cell, cell, cell)
            if (i, j) in mines_list:
                if win:
                    if (i + j) % 2 == 0:
                        pg.draw.rect(field_surf, bd_color, this_rect)
                    else:
                        pg.draw.rect(field_surf, bg_color, this_rect)
                    field_surf.blit(flag, (j*cell, i*cell))
                else:
                    pg.draw.rect(field_surf, mine_color, this_rect)
            elif field_cells[i][j] != 0:
                number = numbers[field_cells[i][j]]
                pg.draw.rect(field_surf, field_color, this_rect)
                field_surf.blit(number, (j*cell, i*cell))

def draw_menu():
    pg.draw.rect(screen, bd_color, (field + bd*4, bd, menu + bd*2, field + bd*2))
    menu_surf.fill(menu_color)
    mines_text = font.render('Mines last: {}'.format(mines_last), True, text_color)
    menu_surf.blit(mines_text, menu_line[0])


def start_new_game():
    global mines_last, actual_mines_last, mines_text
    global mines_list, flags_list, opens_list, opens_num

    mines_last = mines_num
    actual_mines_last = mines_num
    mines_text = font.render('Mines last: {}'.format(mines_last), True, text_color)

    mines_list = generate_mines()
    flags_list = []
    opens_list = []
    opens_num = 0

    screen.fill(bg_color)
    draw_field_bd()
    draw_field()
    draw_menu()

def end_game(win):
    global game
    game = False
    open_field(win)
    draw_menu()
    if win:
        menu_surf.blit(win_text, menu_line[1])
    else:
        menu_surf.blit(gameover_text, menu_line[1])
    menu_surf.blit(new_game_text, menu_line[2])

def in_rect(dot, rect):
    rect = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    cond_1 = dot[0] > rect[0] and dot[0] < rect[2]
    cond_2 = dot[1] >= rect[1] and dot[1] <= rect[3]
    return cond_1 and cond_2

def find_neighbors(i, j):
    near = {'top': (i - 1, j),
            'down': (i + 1, j),
            'left': (i, j - 1),
            'right': (i, j + 1),
            'top left': (i - 1, j - 1),
            'top right': (i - 1, j + 1),
            'down left': (i + 1, j - 1),
            'down right': (i + 1, j + 1)}
    neigh = set()
    if i != 0:
        neigh.add(near['top'])
    if i != cells_in_line - 1:
        neigh.add(near['down'])
    if j != 0:
        neigh.add(near['left'])
    if j != cells_in_line - 1:
        neigh.add(near['right'])
    if i != 0 and j != 0:
        neigh.add(near['top left'])
    if i != 0 and j != cells_in_line - 1:
        neigh.add(near['top right'])
    if i != cells_in_line - 1 and j != 0:
        neigh.add(near['down left'])
    if i != cells_in_line - 1 and j != cells_in_line - 1:
        neigh.add(near['down right'])
    return neigh


black      = (0, 0, 0)
tealblue   = (38, 70, 83)
java       = (42, 157, 143)
goldensand = (233, 196, 106)
red        = (231, 111, 81)

bg_color = java
bd_color = tealblue
field_color = goldensand
menu_color = goldensand
button_color = goldensand
text_color = black
mine_color = red

main_menu = True
settings = False
game = False # Game menu

mines_num = 100
max_number = 8
s_max_number = 150
s_change = 10
s_lines_num = 1

cells_in_line = 30
free_cells = cells_in_line**2 - mines_num
cell = 30

field = cell*cells_in_line
menu = field//2
bd = cell//2
width = field + menu + bd*7
height = field + bd*4
text_size = cell
text_pos_x_1 = cell
text_pos_x_2 = cell + menu//2
s_line_height = text_size*3
s_pos_x = (width - menu)//2
s_pos_y = height//2 - s_line_height*s_lines_num//2
s_menu_edge = (s_pos_x - bd, s_pos_y - bd,
               menu + bd*2, s_line_height*s_lines_num + bd*2)

buttons = {'play': {'rect': (width//3, height//3,
                             width//3, height//9),
                    'text pos': (width//8, bd)},
           'settings': {'rect': (width//3, height*5//9,
                                 width//3, height//9),
                        'text pos': (width//12, bd)}}

for button in buttons:
    buttons[button]['edge'] = (buttons[button]['rect'][0] - bd,
                               buttons[button]['rect'][1] - bd,
                               buttons[button]['rect'][2] + bd*2,
                               buttons[button]['rect'][3] + bd*2)

s_lines = {'mines': {}}

line_num = 0
for line in s_lines:
    s_lines[line]['pos'] = (s_pos_x,
                            s_pos_y + (s_line_height + 0.5)*line_num,
                            menu, s_line_height)
    s_lines[line]['color'] = button_color
    line_num += 1

menu_lines_num = 4
menu_line = []
for i in range(menu_lines_num):
    menu_line.append((bd, text_size*i + bd*(i + 1)))

# Paths to files
flag_path = 'flag.png'
alata_path = 'Alata-Regular.ttf'
kufam_path = 'Kufam.ttf'

# Initialization of surfaces, texts and music
pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Minesweeper')
buttons['play']['surface'] = pg.Surface.subsurface(screen, buttons['play']['rect'])
buttons['settings']['surface'] = pg.Surface.subsurface(screen, buttons['settings']['rect'])
s_menu = pg.Surface.subsurface(screen, (s_pos_x, s_pos_y, menu,
                                        s_line_height*s_lines_num))
field_surf = pg.Surface.subsurface(screen, (bd*2, bd*2, field, field))
menu_surf = pg.Surface.subsurface(screen, (field + bd*5, bd*2, menu, field))
flag = pg.image.load(flag_path)

font = pg.font.Font(alata_path, text_size)
main_menu_font = pg.font.Font(alata_path, text_size*2)
num_font = pg.font.Font(kufam_path, text_size)
win_text = font.render('You won!', True, text_color)
gameover_text = font.render('Game over!', True, text_color)
new_game_text = font.render('Press F to start the new game', True, text_color)
buttons['play']['text'] = main_menu_font.render('PLAY', True, text_color)
buttons['settings']['text'] = main_menu_font.render('SETTINGS', True, text_color)
s_lines['mines']['text'] = font.render('Mines num: ', True, text_color)
numbers = []
for i in range(max_number + 1):
    numbers.append(num_font.render(str(i), True, text_color))
settings_numbers = []
for i in range(s_max_number + 1):
    settings_numbers.append(font.render(str(i), True, text_color))

mines_list = generate_mines()
flags_list = []
opens_list = []
opens_num = 0

mouse_in_field = False
run = True
while run:
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False
            elif event.key == pg.K_ESCAPE:
                game = False
                main_menu = True
                settings = False
            elif event.key == pg.K_f:
                game = True
                main_menu = False
                settings = False
                start_new_game()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if game and mouse_in_field:
                i = (mouse[1] - bd*2)//cell
                j = (mouse[0] - bd*2)//cell
                this_rect = (j*cell, i*cell, cell, cell)
                if event.button == 1 and (i, j) not in flags_list:
                    if (i, j) in mines_list:
                        end_game(win = False)
                    elif (i, j) not in opens_list:
                        draw_field_cell(i, j)
                        if opens_num == free_cells:
                            mines_last = 0
                            end_game(win = True)
                elif event.button == 3 and (i, j) not in opens_list:
                    if (i, j) not in flags_list:
                        mines_last -= 1
                        flags_list.append((i, j))
                        field_surf.blit(flag, (j*cell, i*cell))
                        if (i, j) in mines_list:
                            actual_mines_last -= 1
                            if actual_mines_last == 0:
                                end_game(win = True)
                    else:
                        mines_last += 1
                        if (i, j) in mines_list:
                            actual_mines_last += 1
                        flags_list.remove((i, j))
                        if (i + j) % 2 == 0:
                            pg.draw.rect(field_surf, bd_color, this_rect)
                        else:
                            pg.draw.rect(field_surf, bg_color, this_rect)
            elif main_menu:
                for button in buttons:
                    if in_rect(mouse, buttons[button]['rect']):
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if button == 'play':
                                main_menu = False
                                game = True
                                start_new_game()
                            elif button == 'settings':
                                main_menu = False
                                settings = True
            elif settings:
                line_num = 0
                for line in s_lines:
                    if in_rect(mouse, s_lines[line]['pos']):
                        if line == 'mines':
                            # Mouse wheel up
                            if event.button == 4:
                                if mines_num + s_change <= s_max_number:
                                    mines_num += s_change
                                    free_cells -= s_change
                            # Mouse wheel down
                            elif event.button == 5:
                                if mines_num > s_change:
                                    mines_num -= s_change
                                    free_cells += s_change
                    line_num += 1
    if game:
        if in_rect(mouse, (bd*2, bd*2, field, field)):
            mouse_in_field = True
        else:
            mouse_in_field = False
        draw_menu()
    elif main_menu:
        draw_main_menu()
    elif settings:
        draw_settings()
    pg.display.update()

pg.quit()
