
import pygame

font = None
font_color = (255, 255, 0)


# Initializes global variables
def gui_init(font_size):
    global font
    global font_width

    # Initialize font
    pygame.font.init()
    font = pygame.font.Font("assets/font.otf", font_size)

    # Initialize background music
    pygame.mixer.music.load("assets/theme.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)


# Displays the rank and file markers around the game board
def display_rank_file(start_x, start_y, grid_space, window):

    global font
    global font_color

    # Convert grid coordinates to real coordinates
    real_x = start_x * grid_space
    real_y = start_y * grid_space

    # Draw ranks
    rank = 9
    y = real_y + grid_space
    for i in range(10):
        text = str(rank)
        offset = grid_space // 2 - font.size(text)[0] // 2
        window.blit(font.render(text, True, font_color), (real_x + offset, y))
        y += grid_space
        rank -= 1

    # Draw files
    curr_file = ord('a')
    x = real_x + grid_space
    for i in range(6):
        text = chr(curr_file)
        offset = grid_space // 2 - font.size(text)[0] // 2
        window.blit(font.render(text, True, font_color), (x + offset, real_y))
        x += grid_space
        curr_file += 1


# Displays the username of the current player
def display_turn(player, grid_x, grid_y, grid_space, window):
    global font
    global font_color
    real_x = grid_x * grid_space
    real_y = grid_y * grid_space
    text = "{}'s turn".format(player)
    window.blit(font.render(text, True, font_color), (real_x, real_y))


# Displays the current zlevel being displayed
def display_zlevel(zlevel, grid_x, grid_y, grid_space, window):
    global font
    global font_color
    real_x = grid_x * grid_space
    real_y = grid_y * grid_space
    text = "Zlevel: {}".format(zlevel)
    window.blit(font.render(text, True, font_color), (real_x, real_y))


# Displays the move prompt
def display_move(move, grid_x, grid_y, width, grid_space, window):
    global font
    global font_color
    real_x = grid_x * grid_space
    real_y = grid_y * grid_space
    start_pos = (real_x, real_y + grid_space)
    end_pos = (real_x + width * grid_space, real_y + grid_space)
    text = "> {}".format(move)
    window.blit(font.render(text, True, font_color), (real_x, real_y))
    pygame.draw.line(window, font_color, start_pos, end_pos, 2)
